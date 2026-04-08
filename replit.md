# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)
- **Frontend**: React + Vite (with Tailwind CSS, shadcn/ui, wouter, recharts)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

## Artifacts

### SAGE - Smart Nutrition Tracker (`artifacts/sage`)
- **Preview path**: `/`
- **Purpose**: Full-stack nutrition tracking app
- **Pages**: Dashboard (`/`), Daily Log (`/log`), Weekly View (`/weekly`)

### API Server (`artifacts/api-server`)
- **Preview path**: `/api`
- **Purpose**: Express 5 REST API backend

## Database Schema

Tables:
- `meals` — food items with nutritional data (name, calories, protein, carbs, fats, serving_size, category)
- `daily_logs` — one record per day (date, created_at)
- `log_entries` — meal entries linked to a daily log with quantity multiplier

## API Endpoints

- `GET /api/meals/search?q=...` — search meals by name
- `GET /api/meals` — list all meals
- `GET /api/logs/today` — get today's log with entries and totals
- `POST /api/logs/add` — add meal to today's log
- `DELETE /api/logs/remove/:entryId` — remove a log entry
- `PATCH /api/logs/update/:entryId` — update a log entry quantity
- `GET /api/logs/daily?date=...` — get log for a specific date
- `GET /api/logs/weekly` — get 7-day summary
- `POST /api/logs/cleanup` — delete logs older than 7 days
- `GET /api/summary/daily` — get today's nutrition totals

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
