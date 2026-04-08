import React, { createContext, useContext, useState, useEffect, useCallback } from "react";

export interface UserProfile {
  age: number | null;
  gender: string | null;
  height_cm: number | null;
  weight_kg: number | null;
  activity_level: string | null;
  goal: string | null;
  custom_protein_g: number | null;
  use_custom_protein: boolean;
}

interface AuthState {
  token: string | null;
  username: string | null;
  profile: UserProfile | null;
  profileComplete: boolean;
}

interface AuthContextValue extends AuthState {
  isLoggedIn: boolean;
  login: (token: string, username: string, profileComplete: boolean) => void;
  logout: () => Promise<void>;
  setProfile: (profile: UserProfile, complete: boolean) => void;
  refetchProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const TOKEN_KEY = "sage_token";
const USERNAME_KEY = "sage_username";
const PROFILE_KEY = "sage_profile";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    const username = localStorage.getItem(USERNAME_KEY);
    const raw = localStorage.getItem(PROFILE_KEY);
    const profile = raw ? (JSON.parse(raw) as UserProfile) : null;
    return { token, username, profile, profileComplete: false };
  });

  const refetchProfile = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return;
    try {
      const res = await fetch("/api/auth/profile", {
        headers: { Authorization: `Token ${token}` },
      });
      if (!res.ok) return;
      const data = await res.json();
      const profile: UserProfile = {
        age: data.age,
        gender: data.gender,
        height_cm: data.height_cm,
        weight_kg: data.weight_kg,
        activity_level: data.activity_level,
        goal: data.goal,
        custom_protein_g: data.custom_protein_g,
        use_custom_protein: data.use_custom_protein,
      };
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
      setState((s) => ({ ...s, profile, profileComplete: data.profileComplete }));
    } catch {
      // silent
    }
  }, []);

  useEffect(() => {
    if (state.token) refetchProfile();
  }, []);

  const login = useCallback((token: string, username: string, profileComplete: boolean) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USERNAME_KEY, username);
    setState({ token, username, profile: null, profileComplete });
  }, []);

  const logout = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      try {
        await fetch("/api/auth/logout", {
          method: "POST",
          headers: { Authorization: `Token ${token}` },
        });
      } catch {}
    }
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USERNAME_KEY);
    localStorage.removeItem(PROFILE_KEY);
    setState({ token: null, username: null, profile: null, profileComplete: false });
  }, []);

  const setProfile = useCallback((profile: UserProfile, complete: boolean) => {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
    setState((s) => ({ ...s, profile, profileComplete: complete }));
  }, []);

  return (
    <AuthContext.Provider
      value={{
        ...state,
        isLoggedIn: !!state.token,
        login,
        logout,
        setProfile,
        refetchProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
