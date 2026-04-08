import { pgTable, text, serial, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

// DailyLog table — represents one log per day
export const dailyLogsTable = pgTable("daily_logs", {
  id: serial("id").primaryKey(),
  date: text("date").notNull().unique(), // YYYY-MM-DD format
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const insertDailyLogSchema = createInsertSchema(dailyLogsTable).omit({ id: true, createdAt: true });
export type InsertDailyLog = z.infer<typeof insertDailyLogSchema>;
export type DailyLog = typeof dailyLogsTable.$inferSelect;
