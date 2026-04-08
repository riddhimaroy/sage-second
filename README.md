# SAGE — Smart Nutrition Tracker

A full-stack nutrition tracking web app. Log meals, track your daily macros, and review weekly trends.

**Stack:** React + Vite (frontend) · Django + Django REST Framework (backend) · PostgreSQL

---

## Project Structure

```
workspace/
├── artifacts/
│   ├── sage/                   # React + Vite frontend
│   │   └── src/
│   │       ├── App.tsx
│   │       ├── pages/          # Dashboard, DailyLog, WeeklyView
│   │       └── api/            # Auto-generated API client
│   └── api-server/             # Django backend
│       ├── requirements.txt
│       ├── start_django.sh     # Startup script (migrate → seed → runserver)
│       └── sage_backend/       # Django project root
│           ├── manage.py
│           ├── sage_backend/   # Project settings & URLs
│           ├── meals/          # Meal model, search/list endpoints
│           └── logs/           # DailyLog, LogEntry, weekly summary
└── README.md
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| pnpm | 9+ |
| PostgreSQL | 14+ (or use SQLite for local dev) |

---

## Deploy Again

- **Backend** - 

cd artifacts\api-server
venv\Scripts\activate
cd sage_backend
python manage.py runserver 0.0.0.0:8080

- **Frontend**

$env:PORT=3000
$env:BASE_PATH="/"
pnpm --filter @workspace/sage run dev

## Running Locally

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd workspace

# Install frontend dependencies
pnpm install
```

### 2. Set up the Python environment

```bash
cd artifacts/api-server

# Install Python packages
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file at the project root (or export these in your shell):

```bash
# Required for PostgreSQL. If not set, SQLite is used automatically.
DATABASE_URL=postgresql://user:password@localhost:5432/sage_db

# Optional — defaults shown
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
PORT=8080
```

### 4. Run the backend (Django)

```bash
# From the api-server directory
bash start_django.sh
```

This script will:
1. Apply all database migrations
2. Seed the meal database (Indian foods + international items, ~160 entries)
3. Start the Django development server on `http://localhost:8080`

Or run each step manually:

```bash
cd sage_backend

python manage.py migrate --noinput
python manage.py seed_meals
python manage.py runserver 0.0.0.0:8080
```

### 5. Run the frontend (React + Vite)

In a separate terminal:

```bash
# From the workspace root
pnpm --filter @workspace/sage run dev
```

The frontend will start on `http://localhost:5173` (or the next available port).

---

## API Endpoints

All endpoints are prefixed with `/api/`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/healthz` | Health check — returns `{"status": "ok"}` |
| GET | `/api/meals/search?q=<query>` | Search meals by name |
| GET | `/api/meals/` | List all meals (paginated) |
| GET | `/api/logs/today` | Get today's log with totals |
| GET | `/api/logs/<date>` | Get log for a specific date (`YYYY-MM-DD`) |
| POST | `/api/logs/<date>/entries` | Add a meal entry to a log |
| PUT | `/api/logs/entries/<id>` | Update a log entry |
| DELETE | `/api/logs/entries/<id>` | Delete a log entry |
| GET | `/api/logs/weekly` | Weekly summary (last 7 days) |
| DELETE | `/api/logs/cleanup` | Delete logs older than 7 days |

---

## Database Seeding

The `seed_meals` command populates the database with ~160 food items across these categories:

**International:** Protein, Grains, Vegetables, Fruits, Dairy, Legumes, Nuts

**Indian Cuisine:**
- Indian Breakfast (Idli, Dosa, Poha, Upma, Paratha, Uttapam…)
- Indian Grains & Breads (Roti, Naan, Biryani, Khichdi…)
- Indian Dal (Dal Tadka, Dal Makhani, Rajma, Chole…)
- Indian Curries — Chicken, Mutton, Vegetarian (Butter Chicken, Palak Paneer, Aloo Gobi…)
- Indian Seafood (Fish Curry, Prawn Masala, Fish Tikka…)
- Indian Snacks & Street Food (Samosa, Pani Puri, Vada Pav, Bhel Puri…)
- Indian Dairy (Paneer, Dahi, Lassi, Raita, Ghee…)
- Indian Tandoor & Kebabs (Tandoori Chicken, Seekh Kebab, Paneer Tikka…)
- Indian Sweets (Gulab Jamun, Kheer, Halwa, Jalebi…)
- South Indian Specials (Appam, Rasam, Avial, Puttu…)
- North Indian Specials (Chole Bhature, Sarson Da Saag, Kadhi Pakoda…)
- Indian Drinks (Masala Chai, Mango Lassi, Aam Panna…)

To re-seed or add new items, simply add entries to the `SAMPLE_MEALS` list in:
`artifacts/api-server/sage_backend/meals/management/commands/seed_meals.py`

Then run:
```bash
python manage.py seed_meals
```

---

## Production Deployment

For production use Gunicorn instead of the Django development server:

```bash
cd artifacts/api-server/sage_backend
gunicorn sage_backend.wsgi:application --bind 0.0.0.0:8080 --workers 2
```

Also set these environment variables in production:

```bash
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<a-long-random-secret>
DATABASE_URL=<your-production-postgres-url>
```

---

## Features

- **Meal Search** — instant search across 160+ food items including Indian cuisine
- **Daily Logging** — log meals with quantity, view per-meal macros
- **Macro Tracking** — calorie, protein, carbs, and fats progress bars with daily goals
- **Weekly Trends** — 7-day calorie chart, average intake, tracking streak
- **Auto-cleanup** — remove logs older than 7 days with one click
