/**
 * health.ts — BMR, TDEE, and macro calculation utilities.
 * Uses the Mifflin-St Jeor equation (gold standard for calorie estimation).
 */

export interface NutritionGoals {
  calories: number;
  protein: number;
  carbs: number;
  fats: number;
}

const ACTIVITY_MULTIPLIERS: Record<string, number> = {
  sedentary: 1.2,
  light: 1.375,
  moderate: 1.55,
  active: 1.725,
};

const PROTEIN_PER_KG: Record<string, number> = {
  sedentary: 0.8,
  light: 1.0,
  moderate: 1.4,
  active: 1.8,
};

function calcBMR(weight_kg: number, height_cm: number, age: number, gender: string): number {
  const base = 10 * weight_kg + 6.25 * height_cm - 5 * age;
  return gender === "male" ? base + 5 : base - 161;
}

function calcTDEE(bmr: number, activity_level: string, goal: string): number {
  const tdee = bmr * (ACTIVITY_MULTIPLIERS[activity_level] ?? 1.2);
  if (goal === "lose") return tdee - 400;
  if (goal === "gain") return tdee + 400;
  return tdee;
}

export function computeGoals(
  weight_kg: number,
  height_cm: number,
  age: number,
  gender: string,
  activity_level: string,
  goal: string,
  custom_protein_g: number | null,
  use_custom_protein: boolean,
): NutritionGoals {
  const bmr = calcBMR(weight_kg, height_cm, age, gender);
  const calories = Math.round(calcTDEE(bmr, activity_level, goal));

  const protein = use_custom_protein && custom_protein_g
    ? Math.round(custom_protein_g)
    : Math.round(weight_kg * (PROTEIN_PER_KG[activity_level] ?? 0.8));

  const proteinCalories = protein * 4;
  const remaining = Math.max(0, calories - proteinCalories);
  const carbs = Math.round((remaining * 0.6) / 4);
  const fats = Math.round((remaining * 0.4) / 9);

  return { calories, protein, carbs, fats };
}

export const DEFAULT_GOALS: NutritionGoals = {
  calories: 2000,
  protein: 150,
  carbs: 250,
  fats: 65,
};

export interface Exercise {
  name: string;
  caloriesPer30Min: number;
  emoji: string;
}

export const EXERCISES: Exercise[] = [
  { name: "Walking",  caloriesPer30Min: 120, emoji: "🚶" },
  { name: "Running",  caloriesPer30Min: 300, emoji: "🏃" },
  { name: "Cycling",  caloriesPer30Min: 250, emoji: "🚴" },
  { name: "Skipping", caloriesPer30Min: 350, emoji: "⛹️" },
  { name: "Yoga",     caloriesPer30Min: 150, emoji: "🧘" },
];

export function calcBurnTime(extraCalories: number, caloriesPer30Min: number): number {
  if (caloriesPer30Min <= 0 || extraCalories <= 0) return 0;
  return Math.round((extraCalories / caloriesPer30Min) * 30);
}
