import { create } from "zustand";

interface LeadFilters {
  search: string;
  pipeline_stage: string;
  category: string;
  source: string;
  has_email: boolean | null;
  has_phone: boolean | null;
  min_rating: number | null;
  sort_by: string;
  sort_dir: "asc" | "desc";
  page: number;
  per_page: number;
}

interface LeadFilterState {
  filters: LeadFilters;
  setFilter: <K extends keyof LeadFilters>(key: K, value: LeadFilters[K]) => void;
  resetFilters: () => void;
}

const defaultFilters: LeadFilters = {
  search: "",
  pipeline_stage: "",
  category: "",
  source: "",
  has_email: null,
  has_phone: null,
  min_rating: null,
  sort_by: "created_at",
  sort_dir: "desc",
  page: 1,
  per_page: 25,
};

export const useLeadFilters = create<LeadFilterState>((set) => ({
  filters: { ...defaultFilters },

  setFilter: (key, value) =>
    set((state) => ({
      filters: { ...state.filters, [key]: value, ...(key !== "page" ? { page: 1 } : {}) },
    })),

  resetFilters: () => set({ filters: { ...defaultFilters } }),
}));
