# FBC Project Installation Guide

This guide explains how to install and run the FBC (Faculty Blockchain Collaboration) project on a new machine.

It is written for beginners and includes step-by-step instructions for getting the project working locally.

## What you need first

Before you begin, make sure you have:

- **Python 3.9 or newer**
- **pip** (Python package installer)
- **A text editor or IDE** such as VS Code
- **PostgreSQL** (optional for this project if you plan to use a remote database)
- **Git** only if you want to clone from a remote repository

> If you already have the project folder on your device, you do not need Git.

## Step 0: Confirm your Python setup

Open a terminal or command prompt and run:

```bash
python --version
pip --version
```

If `python` is not found, try one of these commands:

```bash
py --version
python3 --version
```

If the commands work, you are ready to continue.

## Step 1: Get the project files

The project root folder is named `NEXUS`.

### Option A: Clone the repository (requires Git)

```bash
git clone <repository-url>
cd NEXUS
```

### Option B: Copy the project folder directly (recommended if you do not want Git)

1. Transfer the whole `NEXUS` folder to the target device.
2. Open a terminal or command prompt.
3. Change into the project folder:

```bash
cd path\to\NEXUS
```

If the folder is already on your machine, just open it and move to the next step.

## Step 2: Create a virtual environment

A virtual environment keeps this project’s Python packages separate from your global Python installation.

### Windows

```bash
python -m venv FBCenvironment
FBCenvironment\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv FBCenvironment
source FBCenvironment/bin/activate
```

After activation, your terminal prompt should show:

```bash
(FBCenvironment)
```

If it does not, try `python` instead of `python3`, or use `py -3` on Windows.

## Step 3: Install the project dependencies

In the `NEXUS` folder, run:

```bash
pip install -r requirements.txt
```

If the `requirements.txt` file is missing, install the packages manually:

```bash
pip install Django==6.0.5
pip install psycopg2-binary==2.9.12
pip install python-dotenv==1.2.2
pip install dj-database-url==3.1.2
```

## Step 4: Check the database settings

This project currently uses the database connection defined in `NEXUS/settings.py`.

That means:

- You may not need to create a `.env` file right now.
- If you want to use a `.env` file later, the project already has the required packages installed.

### Optional: Create a `.env` file

If you decide to use environment variables, create a file named `.env` in the `NEXUS` folder with these values:

```bash
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

> Note: `NEXUS/settings.py` is currently configured with a default PostgreSQL URL. If you change this file, the application will use the values you supply.

## Step 5: Run database migrations

Run the Django migrations to prepare the database tables:

```bash
python manage.py migrate
```

If the command fails, check the database connection settings in `NEXUS/settings.py`.

## Step 6: Verify the application can connect

Open the Django shell:

```bash
python manage.py shell
```

Then type:

```python
from core.models import Users
print(Users.objects.count())
exit()
```

If this works, Django can connect to the database.

## Step 7: Start the development server

Run:

```bash
python manage.py runserver
```

You should see a message like:

```bash
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Step 8: Open the application in your browser

Visit:

```bash
http://localhost:8000
```

You should see the FBC application home page.

## Useful commands for beginners

- Activate the virtual environment again:

```bash
# Windows
FBCenvironment\Scripts\activate

# Mac/Linux
source FBCenvironment/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Check Django configuration:

```bash
python manage.py check
```

- Create a new admin user:

```bash
python manage.py createsuperuser
```

- Use a different server port:

```bash
python manage.py runserver 8001
```

## Project structure

```
NEXUS/
├── core/                          # Main Django app
│   ├── models.py                 # Database models
│   ├── views.py                  # API views and endpoints
│   ├── app.js                    # Frontend JavaScript
│   ├── index.html                # Frontend UI
│   ├── style.css                 # CSS styles
│   ├── migrations/               # Django migrations
│   └── management/
│       └── commands/
│           └── migrate_schema.py # Custom migration support
│
├── NEXUS/                         # Django project settings
│   ├── settings.py               # Project settings and database config
│   ├── urls.py                   # URL routes
│   ├── wsgi.py                   # WSGI app entry point
│   └── asgi.py                   # ASGI app entry point
│
├── FBCenvironment/               # Python virtual environment
├── manage.py                     # Django command-line utility
├── requirements.txt              # Python package list
├── db.sqlite3                    # Local SQLite database file (development only)
```

## Common troubleshooting

### Problem: `python` or `pip` not found

- Use `py -3` on Windows.
- Use `python3` on Mac/Linux.
- Make sure Python is installed and added to your PATH.

### Problem: `ModuleNotFoundError: No module named 'django'`

- Activate the virtual environment.
- Run `pip install -r requirements.txt`.

### Problem: port 8000 already in use

- Start the server on another port:

```bash
python manage.py runserver 8001
```

### Problem: database connection fails

- Check `NEXUS/settings.py` for the correct connection URL.
- If you are using Supabase, confirm the credentials in its dashboard.

### Problem: `requirements.txt` file missing

- Confirm you are in the `NEXUS` folder.
- If needed, install packages manually.

## Notes

- Always run commands from the `NEXUS` folder.
- If you transfer the project to another machine, copy the full `NEXUS` folder.
- You do not need Git if the files are already on the target device.

## Additional resources

- [Python Downloads](https://www.python.org/downloads/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

Last Updated: May 8, 2026
