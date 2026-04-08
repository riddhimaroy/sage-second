import { useState } from "react";
import { useLocation } from "wouter";
import { Leaf, Eye, EyeOff } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

type Mode = "login" | "register";

export default function AuthPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<{ username?: string; password?: string; general?: string }>({});
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const [, navigate] = useLocation();
  const { toast } = useToast();

  function validate(): boolean {
    const errs: typeof errors = {};
    if (username.trim().length < 3) {
      errs.username = "Username must be at least 3 characters.";
    } else if (mode === "register" && !/^[a-zA-Z0-9_-]+$/.test(username.trim())) {
      errs.username = "Username may only contain letters, numbers, _ and -.";
    }
    if (password.length < 6) {
      errs.password = "Password must be at least 6 characters.";
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    setErrors({});

    try {
      const endpoint = mode === "login" ? "/api/auth/login" : "/api/auth/register";
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username.trim(), password }),
      });

      const data = await res.json();

      if (!res.ok) {
        const msg = data.error || data.username?.[0] || data.password?.[0] || "Something went wrong.";
        setErrors({ general: msg });
        return;
      }

      login(data.token, data.username, data.profileComplete);
      toast({ title: mode === "login" ? "Welcome back!" : "Account created!", description: `Logged in as ${data.username}` });

      if (!data.profileComplete) {
        navigate("/profile");
      } else {
        navigate("/");
      }
    } catch {
      setErrors({ general: "Could not connect to server. Please try again." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-[100dvh] bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 text-primary">
            <Leaf className="w-8 h-8" />
            <span className="text-3xl font-bold tracking-tight font-serif">SAGE</span>
          </div>
          <p className="text-muted-foreground">Smart Nutrition Tracker</p>
        </div>

        <Card className="shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-xl">
              {mode === "login" ? "Sign In" : "Create Account"}
            </CardTitle>
            <CardDescription>
              {mode === "login"
                ? "Welcome back. Enter your credentials to continue."
                : "Start tracking your nutrition journey."}
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. john_doe"
                  autoComplete="username"
                  disabled={loading}
                />
                {errors.username && <p className="text-sm text-destructive">{errors.username}</p>}
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="At least 6 characters"
                    autoComplete={mode === "login" ? "current-password" : "new-password"}
                    disabled={loading}
                    className="pr-10"
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    onClick={() => setShowPassword((v) => !v)}
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && <p className="text-sm text-destructive">{errors.password}</p>}
              </div>

              {errors.general && (
                <div className="text-sm text-destructive bg-destructive/10 rounded-md px-3 py-2">
                  {errors.general}
                </div>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Please wait..." : mode === "login" ? "Sign In" : "Create Account"}
              </Button>
            </form>

            <div className="mt-4 text-center text-sm text-muted-foreground">
              {mode === "login" ? (
                <>
                  No account?{" "}
                  <button
                    className="text-primary hover:underline font-medium"
                    onClick={() => { setMode("register"); setErrors({}); }}
                  >
                    Register
                  </button>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <button
                    className="text-primary hover:underline font-medium"
                    onClick={() => { setMode("login"); setErrors({}); }}
                  >
                    Sign In
                  </button>
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
