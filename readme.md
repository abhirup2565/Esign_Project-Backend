# SignFlow Backend (Django)

This is the backend service for **SignFlow**, a digital contract signing platform.  
SignFlow is a digital contract signing platform that enables organizations to manage, sign, and track documents seamlessly. It supports two types of users — Managers and Employees — each with different capabilities to keep workflows secure and streamlined.

Managers can onboard new users, upload documents, and initiate signing requests. They can also sign documents themselves, track the progress of documents assigned to employees, and download the final signed copies once the signing process is complete.

Employees, on the other hand, get a simplified experience where they can view documents assigned to them, sign when required, monitor the signing status, and download completed documents.

Behind the scenes, SignFlow integrates with Setu’s e-signature API to handle digital signatures. A background job powered by APScheduler ensures that signatures status are periodically synced from Setu to the local database. This way, users always see the latest signing state without needing to manually refresh.

The frontend (React) communicates with this Django REST API backend to provide a smooth, role-based workflow for managing contracts digitally.

💡 Frontend Repository: The backend works together with [SignFlow Frontend](https://github.com/abhirup2565/Esign_Project.git) repository, which is a React-based application that interacts with these APIs.

-----------------------------------------------------

## 🚀 Features
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

## 🛠️ Setup Instructions(With and Without 🐳Docker)
### 1. Clone the repository
```bash
git clone https://github.com/abhirup2565/Esign_Project-Backend.git
cd Esign_Project-Backend
```
### 🐳 Running with Docker
## 2. Environment Variables
The service loads environment variables from the .env file.<br>
The docker-compose.yml mounts your project folder into the container<br>
**Create a .env file in the root of your project**<br>
You’ll need values from different services:<br>
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
## 3. Build and Run Container
```bash
docker-compose up --build
```
This will:
- Build the Docker image from the Dockerfile.
- Start the backend project service.
- Run migrations automatically.
- Expose the app on http://localhost:8000


### ⚙️ Local Development (Without Docker)
### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependency 
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
The database default to local sqlite <br>
To use external database like postgres. <br>
SET DATABASE_URL variable in .env file.<br>
Example:
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
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
    scheduler.add_job(poll_signature, 'interval', seconds=15)
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