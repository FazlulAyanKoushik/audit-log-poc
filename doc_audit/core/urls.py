from django.urls import path
from .views import (
    DocumentListCreateView,
    DocumentDetailView,
    DocumentAccessCreateView,
    DocumentAccessListView,
    DocumentHistoryView,
    DocumentRollbackView,
)

urlpatterns = [
    path("/documents", DocumentListCreateView.as_view(), name="document-list-create"),
    path("/documents/<int:pk>", DocumentDetailView.as_view(), name="document-detail"),
    path("/documents/<int:doc_id>/access", DocumentAccessCreateView.as_view(), name="document-access-create"),
    path("/documents/<int:doc_id>/access/list", DocumentAccessListView.as_view(), name="document-access-list"),

    # ============================== Document History and Rollback ==========================================
    path("/documents/<int:doc_id>/history", DocumentHistoryView.as_view(), name="document-history"),
    path("/documents/<int:doc_id>/rollback/<int:log_id>", DocumentRollbackView.as_view(), name="document-rollback"),
]
