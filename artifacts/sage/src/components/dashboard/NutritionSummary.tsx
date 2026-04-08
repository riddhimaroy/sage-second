import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { NutritionTotals } from "@workspace/api-client-react";
import type { NutritionGoals } from "@/utils/health";
import { DEFAULT_GOALS } from "@/utils/health";

interface NutritionSummaryProps {
  totals?: NutritionTotals;
  goals?: NutritionGoals;
  isLoading?: boolean;
}

export function NutritionSummary({ totals, goals, isLoading }: NutritionSummaryProps) {
  const TARGETS = goals ?? DEFAULT_GOALS;

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="h-48 rounded-xl bg-secondary animate-pulse" />
        <div className="grid grid-cols-3 gap-2">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-48 rounded-xl bg-secondary animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  const safeTotals = totals || { calories: 0, protein: 0, carbs: 0, fats: 0 };

  const calPercent = Math.min(100, Math.round((safeTotals.calories / TARGETS.calories) * 100));
  const proPercent = Math.min(100, Math.round((safeTotals.protein / TARGETS.protein) * 100));
  const carbPercent = Math.min(100, Math.round((safeTotals.carbs / TARGETS.carbs) * 100));
  const fatPercent = Math.min(100, Math.round((safeTotals.fats / TARGETS.fats) * 100));

  const remaining = Math.max(0, TARGETS.calories - safeTotals.calories);

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="md:col-span-2 border-primary/20 bg-primary/5 shadow-none">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Energy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end justify-between mb-1">
              <div className="space-y-1">
                <span className="text-4xl font-bold text-foreground font-serif tracking-tight" data-testid="text-calories-total">
                  {Math.round(safeTotals.calories)}
                </span>
                <span className="text-muted-foreground text-sm ml-2">/ {TARGETS.calories} kcal</span>
              </div>
              <span className="text-primary font-medium">{calPercent}%</span>
            </div>
            <Progress value={calPercent} className="h-3" data-testid="progress-calories" />
            <p className="text-xs text-muted-foreground mt-2">
              {remaining > 0
                ? <><span className="text-primary font-medium">{Math.round(remaining)} kcal</span> remaining today</>
                : <span className="text-amber-600 font-medium">Target reached!</span>}
            </p>
          </CardContent>
        </Card>

        <MacroCard
          title="Protein"
          current={safeTotals.protein}
          target={TARGETS.protein}
          percent={proPercent}
          unit="g"
          testId="protein"
        />
        <MacroCard
          title="Carbs"
          current={safeTotals.carbs}
          target={TARGETS.carbs}
          percent={carbPercent}
          unit="g"
          testId="carbs"
        />
        <MacroCard
          title="Fats"
          current={safeTotals.fats}
          target={TARGETS.fats}
          percent={fatPercent}
          unit="g"
          testId="fats"
        />
      </div>
    </div>
  );
}

function MacroCard({ title, current, target, percent, unit, testId }: {
  title: string;
  current: number;
  target: number;
  percent: number;
  unit: string;
  testId: string;
}) {
  return (
    <Card className="shadow-none">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-end justify-between mb-4">
          <div className="space-y-1">
            <span className="text-2xl font-bold text-foreground tracking-tight" data-testid={`text-${testId}-total`}>
              {Math.round(current)}
            </span>
            <span className="text-muted-foreground text-sm ml-1">{unit}</span>
          </div>
        </div>
        <Progress value={percent} className="h-2" data-testid={`progress-${testId}`} />
        <div className="mt-2 text-xs text-muted-foreground text-right">
          {Math.round(target)}{unit} goal
        </div>
      </CardContent>
    </Card>
  );
}
