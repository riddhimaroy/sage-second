import { AppLayout } from "@/components/layout/AppLayout";
import { NutritionSummary } from "@/components/dashboard/NutritionSummary";
import { MealSearch } from "@/components/meals/MealSearch";
import { getGetTodayLogQueryKey, useGetTodayLog } from "@workspace/api-client-react";
import { format } from "date-fns";
import { Link } from "wouter";
import { ArrowRight, UtensilsCrossed } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { computeGoals, DEFAULT_GOALS } from "@/utils/health";

export default function Dashboard() {
  const { profile, username } = useAuth();
  const { data: todayLog, isLoading } = useGetTodayLog({
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

  return (
    <AppLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <header>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground font-serif">
            {format(new Date(), "EEEE, MMMM do")}
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">
            Stay grounded. Nourish yourself.
          </p>
        </header>

        <section>
          <NutritionSummary totals={todayLog?.totals} goals={goals} isLoading={isLoading} />
        </section>

        <section className="bg-card rounded-2xl p-6 shadow-sm border border-border">
          <h2 className="text-xl font-semibold mb-4 text-foreground flex items-center gap-2">
            <UtensilsCrossed className="w-5 h-5 text-primary" />
            Log a Meal
          </h2>
          <MealSearch />
        </section>

        {!isLoading && todayLog && todayLog.entries.length > 0 && (
          <section className="flex justify-between items-center bg-primary/5 rounded-xl p-4 border border-primary/10">
            <div>
              <h3 className="font-medium text-foreground">You've logged {todayLog.entries.length} items today.</h3>
            </div>
            <Link
              href="/log"
              className="flex items-center text-sm font-medium text-primary hover:text-primary/80 transition-colors"
            >
              View Daily Log <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </section>
        )}
      </div>
    </AppLayout>
  );
}
