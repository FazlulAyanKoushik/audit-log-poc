# 📄 Django DRF Document Audit System

A Django REST Framework (DRF) project with **JWT authentication** and **document history tracking** using [`django-auditlog`](https://github.com/jjkester/django-auditlog).  

Users can:
- Create documents  
- Share documents with other users (view / edit / delete access)  
- View the full audit history of each document (who changed what, when)  
- Rollback to previous versions (owner only)  

---

## 🚀 Features
- **Authentication**: JWT tokens via [`djangorestframework-simplejwt`](https://github.com/jazzband/djangorestframework-simplejwt).  
- **Access Control**:
  - Owner → full access  
  - View → read-only  
  - Edit → update allowed  
  - Delete → delete allowed  
- **Audit Logging**: Tracks create, update, and delete actions with actor + field changes.  
- **Rollback**: Owner can restore a document to a previous version.  

---

## 📦 Installation

### 1. Clone & setup
```bash
    git clone https://github.com/your-username/document-audit.git
    cd document-audit
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
    pip install -r requirements.txt
```

### 3. Run migrations & create superuser
```bash
    python manage.py migrate
    python manage.py createsuperuser
```

### 4. Run runserver
```bash
  python manage.py runserver
```


## 📚 API Endpoints
#### Documents

* GET /api/documents/ → list user documents
* POST /api/documents/ → create document
* GET /api/documents/{id}/ → get document details
* PATCH /api/documents/{id}/ → update document (owner or edit access)
* DELETE /api/documents/{id}/ → delete document (owner or delete access)

#### Document Access

* POST /api/documents/{doc_id}/access/ → assign access (owner only)
* GET /api/documents/{doc_id}/access/list/ → list users with access (owner only)

#### Document History

* GET /api/documents/{doc_id}/history/ → list all changes for a document
* POST /api/documents/{doc_id}/rollback/{log_id}/ → rollback to previous version (owner only)