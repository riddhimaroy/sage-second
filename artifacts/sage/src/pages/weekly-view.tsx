import { AppLayout } from "@/components/layout/AppLayout";
import { useGetWeeklyLogs, useCleanupOldLogs, getGetWeeklyLogsQueryKey } from "@workspace/api-client-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { format, parseISO } from "date-fns";
import { Calendar, Trash2, TrendingUp, AlertCircle, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useQueryClient } from "@tanstack/react-query";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";

export default function WeeklyView() {
  const { data: weeklyData, isLoading, error } = useGetWeeklyLogs();
  const cleanupMutation = useCleanupOldLogs();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [isConfirmCleanup, setIsConfirmCleanup] = useState(false);

  const handleCleanup = () => {
    cleanupMutation.mutate(undefined, {
      onSuccess: (data) => {
        toast({
          title: "Cleanup Complete",
          description: data.message,
        });
        queryClient.invalidateQueries({ queryKey: getGetWeeklyLogsQueryKey() });
        setIsConfirmCleanup(false);
      },
      onError: () => {
        toast({
          title: "Cleanup Failed",
          description: "Could not clean up old logs.",
          variant: "destructive"
        });
        setIsConfirmCleanup(false);
      }
    });
  };

  const formatChartData = () => {
    if (!weeklyData || !weeklyData.days) return [];
    
    return weeklyData.days.map(day => ({
      ...day,
      displayDate: format(parseISO(day.date), "EEE"),
      fullDate: format(parseISO(day.date), "MMM d")
    })).reverse(); // ensure chronological order if API returns descending
  };

  const chartData = formatChartData();

  return (
    <AppLayout>
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground font-serif flex items-center gap-3">
              <Calendar className="w-8 h-8 text-primary" />
              Weekly Summary
            </h1>
            <p className="text-muted-foreground mt-2">
              Your nutrition trends over the last 7 days.
            </p>
          </div>
          
          <Button 
            variant="outline" 
            className="text-muted-foreground hover:text-destructive hover:bg-destructive/10"
            onClick={() => setIsConfirmCleanup(true)}
            data-testid="button-cleanup"
          >
            <Trash2 className="w-4 h-4 mr-2" /> Clean Old Logs
          </Button>
        </header>

        {isLoading ? (
          <div className="space-y-6 mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Skeleton className="h-32 rounded-xl" />
              <Skeleton className="h-32 rounded-xl" />
            </div>
            <Skeleton className="h-[400px] rounded-xl" />
          </div>
        ) : error ? (
          <div className="p-8 text-center bg-destructive/10 rounded-xl border border-destructive/20 text-destructive flex flex-col items-center">
            <AlertCircle className="w-8 h-8 mb-2" />
            <p className="font-medium">Failed to load weekly summary.</p>
          </div>
        ) : !weeklyData ? null : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="bg-card shadow-sm border-border">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" /> Average Intake
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-bold font-serif tracking-tight">{Math.round(weeklyData.averageCalories)}</span>
                    <span className="text-muted-foreground font-medium">kcal/day</span>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card shadow-sm border-border">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <Calendar className="w-4 h-4" /> Tracking Streak
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-bold font-serif tracking-tight">{weeklyData.totalDaysLogged}</span>
                    <span className="text-muted-foreground font-medium">days out of 7</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="bg-card shadow-sm border-border">
              <CardHeader>
                <CardTitle>7-Day Trend</CardTitle>
                <CardDescription>Calorie intake over the past week</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[350px] w-full mt-4">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                      <XAxis 
                        dataKey="displayDate" 
                        axisLine={false} 
                        tickLine={false}
                        tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                        dy={10}
                      />
                      <YAxis 
                        axisLine={false} 
                        tickLine={false}
                        tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                      />
                      <Tooltip 
                        cursor={{ fill: 'hsl(var(--secondary))' }}
                        content={({ active, payload }) => {
                          if (active && payload && payload.length) {
                            const data = payload[0].payload;
                            return (
                              <div className="bg-popover text-popover-foreground border border-border shadow-md p-3 rounded-lg text-sm">
                                <p className="font-semibold mb-1">{data.fullDate}</p>
                                <p><span className="font-medium">Calories:</span> {Math.round(data.calories)} kcal</p>
                                <div className="mt-2 pt-2 border-t border-border flex gap-3 text-xs text-muted-foreground">
                                  <span>{Math.round(data.protein)}g P</span>
                                  <span>{Math.round(data.carbs)}g C</span>
                                  <span>{Math.round(data.fats)}g F</span>
                                </div>
                              </div>
                            );
                          }
                          return null;
                        }}
                      />
                      <Bar dataKey="calories" radius={[4, 4, 0, 0]} maxBarSize={50}>
                        {chartData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={
                              entry.date === weeklyData.highestCalorieDay 
                                ? 'hsl(var(--destructive))' 
                                : entry.date === weeklyData.lowestCalorieDay && entry.calories > 0
                                  ? 'hsl(var(--primary))' 
                                  : 'hsl(var(--primary) / 0.5)'
                            } 
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                
                <div className="flex flex-wrap items-center justify-center gap-6 mt-6 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-primary/50"></div>
                    <span>Normal day</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-destructive"></div>
                    <span>Highest intake</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-primary"></div>
                    <span>Lowest intake</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      <Dialog open={isConfirmCleanup} onOpenChange={setIsConfirmCleanup}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Clean up old logs?</DialogTitle>
            <DialogDescription>
              This will permanently delete all daily logs older than 7 days. This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setIsConfirmCleanup(false)}>Cancel</Button>
            <Button 
              variant="destructive" 
              onClick={handleCleanup}
              disabled={cleanupMutation.isPending}
            >
              {cleanupMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Trash2 className="w-4 h-4 mr-2" />}
              Delete Old Logs
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppLayout>
  );
}
