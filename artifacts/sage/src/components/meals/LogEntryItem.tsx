import { useState } from "react";
import { useUpdateLogEntry, useRemoveLogEntry, getGetTodayLogQueryKey } from "@workspace/api-client-react";
import { useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Pencil, Trash2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from "@/components/ui/dialog";
import type { LogEntry } from "@workspace/api-client-react";

interface LogEntryItemProps {
  entry: LogEntry;
}

export function LogEntryItem({ entry }: LogEntryItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editQuantity, setEditQuantity] = useState(entry.quantity.toString());
  const [isConfirmDelete, setIsConfirmDelete] = useState(false);

  const updateEntry = useUpdateLogEntry();
  const removeEntry = useRemoveLogEntry();
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const handleUpdate = () => {
    const qty = parseFloat(editQuantity);
    if (isNaN(qty) || qty <= 0) return;

    updateEntry.mutate(
      { entryId: entry.id, data: { quantity: qty } },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: getGetTodayLogQueryKey() });
          setIsEditing(false);
          toast({
            title: "Updated",
            description: "Meal quantity updated.",
          });
        },
        onError: () => {
          toast({
            title: "Error",
            description: "Failed to update. Please try again.",
            variant: "destructive",
          });
        }
      }
    );
  };

  const handleDelete = () => {
    removeEntry.mutate(
      { entryId: entry.id },
      {
        onSuccess: () => {
          queryClient.invalidateQueries({ queryKey: getGetTodayLogQueryKey() });
          setIsConfirmDelete(false);
          toast({
            title: "Removed",
            description: "Meal removed from log.",
          });
        },
        onError: () => {
          toast({
            title: "Error",
            description: "Failed to remove. Please try again.",
            variant: "destructive",
          });
        }
      }
    );
  };

  return (
    <>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-card border border-border rounded-xl shadow-sm gap-4 transition-all hover:border-primary/30" data-testid={`log-entry-${entry.id}`}>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-semibold text-foreground text-lg">{entry.meal.name}</h4>
            <span className="text-xs px-2 py-0.5 bg-secondary text-secondary-foreground rounded-full font-medium">
              {entry.meal.category}
            </span>
          </div>
          <div className="text-sm text-muted-foreground flex flex-wrap items-center gap-x-3 gap-y-1">
            <span>{entry.quantity} × {entry.meal.servingSize}</span>
            <span className="hidden sm:inline text-border">•</span>
            <span className="text-foreground font-medium">{Math.round(entry.meal.calories * entry.quantity)} kcal</span>
            <span className="text-border">•</span>
            <span>{Math.round(entry.meal.protein * entry.quantity)}g P</span>
            <span className="text-border">•</span>
            <span>{Math.round(entry.meal.carbs * entry.quantity)}g C</span>
            <span className="text-border">•</span>
            <span>{Math.round(entry.meal.fats * entry.quantity)}g F</span>
          </div>
        </div>

        <div className="flex items-center gap-2 self-end sm:self-auto">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => {
              setEditQuantity(entry.quantity.toString());
              setIsEditing(true);
            }}
            data-testid={`button-edit-entry-${entry.id}`}
            className="h-8 text-muted-foreground hover:text-foreground"
          >
            <Pencil className="w-3.5 h-3.5 mr-1.5" /> Edit
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => setIsConfirmDelete(true)}
            data-testid={`button-remove-entry-${entry.id}`}
            className="h-8 text-destructive hover:bg-destructive/10 hover:text-destructive border-transparent hover:border-destructive/20"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>

      <Dialog open={isEditing} onOpenChange={setIsEditing}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle>Edit Quantity</DialogTitle>
          </DialogHeader>
          <div className="py-4 space-y-4">
            <div>
              <p className="font-medium text-foreground mb-1">{entry.meal.name}</p>
              <p className="text-sm text-muted-foreground">Original serving: {entry.meal.servingSize}</p>
            </div>
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium w-20">Servings</label>
              <Input
                type="number"
                min="0.1"
                step="0.1"
                value={editQuantity}
                onChange={(e) => setEditQuantity(e.target.value)}
                data-testid={`input-edit-quantity-${entry.id}`}
                className="flex-1"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
            <Button 
              onClick={handleUpdate} 
              disabled={updateEntry.isPending || !editQuantity || parseFloat(editQuantity) <= 0}
              data-testid={`button-save-edit-${entry.id}`}
            >
              {updateEntry.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
              Save Changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isConfirmDelete} onOpenChange={setIsConfirmDelete}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle>Remove entry?</DialogTitle>
            <DialogDescription>
              Are you sure you want to remove {entry.meal.name} from your log? This will update your daily totals.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setIsConfirmDelete(false)}>Cancel</Button>
            <Button 
              variant="destructive" 
              onClick={handleDelete} 
              disabled={removeEntry.isPending}
              data-testid={`button-confirm-remove-${entry.id}`}
            >
              {removeEntry.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Trash2 className="w-4 h-4 mr-2" />}
              Remove
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
