# SignFlow Backend (Django)

This is the backend service for **SignFlow**, a digital contract signing platform.  
It provides secure APIs for user management, document uploads, and e-signature workflows.

-----------------------------------------------------

🚀 Features
- JWT-based user authentication
- Role-based access (Manager & Employee)
- Document upload & storage
- Integration with Setu API for e-signatures
- APScheduler job for auto-updating signature status
- PostgreSQL on Supabase (with local SQLite option for dev)

-----------------------------------------------------

## ⚙️ Tech Stack
- Backend: Python, Django, Django REST Framework
- Database: PostgreSQL (Supabase) / SQLite (local dev)
- Auth: JWT (SimpleJWT)
- Scheduler: APScheduler

---

## 🛠️ Setup Instructions
### 1. Clone the repository
```bash
git clone https://github.com/abhirup2565/Esign_Project-Backend.git
cd Esign_Project-Backend
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependency 
```bash
pip install -r requirements.txt
```

### 3. Databse Configuration
The database configuration is in backend/settings.py<br>
This project supports two database setups:<br>
1)SQLite:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
2)PostgreSQL
```bash
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DIRECT_URL'))
}
```

### 5. Configure environment variables:
Create a .env file in the backend folder. <br>You’ll need values from different services:
| Variable                   | Where to Get It                                                       | Description                                       |
| -------------------------- | --------------------------------------------------------------------- | ------------------------------------------------- |
| `SECRET_KEY`               | Generate using `django.core.management.utils.get_random_secret_key()` | Required by Django for security                   |
| `DATABASE_URL`             | From [Supabase project](https://supabase.com/)                        | PostgreSQL connection string (used in production) |
| `SETU_CLIENT_ID`           | From [Setu Dashboard](https://docs.setu.co/dev-tools/bridge/overview) | Client ID for API authentication                  |
| `SETU_CLIENT_SECRET`       | From Setu Dashboard                                                   | Secret key for API authentication                 |
| `SETU_PRODUCT_INSTANCE_ID` | From Setu Dashboard                                                   | Unique identifier for your Setu product instance  |


Example .env
```bash
SECRET_KEY=your_django_secret
DATABASE_URL=postgresql://user:password@host:5432/dbname

SETU_CLIENT_ID=xxxx
SETU_CLIENT_SECRET=xxxx
SETU_PRODUCT_INSTANCE_ID=xxxx

ENABLE_SCHEDULER=true
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7 .Start server
```bash
python manage.py runserver
```

-----------------------------------------------------

## ⏳ Background Jobs (APScheduler)
The backend uses APScheduler to automatically keep signature statuses in sync with Setu.
- Task: Periodically polls Setu for the status of pending signatures.
- Database Update: Updates the corresponding records in the database once the status changes.
- Polling Interval: Configurable inside backend/api/scheduler.py
- ⚠️ Note: If you are running locally on SQLite, avoid using very short intervals (e.g., below 15 seconds). SQLite does not handle concurrent writes well, which can lead to database locking issues. For production, a more robust database like PostgreSQL is recommended.
Scheduler Example (from scheduler.py):
```bash
def start_scheduler():
    # Poll signature status every 10 seconds
    scheduler.add_job(poll_signature, 'interval', seconds=10)
    scheduler.start()

    # Graceful shutdown on exit
    atexit.register(lambda: scheduler.shutdown())
```
**Disabling APScheduler**:<br>
Disable APScheduler by setting ENABLE_SCHEDULER=false in your .env <br>
Example of .env
```bash
ENABLE_SCHEDULER=false
```

-----------------------------------------------------

## 📡 API Endpoints
🔑 Authentication
| Endpoint              | Method | Description                        |
| --------------------- | ------ | ---------------------------------- |
| `/api/token/`         | POST   | Obtain JWT access & refresh tokens |
| `/api/token/refresh/` | POST   | Refresh JWT access token           |

👤 Users
| Endpoint             | Method | Description                            |
| -------------------- | ------ | -------------------------------------- |
| `/api/users/create/` | POST   | Create a new user (Manager / Employee) |
| `/api/users/list/`   | GET    | List all users                         |

📄 Documents & Signatures
| Endpoint                         | Method | Description                                            |
| -------------------------------- | ------ | ------------------------------------------------------ |
| `/api/documents/`                | POST   | Upload a document for signing                          |
| `/api/signature/`                | POST   | Create a signature request                             |
| `/api/signature/<signature_id>/` | GET    | Fetch status of a specific signature                   |
| `/api/download/<signature_id>/`  | GET    | Download the signed document                           |
| `/api/status/`                   | GET    | Fetch overall status of document & signatures          |
| `/api/dashboard/`                | GET    | Get dashboard data (Signature status of paticular user)|

⚙️ Admin
| Endpoint  | Method | Description        |
| --------- | ------ | ------------------ |
| `/admin/` | GET    | Django Admin Panel |