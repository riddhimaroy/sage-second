# SAGE — Windows Setup Guide

This guide walks you through running SAGE on a Windows PC from scratch.  
Every step is explained in full — no prior experience assumed.

---

## What You Will Install

| Tool | Purpose |
|------|---------|
| Python 3.11 | Runs the Django backend |
| Node.js 18+ | Runs the React frontend |
| pnpm | Manages JavaScript packages |
| Git | Downloads the project |
| PostgreSQL 16 | The database (optional — SQLite works too) |

---

## STEP 1 — Download the Project

> Skip this step if you already have the project folder on your computer.

1. Open your browser and go to your repository URL.
2. Click the green **Code** button → **Download ZIP**.
3. Right-click the downloaded ZIP → **Extract All** → choose a simple path like `C:\Projects\sage`.

**Or**, if you have Git installed, open **Command Prompt** and run:

```cmd
git clone <your-repo-url> C:\Projects\sage
```

---

## STEP 2 — Install Python 3.11

1. Go to: https://www.python.org/downloads/
2. Click **Download Python 3.11.x** (pick the latest 3.11 version).
3. Run the installer.
4. **IMPORTANT:** On the first screen of the installer, check the box that says **"Add Python to PATH"** before clicking Install Now.
5. Click **Install Now** and wait for it to finish.

**Verify Python installed correctly:**

Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and run:

```cmd
python --version
```

You should see something like: `Python 3.11.9`

If you see an error, restart your computer and try again.

---

## STEP 3 — Install Node.js

1. Go to: https://nodejs.org/
2. Click the **LTS** (Long Term Support) version to download.
3. Run the installer and click **Next** through all the screens — the defaults are fine.

**Verify Node.js installed correctly:**

```cmd
node --version
```

You should see something like: `v20.11.0`

---

## STEP 4 — Install pnpm

pnpm is a faster alternative to npm that this project uses.

Open **Command Prompt** and run:

```cmd
npm install -g pnpm
```

**Verify pnpm:**

```cmd
pnpm --version
```

You should see a version number like `9.1.0`.

---

## STEP 5 — Set Up the Database

You have two options. **SQLite is the easiest** — no installation required.

### Option A: SQLite (Recommended for local use — zero setup)

No extra software needed. The database will be a single file on your computer.  
Skip directly to **Step 6**.

### Option B: PostgreSQL (Closer to production)

1. Go to: https://www.postgresql.org/download/windows/
2. Click **Download the installer** and choose version 16.
3. Run the installer:
   - Set a password for the `postgres` user — **write this down, you will need it**.
   - Leave the port as `5432`.
   - Leave the locale as default.
   - Click **Next** until it installs.
4. After installation, open **pgAdmin** (installed automatically) or use **psql** to create a database:

   Open Command Prompt and run:
   ```cmd
   psql -U postgres
   ```
   Enter your password, then run:
   ```sql
   CREATE DATABASE sage_db;
   \q
   ```

   Your `DATABASE_URL` will be:
   ```
   postgresql://postgres:YOUR_PASSWORD@localhost:5432/sage_db
   ```

---

## STEP 6 — Open the Project Folder

All commands from this point forward must be run from inside your project folder.

Open **Command Prompt** and navigate to the project:

```cmd
cd C:\Projects\sage
```

> If your path has spaces (e.g. `C:\My Projects\sage`), wrap it in quotes:
> ```cmd
> cd "C:\My Projects\sage"
> ```

Keep this Command Prompt window open — you will use it throughout.

---

## STEP 7 — Set Up the Python Backend

### 7a. Create a virtual environment

A virtual environment keeps the Python packages for this project separate from the rest of your computer.

```cmd
python -m venv venv
```

This creates a folder called `venv` inside your project.

### 7b. Activate the virtual environment

```cmd
venv\Scripts\activate
```

Your command prompt line should now start with `(venv)` like this:

```
(venv) C:\Projects\sage>
```

> You must activate the virtual environment every time you open a new Command Prompt window.

### 7c. Install Python packages

```cmd
pip install -r artifacts\api-server\requirements.txt
```

Wait for all packages to download and install. This may take 1–2 minutes.

---

## STEP 8 — Configure Environment Variables

### If using SQLite (Option A from Step 5)

No configuration needed — the app uses SQLite automatically when no database URL is set.

### If using PostgreSQL (Option B from Step 5)

You need to tell the app where your database is. Run this in your Command Prompt (replace `YOUR_PASSWORD` with the password you set in Step 5):

```cmd
set DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/sage_db
```

> This variable only lasts for the current Command Prompt session. You will need to run it again each time you open a new window, or follow the permanent method below.

**To set it permanently on Windows:**

1. Press `Win + S` and search for **"Environment Variables"**.
2. Click **"Edit the system environment variables"**.
3. Click the **"Environment Variables"** button at the bottom.
4. Under **User variables**, click **New**.
5. Variable name: `DATABASE_URL`
6. Variable value: `postgresql://postgres:YOUR_PASSWORD@localhost:5432/sage_db`
7. Click OK on all windows.
8. **Restart Command Prompt** for changes to take effect.

---

## STEP 9 — Run the Django Backend

Make sure your virtual environment is still active (you see `(venv)` at the start of the line).  
If not, run `venv\Scripts\activate` again.

Navigate to the Django project:

```cmd
cd artifacts\api-server\sage_backend
```

### 9a. Apply database migrations

```cmd
python manage.py migrate --noinput
```

You should see lines like `Applying meals.0001_initial... OK`.

### 9b. Seed the meal database

```cmd
python manage.py seed_meals
```

You should see: `Seeding complete: 151 meals created, 0 already existed.`

### 9c. Start the Django server

```cmd
python manage.py runserver 0.0.0.0:8080
```

You should see:

```
Starting development server at http://0.0.0.0:8080/
Quit the server with CTRL-BREAK.
```

**The backend is now running. Leave this window open.**

To verify it works, open your browser and go to:
```
http://localhost:8080/api/healthz
```
You should see: `{"status": "ok"}`

---

## STEP 10 — Run the React Frontend

**Open a second Command Prompt window** (keep the first one running Django).

Navigate back to the project root:

```cmd
cd C:\Projects\sage
```

Install JavaScript dependencies:

```cmd
pnpm install
```

Start the frontend:

```cmd
$env:PORT=3000
$env:BASE_PATH="/"
pnpm --filter @workspace/sage run dev
```

You should see output like:

```
  VITE v5.x  ready in 500ms

  ➜  Local:   http://localhost:5173/
```

**Open your browser and go to:** `http://localhost:5173`

You should see the SAGE dashboard.

---

## You Are All Set

| Service | URL |
|---------|-----|
| Frontend (React) | http://localhost:5173 |
| Backend (Django) | http://localhost:8080 |
| Health check | http://localhost:8080/api/healthz |

---

## Every Time You Want to Start the App

You need to start both the backend and the frontend in separate Command Prompt windows.

### Window 1 — Start the backend

```cmd
cd C:\Projects\sage
venv\Scripts\activate
cd artifacts\api-server\sage_backend
python manage.py runserver 0.0.0.0:8080
```

### Window 2 — Start the frontend

```cmd
cd C:\Projects\sage
pnpm --filter @workspace/sage run dev
```

Then open `http://localhost:5173` in your browser.

---

## Troubleshooting

### "python is not recognized as a command"

Python was not added to your PATH during installation.  
Fix: Re-run the Python installer, check "Add Python to PATH", then restart Command Prompt.

### "pip is not recognized as a command"

Run this instead:
```cmd
python -m pip install -r artifacts\api-server\requirements.txt
```

### "pnpm is not recognized as a command"

Close and reopen Command Prompt after installing pnpm, then try again.

### "venv\Scripts\activate is not recognized"

Make sure you are in the project root folder (`C:\Projects\sage`) before running activate.

### "(venv) disappeared after I closed Command Prompt"

The virtual environment must be activated every time you open a new window.  
Run `venv\Scripts\activate` again.

### The browser shows "This site can't be reached"

Make sure both Command Prompt windows are still running (not closed or showing errors).  
Check that you used the correct URL — frontend is port `5173`, backend is port `8080`.

### Port 8080 or 5173 is already in use

Find and close whatever is using that port, or change the port number:

- Backend on a different port: `python manage.py runserver 0.0.0.0:8090`
- Frontend on a different port: add `-- --port 5174` to the pnpm command

### Database connection error (PostgreSQL only)

- Make sure the PostgreSQL service is running: press `Win + R`, type `services.msc`, find **postgresql-x64-16** and check it says **Running**.
- Double-check the `DATABASE_URL` variable has the correct password and database name.
- If in doubt, use SQLite (Option A) by unsetting the variable:
  ```cmd
  set DATABASE_URL=
  ```

### "No module named 'django'" even after pip install

Your virtual environment may not be active. Run:
```cmd
venv\Scripts\activate
```
Then try again.

---

## Stopping the App

- In each Command Prompt window, press `Ctrl + C` to stop the server.
- Close the windows when done.
