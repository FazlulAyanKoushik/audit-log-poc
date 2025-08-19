from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import DocumentAccess


class DocumentPermission(BasePermission):
    """
    Controls access based on owner or DocumentAccess table.
    - Owner: full access
    - View: GET only
    - Edit: PUT/PATCH allowed
    - Delete: DELETE allowed
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Owner always has full access
        if obj.owner == user:
            return True

        try:
            access = DocumentAccess.objects.get(document=obj, user=user)
        except DocumentAccess.DoesNotExist:
            return False

        if request.method in SAFE_METHODS:
            return True if access.access_type in ["view", "edit", "delete"] else False

        if request.method in ["PUT", "PATCH"]:
            return access.access_type == "edit"

        if request.method == "DELETE":
            return access.access_type == "delete"

        return False
