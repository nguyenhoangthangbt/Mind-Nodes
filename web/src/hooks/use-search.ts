"use client";

import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { SearchResponse } from "@/types";

interface SearchParams {
  query: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  radius_meters?: number;
  source?: string;
}

export function useSearch() {
  return useMutation({
    mutationFn: (params: SearchParams) =>
      api.post<SearchResponse>("/api/v1/search", params),
  });
}
