import { Router, type IRouter } from "express";
import { ilike } from "drizzle-orm";
import { db, mealsTable } from "@workspace/db";
import {
  SearchMealsQueryParams,
  SearchMealsResponse,
  ListMealsResponse,
} from "@workspace/api-zod";

const router: IRouter = Router();

/**
 * GET /meals/search?q=<query>
 * Search meals by name (case-insensitive partial match)
 */
router.get("/meals/search", async (req, res): Promise<void> => {
  const params = SearchMealsQueryParams.safeParse(req.query);
  if (!params.success) {
    res.status(400).json({ error: params.error.message });
    return;
  }

  const { q } = params.data;
  const meals = await db
    .select()
    .from(mealsTable)
    .where(ilike(mealsTable.name, `%${q}%`))
    .limit(20);

  res.json(SearchMealsResponse.parse(meals));
});

/**
 * GET /meals
 * List all available meals
 */
router.get("/meals", async (_req, res): Promise<void> => {
  const meals = await db.select().from(mealsTable).orderBy(mealsTable.name);
  res.json(ListMealsResponse.parse(meals));
});

export default router;
