"use client";

import { usePipelineStats } from "@/hooks/use-leads";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { UsageResponse } from "@/types";

const STAGES = [
  { key: "new", label: "New", color: "bg-blue-100 text-blue-700" },
  { key: "contacted", label: "Contacted", color: "bg-yellow-100 text-yellow-700" },
  { key: "responded", label: "Responded", color: "bg-green-100 text-green-700" },
  { key: "meeting", label: "Meeting", color: "bg-purple-100 text-purple-700" },
  { key: "proposal", label: "Proposal", color: "bg-orange-100 text-orange-700" },
  { key: "won", label: "Won", color: "bg-emerald-100 text-emerald-700" },
  { key: "lost", label: "Lost", color: "bg-red-100 text-red-700" },
];

export default function DashboardOverview() {
  const { data: pipeline } = usePipelineStats();
  const { data: usage } = useQuery({
    queryKey: ["usage"],
    queryFn: () => api.get<UsageResponse>("/api/v1/billing/usage"),
  });

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      {/* Usage bar */}
      {usage && (
        <div className="mb-8 grid grid-cols-2 gap-4">
          <div className="rounded-lg border bg-white p-4">
            <p className="text-sm text-gray-500">Leads</p>
            <p className="text-2xl font-bold">
              {usage.leads_used}{" "}
              <span className="text-sm font-normal text-gray-400">/ {usage.leads_limit}</span>
            </p>
            <div className="mt-2 h-2 rounded-full bg-gray-100">
              <div
                className="h-full rounded-full bg-primary-500"
                style={{ width: `${Math.min((usage.leads_used / usage.leads_limit) * 100, 100)}%` }}
              />
            </div>
          </div>
          <div className="rounded-lg border bg-white p-4">
            <p className="text-sm text-gray-500">Searches this month</p>
            <p className="text-2xl font-bold">
              {usage.searches_used}{" "}
              <span className="text-sm font-normal text-gray-400">/ {usage.searches_limit}</span>
            </p>
            <div className="mt-2 h-2 rounded-full bg-gray-100">
              <div
                className="h-full rounded-full bg-primary-500"
                style={{
                  width: `${Math.min((usage.searches_used / usage.searches_limit) * 100, 100)}%`,
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Pipeline cards */}
      <h2 className="text-lg font-semibold mb-3">Pipeline</h2>
      <div className="grid grid-cols-7 gap-3">
        {STAGES.map((stage) => (
          <div key={stage.key} className="rounded-lg border bg-white p-4 text-center">
            <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${stage.color}`}>
              {stage.label}
            </span>
            <p className="mt-2 text-3xl font-bold">
              {pipeline ? (pipeline as any)[stage.key] : "-"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
