# SAGE - Windows Setup Guide

This guide shows the exact steps to run this project on Windows after downloading it from GitHub.

These instructions assume:

- You downloaded the repository as a ZIP from GitHub and extracted it.
- You are using PowerShell on Windows.
- You want the simplest local setup.

This project runs as two apps:

- Backend: Django on `http://localhost:8080`
- Frontend: Vite + React on `http://localhost:3000`

## 1. Install What You Need

Install these tools first:

- Python 3.11 or newer
- Node.js 18 or newer
- Git (optional, only needed if you want to clone instead of downloading ZIP)

Check them in PowerShell:

```powershell
python --version
node --version
npm --version
```

If `python` does not work, reinstall Python and make sure `Add Python to PATH` is enabled during setup.

## 2. Download And Extract The Project

If downloading from GitHub:

1. Open the repository on GitHub.
2. Click `Code`.
3. Click `Download ZIP`.
4. Extract it somewhere simple, for example:

```text
C:\Projects\Smart-Nutrition-Log-main
```

Open PowerShell and go to the extracted folder:

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
```

If your folder path has spaces, use quotes:

```powershell
cd "C:\Users\YourName\Downloads\Smart Nutrition Log"
```

## 3. Install Frontend Dependencies

This repo uses `pnpm`, but you do not need to install it globally first. Use `npx`:

```powershell
npx pnpm install
```

This installs the workspace dependencies from the root of the repo.

## 4. Create And Activate The Python Virtual Environment

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

After activation, your prompt should start with `(venv)`.

## 5. Install Backend Dependencies

With the virtual environment active, run:

```powershell
pip install -r .\artifacts\api-server\requirements.txt
```

## 6. Set Up The Database

For a normal local run, you do not need PostgreSQL.

This project already falls back to SQLite automatically when `DATABASE_URL` is not set. That means you can skip database setup entirely for local use.

The SQLite database file will be created here when you run migrations:

```text
artifacts\api-server\sage_backend\db.sqlite3
```

## 7. Run Backend Setup Commands

Still in the repo root, run:

```powershell
cd .\artifacts\api-server\sage_backend
python manage.py migrate
python manage.py seed_meals
```

What these do:

- `migrate` creates the database tables
- `seed_meals` loads the built-in meal data used by the app

## 8. Start The Django Backend

In the same PowerShell window:

```powershell
python manage.py runserver 0.0.0.0:8080
```

Leave that window open.

You can verify the backend is running by opening:

```text
http://localhost:8080/api/healthz
```

You should get:

```json
{"status":"ok"}
```

## 9. Start The React Frontend

Open a second PowerShell window.

Go back to the project root:

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
```

Set the environment variables required by `artifacts/sage/vite.config.ts`:

```powershell
$env:PORT="3000"
$env:BASE_PATH="/"
```

Then start the frontend:

```powershell
npx pnpm --filter @workspace/sage run dev
```

Leave this second window open too.

Open the app in your browser:

```text
http://localhost:3000
```

## 10. Exact Daily Startup Commands

After the project has already been installed once, this is all you need next time.

Window 1: backend

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
.\venv\Scripts\Activate.ps1
cd .\artifacts\api-server\sage_backend
python manage.py runserver 0.0.0.0:8080
```

Window 2: frontend

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
$env:PORT="3000"
$env:BASE_PATH="/"
npx pnpm --filter @workspace/sage run dev
```

Then open:

- Frontend: `http://localhost:3000`
- Backend health check: `http://localhost:8080/api/healthz`

## 11. First-Time Full Setup Commands

If you want the complete setup as one checklist, use these exact commands.

Window 1:

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
npx pnpm install
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\artifacts\api-server\requirements.txt
cd .\artifacts\api-server\sage_backend
python manage.py migrate
python manage.py seed_meals
python manage.py runserver 0.0.0.0:8080
```

Window 2:

```powershell
cd C:\Projects\Smart-Nutrition-Log-main
$env:PORT="3000"
$env:BASE_PATH="/"
npx pnpm --filter @workspace/sage run dev
```

## Troubleshooting

### `python` is not recognized

Python is either not installed or not on PATH. Reinstall Python and enable `Add Python to PATH`.

### PowerShell says running scripts is disabled

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

### `npx pnpm install` fails

Make sure Node.js is installed correctly:

```powershell
node --version
npm --version
```

Then retry:

```powershell
npx pnpm install
```

### Frontend fails with `PORT environment variable is required`

That is expected if `PORT` and `BASE_PATH` were not set first. Run:

```powershell
$env:PORT="3000"
$env:BASE_PATH="/"
```

Then start the frontend again.

### Backend starts but frontend cannot reach the API

Make sure:

- Django is running on `http://localhost:8080`
- The frontend was started from the repo root
- You opened `http://localhost:3000`

The frontend Vite server proxies `/api` to `http://localhost:8080`.

### Seed command fails

Make sure you are in this folder before running it:

```text
artifacts\api-server\sage_backend
```

Then run:

```powershell
python manage.py seed_meals
```

## Stop The Project

In each PowerShell window, press `Ctrl + C`.
