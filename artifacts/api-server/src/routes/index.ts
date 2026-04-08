import { Router, type IRouter } from "express";
import healthRouter from "./health";
import mealsRouter from "./meals";
import logsRouter from "./logs";

const router: IRouter = Router();

// Health check
router.use(healthRouter);

// Meals: search and listing
router.use(mealsRouter);

// Logs: daily logging, weekly summaries, cleanup
router.use(logsRouter);

export default router;
