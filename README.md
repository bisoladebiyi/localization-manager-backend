# 🔧 Localization Manager — Backend API

This is the backend API for the Localization Manager, built with **FastAPI** and connected to **Supabase** (PostgreSQL).

## 🌟 Features

- Full CRUD for localization keys
- Bulk update endpoint
- UUID-based resource IDs

---

## ⚙️ Stack

- **FastAPI**
- **Supabase-py**
- **Pydantic**
- **Uvicorn** 
- **PostgreSQL** (via Supabase)

---

## 📦 Installation

```bash
git clone https://github.com/bisoladebiyi/localization-manager-backend.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the server

Create your `.env` file in root folder

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

Run your API

```bash
uvicorn src.localization_management_api.main:app --reload
```

## 📚 Endpoints

| Method | Route                              | Description                  |
|--------|------------------------------------|------------------------------|
| GET    | `/api/localizations`               | Get all localization keys    |
| GET    | `/api/localizations/{id}`          | Get localization by ID       |
| POST   | `/api/localizations`               | Create new localization      |
| PUT    | `/api/localizations/{id}`          | Edit a localization          |
| POST   | `/api/localizations/bulk-update`   | Bulk update localizations    |
| DELETE | `/api/localizations/{id}`          | Delete a localization        |

## ✅ Testing

```bash
pytest
```
**Tests cover:**

- Input validation  
- Bulk update behavior  
- DB query correctness (with mock Supabase client)

