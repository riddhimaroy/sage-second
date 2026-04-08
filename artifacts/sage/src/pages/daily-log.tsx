import { AppLayout } from "@/components/layout/AppLayout";
import { useGetTodayLog } from "@workspace/api-client-react";
import { LogEntryItem } from "@/components/meals/LogEntryItem";
import { format } from "date-fns";
import { BookOpen, AlertCircle } from "lucide-react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export default function DailyLog() {
  const { data: todayLog, isLoading, error } = useGetTodayLog();

  return (
    <AppLayout>
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground font-serif flex items-center gap-3">
              <BookOpen className="w-8 h-8 text-primary" />
              Daily Log
            </h1>
            <p className="text-muted-foreground mt-2">
              {format(new Date(), "EEEE, MMMM do, yyyy")}
            </p>
          </div>
          
          {!isLoading && todayLog && (
            <div className="bg-secondary px-4 py-2 rounded-lg text-sm font-medium">
              <span className="text-muted-foreground">Total: </span>
              <span className="text-foreground ml-1">{Math.round(todayLog.totals.calories)} kcal</span>
            </div>
          )}
        </header>

        {isLoading ? (
          <div className="space-y-4 mt-8">
            <Skeleton className="h-24 w-full rounded-xl" />
            <Skeleton className="h-24 w-full rounded-xl" />
            <Skeleton className="h-24 w-full rounded-xl" />
          </div>
        ) : error ? (
          <div className="p-8 text-center bg-destructive/10 rounded-xl border border-destructive/20 text-destructive flex flex-col items-center">
            <AlertCircle className="w-8 h-8 mb-2" />
            <p className="font-medium">Failed to load your daily log.</p>
          </div>
        ) : !todayLog || todayLog.entries.length === 0 ? (
          <div className="py-16 text-center bg-card rounded-2xl border border-border shadow-sm flex flex-col items-center justify-center">
            <div className="w-16 h-16 rounded-full bg-secondary flex items-center justify-center mb-4">
              <BookOpen className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">No meals logged yet</h3>
            <p className="text-muted-foreground mb-6 max-w-md">
              You haven't logged any meals for today. Head over to the dashboard to find and add your meals.
            </p>
            <Link href="/">
              <Button>Go to Dashboard</Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-4 mt-8">
            {todayLog.entries.map((entry) => (
              <LogEntryItem key={entry.id} entry={entry} />
            ))}
          </div>
        )}
      </div>
    </AppLayout>
  );
}
