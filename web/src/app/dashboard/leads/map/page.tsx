"use client";

import { useState } from "react";
import { useLeads } from "@/hooks/use-leads";
import { useLeadFilters } from "@/stores/leads";
import { LeadMap } from "@/components/leads/lead-map";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Lead } from "@/types";

const STAGE_COLORS: Record<string, string> = {
  new: "bg-blue-100 text-blue-700",
  contacted: "bg-yellow-100 text-yellow-700",
  responded: "bg-green-100 text-green-700",
  meeting: "bg-purple-100 text-purple-700",
  proposal: "bg-orange-100 text-orange-700",
  won: "bg-emerald-100 text-emerald-700",
  lost: "bg-red-100 text-red-700",
};

export default function LeadsMapPage() {
  const router = useRouter();
  const { data, isLoading } = useLeads();
  const { filters, setFilter } = useLeadFilters();
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Leads Map View</h1>
        <div className="flex gap-2">
          <Link
            href="/dashboard/leads"
            className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            List View
          </Link>
          <select
            value={filters.pipeline_stage}
            onChange={(e) => setFilter("pipeline_stage", e.target.value)}
            className="rounded-md border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All Stages</option>
            {Object.keys(STAGE_COLORS).map((s) => (
              <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
      </div>

      {isLoading ? (
        <p className="text-gray-500">Loading leads...</p>
      ) : (
        <div className="grid grid-cols-3 gap-4">
          {/* Map */}
          <div className="col-span-2">
            <LeadMap
              leads={data?.items || []}
              onLeadClick={(lead) => setSelectedLead(lead)}
              selectedLeadId={selectedLead?.id}
              height="600px"
            />
          </div>

          {/* Side panel: selected lead or lead list */}
          <div className="rounded-lg border bg-white overflow-auto" style={{ maxHeight: "650px" }}>
            {selectedLead ? (
              <div className="p-4">
                <button
                  onClick={() => setSelectedLead(null)}
                  className="text-xs text-gray-500 hover:text-gray-700 mb-2"
                >
                  &larr; Back to list
                </button>
                <h2 className="text-lg font-semibold">{selectedLead.business_name}</h2>
                {selectedLead.category && (
                  <p className="text-sm text-gray-500">{selectedLead.category}</p>
                )}
                <span className={`inline-block mt-2 rounded-full px-2 py-0.5 text-xs font-medium ${STAGE_COLORS[selectedLead.pipeline_stage]}`}>
                  {selectedLead.pipeline_stage}
                </span>
                <div className="mt-4 space-y-2 text-sm">
                  {selectedLead.address && <p>{selectedLead.address}</p>}
                  {selectedLead.phone && <p>Phone: {selectedLead.phone}</p>}
                  {selectedLead.email && <p>Email: {selectedLead.email}</p>}
                  {selectedLead.rating && <p>Rating: {selectedLead.rating}/5</p>}
                </div>
                <button
                  onClick={() => router.push(`/dashboard/leads/${selectedLead.id}`)}
                  className="mt-4 w-full rounded-md bg-primary-600 py-2 text-sm text-white hover:bg-primary-700"
                >
                  View Full Details
                </button>
              </div>
            ) : (
              <div className="p-3">
                <p className="text-sm text-gray-500 mb-2">
                  {data?.total || 0} leads — click a pin on the map
                </p>
                <div className="space-y-1">
                  {data?.items
                    .filter((l) => l.latitude && l.longitude)
                    .map((lead) => (
                      <div
                        key={lead.id}
                        onClick={() => setSelectedLead(lead)}
                        className="flex items-center gap-2 p-2 rounded cursor-pointer hover:bg-gray-50"
                      >
                        <div
                          className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                          style={{
                            backgroundColor:
                              STAGE_COLORS[lead.pipeline_stage]?.includes("blue") ? "#3b82f6"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("yellow") ? "#eab308"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("green") ? "#22c55e"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("purple") ? "#a855f7"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("orange") ? "#f97316"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("emerald") ? "#10b981"
                              : STAGE_COLORS[lead.pipeline_stage]?.includes("red") ? "#ef4444"
                              : "#6b7280",
                          }}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{lead.business_name}</p>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
