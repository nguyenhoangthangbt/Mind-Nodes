import { create } from "zustand";
import { api } from "@/lib/api";
import type { User, TokenResponse } from "@/types";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, fullName: string, company?: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  isLoading: true,

  login: async (email, password) => {
    const tokens = await api.post<TokenResponse>("/api/v1/auth/login", { email, password });
    api.setToken(tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
    const user = await api.get<User>("/api/v1/auth/me");
    set({ user });
  },

  signup: async (email, password, full_name, company) => {
    const tokens = await api.post<TokenResponse>("/api/v1/auth/signup", {
      email, password, full_name, company,
    });
    api.setToken(tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
    const user = await api.get<User>("/api/v1/auth/me");
    set({ user });
  },

  logout: () => {
    api.setToken(null);
    localStorage.removeItem("refresh_token");
    set({ user: null });
  },

  fetchUser: async () => {
    try {
      const user = await api.get<User>("/api/v1/auth/me");
      set({ user, isLoading: false });
    } catch {
      set({ user: null, isLoading: false });
    }
  },
}));
