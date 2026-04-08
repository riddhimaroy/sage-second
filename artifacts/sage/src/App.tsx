import { Switch, Route, Router as WouterRouter, Redirect, useLocation } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";

import Dashboard from "@/pages/dashboard";
import DailyLog from "@/pages/daily-log";
import WeeklyView from "@/pages/weekly-view";
import AuthPage from "@/pages/auth-page";
import ProfileSetup from "@/pages/profile-setup";
import BurnCalculator from "@/pages/burn-calculator";

import { AuthProvider, useAuth } from "@/contexts/AuthContext";

const queryClient = new QueryClient();

function ProtectedRoute({ component: Component }: { component: React.ComponentType }) {
  const { isLoggedIn, profileComplete } = useAuth();
  if (!isLoggedIn) return <Redirect to="/auth" />;
  if (!profileComplete) return <Redirect to="/profile" />;
  return <Component />;
}

function Router() {
  const { isLoggedIn, profileComplete, username } = useAuth();

  return (
    <Switch key={username ?? "guest"}>
      <Route path="/auth">
        {isLoggedIn && profileComplete ? <Redirect to="/" /> : <AuthPage />}
      </Route>
      <Route path="/profile">
        {!isLoggedIn ? <Redirect to="/auth" /> : <ProfileSetup />}
      </Route>
      <Route path="/">
        <ProtectedRoute component={Dashboard} />
      </Route>
      <Route path="/log">
        <ProtectedRoute component={DailyLog} />
      </Route>
      <Route path="/weekly">
        <ProtectedRoute component={WeeklyView} />
      </Route>
      <Route path="/burn">
        <ProtectedRoute component={BurnCalculator} />
      </Route>
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <AuthProvider>
          <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
            <Router />
          </WouterRouter>
          <Toaster />
        </AuthProvider>
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
