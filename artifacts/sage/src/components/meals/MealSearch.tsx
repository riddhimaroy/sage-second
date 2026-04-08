import { useState } from "react";
import { useSearchMeals, useAddLogEntry, getGetTodayLogQueryKey } from "@workspace/api-client-react";
import { useDebounce } from "@/hooks/use-debounce";
import { Search, Plus, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import type { Meal } from "@workspace/api-client-react";

export function MealSearch() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  const [selectedMeal, setSelectedMeal] = useState<Meal | null>(null);
  const [quantity, setQuantity] = useState("1.0");

  const { data: meals, isLoading } = useSearchMeals(
    { q: debouncedQuery },
    { query: { enabled: debouncedQuery.length > 1 } }
  );

  const queryClient = useQueryClient();
  const { toast } = useToast();
  const addLogEntry = useAddLogEntry();

  const handleAddMeal = () => {
    if (!selectedMeal) return;
    
    const qtyNum = parseFloat(quantity);
    if (isNaN(qtyNum) || qtyNum <= 0) return;

    addLogEntry.mutate(
      { data: { mealId: selectedMeal.id, quantity: qtyNum } },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: getGetTodayLogQueryKey() });
          toast({
            title: "Meal logged",
            description: `Added ${qtyNum}x ${selectedMeal.name} to your daily log.`,
          });
          setSelectedMeal(null);
          setQuery("");
        },
        onError: () => {
          toast({
            title: "Error",
            description: "Failed to log meal. Please try again.",
            variant: "destructive",
          });
        }
      }
    );
  };

  return (
    <div className="space-y-4">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          placeholder="Search for meals (e.g. Oatmeal, Chicken Salad)..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-10 h-12 bg-card text-base shadow-sm"
          data-testid="input-meal-search"
        />
        {isLoading && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
          </div>
        )}
      </div>

      {debouncedQuery.length > 1 && meals && (
        <Card className="p-2 border-border shadow-sm max-h-[300px] overflow-y-auto">
          {meals.length === 0 ? (
            <div className="p-4 text-center text-muted-foreground text-sm">
              No meals found matching "{debouncedQuery}"
            </div>
          ) : (
            <div className="space-y-1">
              {meals.map((meal) => (
                <div 
                  key={meal.id} 
                  className="flex items-center justify-between p-3 rounded-lg hover:bg-secondary transition-colors group cursor-pointer"
                  onClick={() => {
                    setSelectedMeal(meal);
                    setQuantity("1.0");
                  }}
                  data-testid={`search-result-${meal.id}`}
                >
                  <div>
                    <h4 className="font-medium text-foreground">{meal.name}</h4>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {meal.calories} kcal • {meal.protein}g P • {meal.carbs}g C • {meal.fats}g F
                    </p>
                  </div>
                  <Button 
                    size="sm" 
                    variant="ghost" 
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-primary hover:text-primary hover:bg-primary/10"
                    data-testid={`button-add-${meal.id}`}
                  >
                    <Plus className="w-4 h-4 mr-1" /> Add
                  </Button>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      <Dialog open={!!selectedMeal} onOpenChange={(open) => !open && setSelectedMeal(null)}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Log Meal</DialogTitle>
          </DialogHeader>
          
          {selectedMeal && (
            <div className="py-4">
              <h3 className="font-semibold text-lg mb-1">{selectedMeal.name}</h3>
              <p className="text-sm text-muted-foreground mb-4">Standard serving: {selectedMeal.servingSize}</p>
              
              <div className="grid grid-cols-4 gap-2 mb-6">
                <div className="bg-secondary p-2 rounded text-center">
                  <div className="text-xs text-muted-foreground mb-1">Cals</div>
                  <div className="font-medium">{Math.round(selectedMeal.calories * parseFloat(quantity || "0"))}</div>
                </div>
                <div className="bg-secondary p-2 rounded text-center">
                  <div className="text-xs text-muted-foreground mb-1">Pro</div>
                  <div className="font-medium">{Math.round(selectedMeal.protein * parseFloat(quantity || "0"))}g</div>
                </div>
                <div className="bg-secondary p-2 rounded text-center">
                  <div className="text-xs text-muted-foreground mb-1">Carb</div>
                  <div className="font-medium">{Math.round(selectedMeal.carbs * parseFloat(quantity || "0"))}g</div>
                </div>
                <div className="bg-secondary p-2 rounded text-center">
                  <div className="text-xs text-muted-foreground mb-1">Fat</div>
                  <div className="font-medium">{Math.round(selectedMeal.fats * parseFloat(quantity || "0"))}g</div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <label className="text-sm font-medium w-24">Servings</label>
                <Input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="flex-1"
                  data-testid="input-serving-quantity"
                />
              </div>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setSelectedMeal(null)}>Cancel</Button>
            <Button 
              onClick={handleAddMeal} 
              disabled={addLogEntry.isPending || !quantity || parseFloat(quantity) <= 0}
              data-testid="button-confirm-add"
            >
              {addLogEntry.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Plus className="w-4 h-4 mr-2" />}
              Log Meal
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
