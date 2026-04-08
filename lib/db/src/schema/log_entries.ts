import { pgTable, serial, integer, doublePrecision, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";
import { mealsTable } from "./meals";
import { dailyLogsTable } from "./daily_logs";

// LogEntry table — links a meal to a daily log with a quantity multiplier
export const logEntriesTable = pgTable("log_entries", {
  id: serial("id").primaryKey(),
  mealId: integer("meal_id").notNull().references(() => mealsTable.id, { onDelete: "cascade" }),
  dailyLogId: integer("daily_log_id").notNull().references(() => dailyLogsTable.id, { onDelete: "cascade" }),
  quantity: doublePrecision("quantity").notNull().default(1.0),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const insertLogEntrySchema = createInsertSchema(logEntriesTable).omit({ id: true, createdAt: true });
export type InsertLogEntry = z.infer<typeof insertLogEntrySchema>;
export type LogEntry = typeof logEntriesTable.$inferSelect;
