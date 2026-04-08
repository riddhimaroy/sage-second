import { pgTable, text, serial, doublePrecision } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

// Meal table — stores the nutritional information for each food item
export const mealsTable = pgTable("meals", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  calories: doublePrecision("calories").notNull(),
  protein: doublePrecision("protein").notNull(),
  carbs: doublePrecision("carbs").notNull(),
  fats: doublePrecision("fats").notNull(),
  servingSize: text("serving_size").notNull().default("100g"),
  category: text("category").notNull().default("General"),
});

export const insertMealSchema = createInsertSchema(mealsTable).omit({ id: true });
export type InsertMeal = z.infer<typeof insertMealSchema>;
export type Meal = typeof mealsTable.$inferSelect;
