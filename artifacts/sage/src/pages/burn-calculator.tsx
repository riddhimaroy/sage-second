import { useState } from "react";
import { Accessibility, Activity, Bike, Flame, Footprints, StretchVertical, Timer, type LucideIcon } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EXERCISES, calcBurnTime } from "@/utils/health";
import { getGetTodayLogQueryKey, useGetTodayLog } from "@workspace/api-client-react";
import { useAuth } from "@/contexts/AuthContext";
import { computeGoals, DEFAULT_GOALS } from "@/utils/health";

function formatTime(mins: number): string {
  if (mins < 60) return `${mins} min`;
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return m === 0 ? `${h} hr` : `${h} hr ${m} min`;
}

const exerciseIcons: Record<string, LucideIcon> = {
  Walking: Footprints,
  Running: Activity,
  Cycling: Bike,
  Skipping: Accessibility,
  Yoga: StretchVertical,
};

export default function BurnCalculator() {
  const [extraInput, setExtraInput] = useState("");
  const { profile, username } = useAuth();
  const { data: todayLog } = useGetTodayLog({
    query: { queryKey: [...getGetTodayLogQueryKey(), username ?? "guest"] },
  });

  const goals =
    profile?.age && profile?.gender && profile?.height_cm && profile?.weight_kg && profile?.activity_level && profile?.goal
      ? computeGoals(
          profile.weight_kg!,
          profile.height_cm!,
          profile.age!,
          profile.gender!,
          profile.activity_level!,
          profile.goal!,
          profile.custom_protein_g,
          profile.use_custom_protein,
        )
      : DEFAULT_GOALS;

  const consumed = todayLog?.totals?.calories ?? 0;
  const autoExtra = Math.round(Math.max(0, consumed - goals.calories));

  const extra = parseFloat(extraInput) || autoExtra;
  const hasExtra = extra > 0;

  return (
    <AppLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <header>
          <div className="flex items-center gap-2 text-primary mb-1">
            <Flame className="w-6 h-6" />
            <h1 className="text-3xl font-bold font-serif tracking-tight">Burn Calories</h1>
          </div>
          <p className="text-muted-foreground">Find out how long you need to exercise to burn off extra calories.</p>
        </header>

        {/* Calorie overview */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: "Target", value: goals.calories, unit: "kcal", color: "text-primary" },
            { label: "Consumed", value: Math.round(consumed), unit: "kcal", color: "text-foreground" },
            { label: "Over Target", value: autoExtra, unit: "kcal", color: autoExtra > 0 ? "text-red-500" : "text-green-600" },
          ].map((item) => (
            <Card key={item.label} className="shadow-none text-center">
              <CardContent className="pt-4 pb-3">
                <div className={`text-2xl font-bold font-serif ${item.color}`}>{item.value}</div>
                <div className="text-xs text-muted-foreground">{item.unit}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{item.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Custom input */}
        <Card className="shadow-none">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Calories to Burn</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Label>Enter calories (leave blank to use your surplus above)</Label>
            <div className="flex gap-3 items-center max-w-xs">
              <Input
                type="number"
                min={1}
                placeholder={autoExtra > 0 ? `${autoExtra} (auto)` : "e.g. 300"}
                value={extraInput}
                onChange={(e) => setExtraInput(e.target.value)}
              />
              {extraInput && (
                <button
                  type="button"
                  className="text-sm text-muted-foreground hover:text-foreground"
                  onClick={() => setExtraInput("")}
                >
                  Clear
                </button>
              )}
            </div>
            {!hasExtra && !extraInput && (
              <p className="text-sm text-muted-foreground">
                {autoExtra === 0
                  ? "You're within your calorie target today — great job!"
                  : ""}
              </p>
            )}
          </CardContent>
        </Card>

        {/* Exercise cards */}
        {hasExtra && (
          <div className="space-y-3">
            <h2 className="font-semibold text-foreground">
              To burn <span className="text-primary">{extra} kcal</span>, try:
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {EXERCISES.map((ex) => {
                const mins = calcBurnTime(extra, ex.caloriesPer30Min);
                const Icon = exerciseIcons[ex.name] ?? Flame;
                return (
                  <Card key={ex.name} className="shadow-none hover:border-primary/40 transition-colors">
                    <CardContent className="flex items-center gap-4 py-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                        <Icon className="h-6 w-6" />
                      </div>
                      <div className="flex-1">
                        <div className="font-semibold text-foreground">{ex.name}</div>
                        <div className="text-xs text-muted-foreground">{ex.caloriesPer30Min} kcal / 30 min</div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1 text-primary font-bold">
                          <Timer className="w-4 h-4" />
                          {formatTime(mins)}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
