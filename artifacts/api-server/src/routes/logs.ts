import { Router, type IRouter } from "express";
import { eq, and, lt } from "drizzle-orm";
import { db, mealsTable, dailyLogsTable, logEntriesTable } from "@workspace/db";
import {
  AddLogEntryBody,
  RemoveLogEntryParams,
  UpdateLogEntryParams,
  UpdateLogEntryBody,
  UpdateLogEntryResponse,
  GetDailyLogsQueryParams,
  GetDailyLogsResponse,
  GetTodayLogResponse,
  GetWeeklyLogsResponse,
  CleanupOldLogsResponse,
  GetDailySummaryResponse,
} from "@workspace/api-zod";

const router: IRouter = Router();

/** Helper: get today's date string in YYYY-MM-DD */
function todayStr(): string {
  return new Date().toISOString().split("T")[0];
}

/** Helper: get or create a daily log for a given date */
async function getOrCreateDailyLog(date: string): Promise<{ id: number; date: string }> {
  const existing = await db.select().from(dailyLogsTable).where(eq(dailyLogsTable.date, date));
  if (existing.length > 0) return existing[0];
  const [created] = await db.insert(dailyLogsTable).values({ date }).returning();
  return created;
}

/** Helper: compute nutrition totals from entries */
function computeTotals(entries: Array<{ quantity: number; meal: { calories: number; protein: number; carbs: number; fats: number } }>) {
  return entries.reduce(
    (acc, entry) => ({
      calories: acc.calories + entry.meal.calories * entry.quantity,
      protein: acc.protein + entry.meal.protein * entry.quantity,
      carbs: acc.carbs + entry.meal.carbs * entry.quantity,
      fats: acc.fats + entry.meal.fats * entry.quantity,
    }),
    { calories: 0, protein: 0, carbs: 0, fats: 0 },
  );
}

/** Helper: fetch entries with meals for a daily log */
async function getEntriesWithMeals(dailyLogId: number) {
  const entries = await db
    .select({
      id: logEntriesTable.id,
      mealId: logEntriesTable.mealId,
      dailyLogId: logEntriesTable.dailyLogId,
      quantity: logEntriesTable.quantity,
      meal: mealsTable,
    })
    .from(logEntriesTable)
    .innerJoin(mealsTable, eq(logEntriesTable.mealId, mealsTable.id))
    .where(eq(logEntriesTable.dailyLogId, dailyLogId))
    .orderBy(logEntriesTable.id);
  return entries;
}

/**
 * GET /logs/today
 * Returns today's food log with all entries and computed totals
 */
router.get("/logs/today", async (req, res): Promise<void> => {
  const today = todayStr();
  const dailyLog = await getOrCreateDailyLog(today);
  const entries = await getEntriesWithMeals(dailyLog.id);
  const totals = computeTotals(entries);

  const response = GetTodayLogResponse.parse({
    id: dailyLog.id,
    date: dailyLog.date,
    entries,
    totals,
  });
  res.json(response);
});

/**
 * POST /logs/add
 * Add a meal entry to today's log
 */
router.post("/logs/add", async (req, res): Promise<void> => {
  const parsed = AddLogEntryBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: parsed.error.message });
    return;
  }

  const { mealId, quantity } = parsed.data;

  // Verify meal exists
  const [meal] = await db.select().from(mealsTable).where(eq(mealsTable.id, mealId));
  if (!meal) {
    res.status(404).json({ error: "Meal not found" });
    return;
  }

  const today = todayStr();
  const dailyLog = await getOrCreateDailyLog(today);

  const [entry] = await db
    .insert(logEntriesTable)
    .values({ mealId, dailyLogId: dailyLog.id, quantity })
    .returning();

  res.status(201).json({
    id: entry.id,
    mealId: entry.mealId,
    dailyLogId: entry.dailyLogId,
    quantity: entry.quantity,
    meal,
  });
});

/**
 * DELETE /logs/remove/:entryId
 * Remove a log entry by ID
 */
router.delete("/logs/remove/:entryId", async (req, res): Promise<void> => {
  const params = RemoveLogEntryParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const [deleted] = await db
    .delete(logEntriesTable)
    .where(eq(logEntriesTable.id, params.data.entryId))
    .returning();

  if (!deleted) {
    res.status(404).json({ error: "Log entry not found" });
    return;
  }

  res.sendStatus(204);
});

/**
 * PATCH /logs/update/:entryId
 * Update the quantity of a log entry
 */
router.patch("/logs/update/:entryId", async (req, res): Promise<void> => {
  const params = UpdateLogEntryParams.safeParse(req.params);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const body = UpdateLogEntryBody.safeParse(req.body);
  if (!body.success) {
    res.status(400).json({ error: body.error.message });
    return;
  }

  const [updated] = await db
    .update(logEntriesTable)
    .set({ quantity: body.data.quantity })
    .where(eq(logEntriesTable.id, params.data.entryId))
    .returning();

  if (!updated) {
    res.status(404).json({ error: "Log entry not found" });
    return;
  }

  // Fetch the meal for the response
  const [meal] = await db.select().from(mealsTable).where(eq(mealsTable.id, updated.mealId));

  res.json(
    UpdateLogEntryResponse.parse({
      id: updated.id,
      mealId: updated.mealId,
      dailyLogId: updated.dailyLogId,
      quantity: updated.quantity,
      meal,
    }),
  );
});

/**
 * GET /logs/daily?date=YYYY-MM-DD
 * Get the log for a specific date (defaults to today)
 */
router.get("/logs/daily", async (req, res): Promise<void> => {
  const queryParams = GetDailyLogsQueryParams.safeParse(req.query);
  if (!queryParams.success) {
    res.status(400).json({ error: queryParams.error.message });
    return;
  }

  const date = queryParams.data.date ?? todayStr();
  const dailyLog = await getOrCreateDailyLog(date);
  const entries = await getEntriesWithMeals(dailyLog.id);
  const totals = computeTotals(entries);

  res.json(
    GetDailyLogsResponse.parse({
      id: dailyLog.id,
      date: dailyLog.date,
      entries,
      totals,
    }),
  );
});

/**
 * GET /logs/weekly
 * Aggregate the last 7 days of logs with per-day totals
 */
router.get("/logs/weekly", async (req, res): Promise<void> => {
  // Build last 7 days array
  const days: string[] = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push(d.toISOString().split("T")[0]);
  }

  const dayAggregates = await Promise.all(
    days.map(async (date) => {
      const logs = await db.select().from(dailyLogsTable).where(eq(dailyLogsTable.date, date));
      if (logs.length === 0) {
        return { date, calories: 0, protein: 0, carbs: 0, fats: 0, entryCount: 0 };
      }

      const entries = await getEntriesWithMeals(logs[0].id);
      const totals = computeTotals(entries);
      return { date, ...totals, entryCount: entries.length };
    }),
  );

  // Find highest/lowest calorie days (only among days with entries)
  const daysWithEntries = dayAggregates.filter((d) => d.entryCount > 0);
  let highestCalorieDay: string | null = null;
  let lowestCalorieDay: string | null = null;

  if (daysWithEntries.length > 0) {
    const sorted = [...daysWithEntries].sort((a, b) => b.calories - a.calories);
    highestCalorieDay = sorted[0].date;
    lowestCalorieDay = sorted[sorted.length - 1].date;
    // Only assign lowestCalorieDay if it's different from highest
    if (lowestCalorieDay === highestCalorieDay && sorted.length === 1) {
      lowestCalorieDay = null;
    }
  }

  const averageCalories =
    daysWithEntries.length > 0
      ? daysWithEntries.reduce((sum, d) => sum + d.calories, 0) / daysWithEntries.length
      : 0;

  res.json(
    GetWeeklyLogsResponse.parse({
      days: dayAggregates,
      highestCalorieDay,
      lowestCalorieDay,
      averageCalories,
      totalDaysLogged: daysWithEntries.length,
    }),
  );
});

/**
 * POST /logs/cleanup
 * Delete all daily logs older than 7 days (cascade deletes entries)
 */
router.post("/logs/cleanup", async (req, res): Promise<void> => {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  const cutoffStr = cutoff.toISOString().split("T")[0];

  const deleted = await db
    .delete(dailyLogsTable)
    .where(lt(dailyLogsTable.date, cutoffStr))
    .returning();

  res.json(
    CleanupOldLogsResponse.parse({
      deletedLogs: deleted.length,
      message: `Deleted ${deleted.length} log(s) older than 7 days`,
    }),
  );
});

/**
 * GET /summary/daily
 * Get today's nutrition totals
 */
router.get("/summary/daily", async (req, res): Promise<void> => {
  const today = todayStr();
  const logs = await db.select().from(dailyLogsTable).where(eq(dailyLogsTable.date, today));

  if (logs.length === 0) {
    res.json(GetDailySummaryResponse.parse({ calories: 0, protein: 0, carbs: 0, fats: 0 }));
    return;
  }

  const entries = await getEntriesWithMeals(logs[0].id);
  const totals = computeTotals(entries);

  res.json(GetDailySummaryResponse.parse(totals));
});

export default router;
