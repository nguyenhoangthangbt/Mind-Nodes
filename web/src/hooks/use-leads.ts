"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useLeadFilters } from "@/stores/leads";
import type { Lead, LeadListResponse, LeadAnalytics, PipelineStats } from "@/types";

export function useLeads() {
  const { filters } = useLeadFilters();

  const params = new URLSearchParams();
  params.set("page", String(filters.page));
  params.set("per_page", String(filters.per_page));
  params.set("sort_by", filters.sort_by);
  params.set("sort_dir", filters.sort_dir);
  if (filters.search) params.set("search", filters.search);
  if (filters.pipeline_stage) params.set("pipeline_stage", filters.pipeline_stage);
  if (filters.category) params.set("category", filters.category);
  if (filters.source) params.set("source", filters.source);
  if (filters.has_email !== null) params.set("has_email", String(filters.has_email));
  if (filters.has_phone !== null) params.set("has_phone", String(filters.has_phone));
  if (filters.min_rating !== null) params.set("min_rating", String(filters.min_rating));

  return useQuery({
    queryKey: ["leads", filters],
    queryFn: () => api.get<LeadListResponse>(`/api/v1/leads?${params}`),
  });
}

export function useLead(id: string) {
  return useQuery({
    queryKey: ["lead", id],
    queryFn: () => api.get<Lead>(`/api/v1/leads/${id}`),
    enabled: !!id,
  });
}

export function usePipelineStats() {
  return useQuery({
    queryKey: ["pipeline-stats"],
    queryFn: () => api.get<PipelineStats>("/api/v1/leads/pipeline"),
  });
}

export function useAnalytics() {
  return useQuery({
    queryKey: ["analytics"],
    queryFn: () => api.get<LeadAnalytics>("/api/v1/leads/analytics"),
  });
}

export function useSaveLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Lead>) => api.post<Lead>("/api/v1/leads", data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["leads"] });
      qc.invalidateQueries({ queryKey: ["pipeline-stats"] });
    },
  });
}

export function useUpdateLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: string } & Partial<Lead>) =>
      api.patch<Lead>(`/api/v1/leads/${id}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["leads"] });
      qc.invalidateQueries({ queryKey: ["pipeline-stats"] });
    },
  });
}

export function useDeleteLead() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/leads/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["leads"] });
      qc.invalidateQueries({ queryKey: ["pipeline-stats"] });
    },
  });
}
