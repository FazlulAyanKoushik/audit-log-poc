from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from auditlog.context import set_actor

from .models import Document, DocumentAccess
from .serializers import DocumentSerializer, DocumentAccessSerializer, LogEntrySerializer
from .permissions import DocumentPermission


class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, DocumentPermission]


class DocumentAccessCreateView(generics.CreateAPIView):
    """
    Owner assigns access to other users.
    """
    serializer_class = DocumentAccessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        document_id = self.kwargs.get("doc_id")
        document = get_object_or_404(Document, id=document_id)

        if document.owner != self.request.user:
            raise PermissionError("Only owner can assign access.")

        serializer.save(document=document)


class DocumentAccessListView(generics.ListAPIView):
    serializer_class = DocumentAccessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        document_id = self.kwargs.get("doc_id")
        document = get_object_or_404(Document, id=document_id)

        if document.owner != self.request.user:
            raise PermissionError("Only owner can view access list.")

        return DocumentAccess.objects.filter(document=document)



# ====================================Document History==============================================
from auditlog.models import LogEntry


class DocumentHistoryView(generics.ListAPIView):
    """
    List all audit log entries for a document.
    """
    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated, DocumentPermission]

    def get_queryset(self):
        doc_id = self.kwargs.get("doc_id")
        document = get_object_or_404(Document, id=doc_id)

        # Check object permission (view allowed)
        self.check_object_permissions(self.request, document)

        return LogEntry.objects.filter(
            content_type__model="document", object_pk=str(doc_id)
        ).order_by("-timestamp")


from rest_framework.views import APIView


class DocumentRollbackView(APIView):
    """
    Roll back a document to a previous version.
    Only owner can roll back.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, doc_id, log_id):
        document = get_object_or_404(Document, id=doc_id)
        log_entry = get_object_or_404(
            LogEntry, id=log_id, content_type__model="document", object_pk=str(doc_id)
        )

        # Only owner can rollback
        if document.owner != request.user:
            return Response({"detail": "Only owner can rollback."}, status=403)

        # Apply rollback (use the old values from log_entry.changes)
        changes = log_entry.changes
        if not isinstance(changes, dict):
            return Response({"detail": "No changes found."}, status=400)

        for field, values in changes.items():
            old_value, new_value = values
            setattr(document, field, old_value)

        with set_actor(request.user):
            document.save()

        return Response(
            {"detail": f"Document rolled back using log {log_id}"},
            status=status.HTTP_200_OK,
        )
