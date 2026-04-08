import { useState, useEffect } from "react";
import { useLocation } from "wouter";
import { User, ChevronRight, ToggleLeft, ToggleRight } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { computeGoals } from "@/utils/health";

const ACTIVITY_OPTIONS = [
  { value: "sedentary", label: "Sedentary", description: "Little to no exercise" },
  { value: "light", label: "Light", description: "1–3 days/week exercise" },
  { value: "moderate", label: "Moderate", description: "3–5 days/week exercise" },
  { value: "active", label: "Active", description: "6–7 days/week exercise" },
];

const GOAL_OPTIONS = [
  { value: "lose", label: "Lose Weight", description: "−400 kcal/day deficit" },
  { value: "maintain", label: "Maintain Weight", description: "Stay at current weight" },
  { value: "gain", label: "Gain Weight", description: "+400 kcal/day surplus" },
];

export default function ProfileSetup() {
  const { token, profile, setProfile, logout } = useAuth();
  const [, navigate] = useLocation();
  const { toast } = useToast();

  const [form, setForm] = useState({
    age: profile?.age?.toString() ?? "",
    gender: profile?.gender ?? "",
    height_cm: profile?.height_cm?.toString() ?? "",
    weight_kg: profile?.weight_kg?.toString() ?? "",
    activity_level: profile?.activity_level ?? "",
    goal: profile?.goal ?? "",
    custom_protein_g: profile?.custom_protein_g?.toString() ?? "",
    use_custom_protein: profile?.use_custom_protein ?? false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  function set(field: string, value: string | boolean) {
    setForm((f) => ({ ...f, [field]: value }));
    setErrors((e) => { const n = { ...e }; delete n[field]; return n; });
  }

  function validate(): boolean {
    const errs: Record<string, string> = {};
    const age = parseInt(form.age);
    if (!form.age || isNaN(age) || age < 1 || age > 120) errs.age = "Enter a valid age (1–120).";
    if (!form.gender) errs.gender = "Please select a gender.";
    const h = parseFloat(form.height_cm);
    if (!form.height_cm || isNaN(h) || h <= 0) errs.height_cm = "Enter a positive height in cm.";
    const w = parseFloat(form.weight_kg);
    if (!form.weight_kg || isNaN(w) || w <= 0) errs.weight_kg = "Enter a positive weight in kg.";
    if (!form.activity_level) errs.activity_level = "Please select an activity level.";
    if (!form.goal) errs.goal = "Please select a goal.";
    if (form.use_custom_protein) {
      const p = parseFloat(form.custom_protein_g);
      if (!form.custom_protein_g || isNaN(p) || p <= 0) errs.custom_protein_g = "Enter a valid protein target (g).";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);

    const body: Record<string, unknown> = {
      age: parseInt(form.age),
      gender: form.gender,
      height_cm: parseFloat(form.height_cm),
      weight_kg: parseFloat(form.weight_kg),
      activity_level: form.activity_level,
      goal: form.goal,
      use_custom_protein: form.use_custom_protein,
      custom_protein_g: form.use_custom_protein ? parseFloat(form.custom_protein_g) : null,
    };

    try {
      const res = await fetch("/api/auth/profile", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) {
        if (res.status === 401) {
          await logout();
          toast({
            title: "Session expired",
            description: "Please sign in again, then save your profile.",
            variant: "destructive",
          });
          navigate("/auth");
          return;
        }

        const firstFieldError = Object.values(data).find(
          (value) => Array.isArray(value) && typeof value[0] === "string",
        ) as string[] | undefined;
        const description =
          data.error ||
          firstFieldError?.[0] ||
          "Please check your inputs.";

        toast({
          title: "Error saving profile",
          description,
          variant: "destructive",
        });
        return;
      }
      setProfile({
        age: data.age,
        gender: data.gender,
        height_cm: data.height_cm,
        weight_kg: data.weight_kg,
        activity_level: data.activity_level,
        goal: data.goal,
        custom_protein_g: data.custom_protein_g,
        use_custom_protein: data.use_custom_protein,
      }, data.profileComplete);
      toast({ title: "Profile saved!", description: "Your goals have been calculated." });
      navigate("/");
    } catch {
      toast({ title: "Error", description: "Could not save profile.", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }

  const previewGoals =
    form.age && form.gender && form.height_cm && form.weight_kg && form.activity_level && form.goal
      ? computeGoals(
          parseFloat(form.weight_kg),
          parseFloat(form.height_cm),
          parseInt(form.age),
          form.gender,
          form.activity_level,
          form.goal,
          form.use_custom_protein ? parseFloat(form.custom_protein_g) : null,
          form.use_custom_protein,
        )
      : null;

  return (
    <AppLayout>
      <div className="max-w-2xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <header className="space-y-1">
          <div className="flex items-center gap-2 text-primary">
            <User className="w-6 h-6" />
            <h1 className="text-2xl font-bold font-serif">Your Profile</h1>
          </div>
          <p className="text-muted-foreground">Fill in your details so we can calculate your personalised daily nutrition targets.</p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Basic info */}
          <Card className="shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Basic Information</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label>Age</Label>
                <Input type="number" min={1} max={120} placeholder="e.g. 25" value={form.age} onChange={(e) => set("age", e.target.value)} />
                {errors.age && <p className="text-xs text-destructive">{errors.age}</p>}
              </div>

              <div className="space-y-1.5">
                <Label>Gender</Label>
                <div className="flex gap-2">
                  {["male", "female", "other"].map((g) => (
                    <button
                      type="button"
                      key={g}
                      onClick={() => set("gender", g)}
                      className={`flex-1 py-2 rounded-md text-sm font-medium border transition-colors ${
                        form.gender === g ? "bg-primary text-primary-foreground border-primary" : "bg-secondary border-border text-muted-foreground hover:text-foreground"
                      }`}
                    >
                      {g.charAt(0).toUpperCase() + g.slice(1)}
                    </button>
                  ))}
                </div>
                {errors.gender && <p className="text-xs text-destructive">{errors.gender}</p>}
              </div>

              <div className="space-y-1.5">
                <Label>Height (cm)</Label>
                <Input type="number" min={50} max={300} placeholder="e.g. 170" value={form.height_cm} onChange={(e) => set("height_cm", e.target.value)} />
                {errors.height_cm && <p className="text-xs text-destructive">{errors.height_cm}</p>}
              </div>

              <div className="space-y-1.5">
                <Label>Weight (kg)</Label>
                <Input type="number" min={1} max={500} step={0.1} placeholder="e.g. 70" value={form.weight_kg} onChange={(e) => set("weight_kg", e.target.value)} />
                {errors.weight_kg && <p className="text-xs text-destructive">{errors.weight_kg}</p>}
              </div>
            </CardContent>
          </Card>

          {/* Activity level */}
          <Card className="shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Activity Level</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-2">
              {ACTIVITY_OPTIONS.map((opt) => (
                <button
                  type="button"
                  key={opt.value}
                  onClick={() => set("activity_level", opt.value)}
                  className={`text-left p-3 rounded-lg border transition-colors ${
                    form.activity_level === opt.value
                      ? "bg-primary/10 border-primary text-primary"
                      : "border-border hover:bg-secondary"
                  }`}
                >
                  <div className="font-medium text-sm">{opt.label}</div>
                  <div className="text-xs text-muted-foreground mt-0.5">{opt.description}</div>
                </button>
              ))}
            </CardContent>
            {errors.activity_level && <p className="text-xs text-destructive px-6 pb-3">{errors.activity_level}</p>}
          </Card>

          {/* Goal */}
          <Card className="shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Your Goal</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-3 gap-2">
              {GOAL_OPTIONS.map((opt) => (
                <button
                  type="button"
                  key={opt.value}
                  onClick={() => set("goal", opt.value)}
                  className={`text-left p-3 rounded-lg border transition-colors ${
                    form.goal === opt.value
                      ? "bg-primary/10 border-primary text-primary"
                      : "border-border hover:bg-secondary"
                  }`}
                >
                  <div className="font-medium text-sm">{opt.label}</div>
                  <div className="text-xs text-muted-foreground mt-0.5">{opt.description}</div>
                </button>
              ))}
            </CardContent>
            {errors.goal && <p className="text-xs text-destructive px-6 pb-3">{errors.goal}</p>}
          </Card>

          {/* Protein customisation */}
          <Card className="shadow-none">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Protein Target</CardTitle>
                <button
                  type="button"
                  onClick={() => set("use_custom_protein", !form.use_custom_protein)}
                  className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  {form.use_custom_protein
                    ? <><ToggleRight className="w-5 h-5 text-primary" /> Custom</>
                    : <><ToggleLeft className="w-5 h-5" /> Recommended</>}
                </button>
              </div>
              <CardDescription>
                {form.use_custom_protein
                  ? "Enter your own protein goal."
                  : "Protein is calculated automatically based on your weight and activity."}
              </CardDescription>
            </CardHeader>
            {form.use_custom_protein && (
              <CardContent>
                <div className="space-y-1.5 max-w-xs">
                  <Label>Protein (g/day)</Label>
                  <Input
                    type="number"
                    min={1}
                    step={1}
                    placeholder="e.g. 140"
                    value={form.custom_protein_g}
                    onChange={(e) => set("custom_protein_g", e.target.value)}
                  />
                  {errors.custom_protein_g && <p className="text-xs text-destructive">{errors.custom_protein_g}</p>}
                </div>
              </CardContent>
            )}
          </Card>

          {/* Goals preview */}
          {previewGoals && (
            <Card className="shadow-none border-primary/20 bg-primary/5">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-primary uppercase tracking-wider">Your Daily Targets</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-4 gap-3 text-center">
                {[
                  { label: "Calories", value: previewGoals.calories, unit: "kcal" },
                  { label: "Protein", value: previewGoals.protein, unit: "g" },
                  { label: "Carbs", value: previewGoals.carbs, unit: "g" },
                  { label: "Fats", value: previewGoals.fats, unit: "g" },
                ].map((item) => (
                  <div key={item.label}>
                    <div className="text-xl font-bold text-foreground font-serif">{item.value}</div>
                    <div className="text-xs text-muted-foreground">{item.unit}</div>
                    <div className="text-xs text-muted-foreground">{item.label}</div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          <Button type="submit" className="w-full" size="lg" disabled={loading}>
            {loading ? "Saving..." : "Save Profile & Continue"}
            {!loading && <ChevronRight className="w-4 h-4 ml-1" />}
          </Button>
        </form>
      </div>
    </AppLayout>
  );
}
