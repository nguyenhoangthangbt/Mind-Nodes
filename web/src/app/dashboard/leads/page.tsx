"use client";

import { useLeads, useUpdateLead, useDeleteLead } from "@/hooks/use-leads";
import { useLeadFilters } from "@/stores/leads";
import Link from "next/link";

const PIPELINE_STAGES = ["", "new", "contacted", "responded", "meeting", "proposal", "won", "lost"];
const SORT_OPTIONS = [
  { value: "created_at", label: "Date Added" },
  { value: "business_name", label: "Name" },
  { value: "rating", label: "Rating" },
  { value: "review_count", label: "Reviews" },
  { value: "pipeline_stage", label: "Stage" },
  { value: "category", label: "Category" },
];

const STAGE_COLORS: Record<string, string> = {
  new: "bg-blue-100 text-blue-700",
  contacted: "bg-yellow-100 text-yellow-700",
  responded: "bg-green-100 text-green-700",
  meeting: "bg-purple-100 text-purple-700",
  proposal: "bg-orange-100 text-orange-700",
  won: "bg-emerald-100 text-emerald-700",
  lost: "bg-red-100 text-red-700",
};

export default function LeadsPage() {
  const { data, isLoading } = useLeads();
  const { filters, setFilter, resetFilters } = useLeadFilters();
  const updateLead = useUpdateLead();
  const deleteLead = useDeleteLead();

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Leads</h1>
        <div className="flex gap-2">
          <Link
            href="/dashboard/leads/map"
            className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            Map View
          </Link>
          <a
            href="/api/v1/leads/export"
            className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            Export CSV
          </a>
          <Link
            href="/dashboard/search"
            className="rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-700"
          >
            + Find Leads
          </Link>
        </div>
      </div>

      {/* Filters bar */}
      <div className="mb-4 flex flex-wrap gap-3 rounded-lg border bg-white p-4">
        <input
          type="text"
          placeholder="Search leads..."
          value={filters.search}
          onChange={(e) => setFilter("search", e.target.value)}
          className="flex-1 min-w-[200px] rounded-md border border-gray-300 px-3 py-1.5 text-sm"
        />
        <select
          value={filters.pipeline_stage}
          onChange={(e) => setFilter("pipeline_stage", e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm"
        >
          <option value="">All Stages</option>
          {PIPELINE_STAGES.filter(Boolean).map((s) => (
            <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
          ))}
        </select>
        <select
          value={filters.source}
          onChange={(e) => setFilter("source", e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm"
        >
          <option value="">All Sources</option>
          <option value="google_places">Google Places</option>
          <option value="yelp">Yelp</option>
          <option value="manual">Manual</option>
        </select>
        <select
          value={filters.sort_by}
          onChange={(e) => setFilter("sort_by", e.target.value)}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm"
        >
          {SORT_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        <button
          onClick={() => setFilter("sort_dir", filters.sort_dir === "asc" ? "desc" : "asc")}
          className="rounded-md border border-gray-300 px-3 py-1.5 text-sm"
        >
          {filters.sort_dir === "asc" ? "Asc" : "Desc"}
        </button>
        <button onClick={resetFilters} className="text-sm text-gray-500 hover:text-gray-700">
          Reset
        </button>
      </div>

      {/* Leads table */}
      {isLoading ? (
        <p className="text-gray-500">Loading leads...</p>
      ) : (
        <>
          <div className="overflow-x-auto rounded-lg border bg-white">
            <table className="w-full text-sm">
              <thead className="border-b bg-gray-50 text-left">
                <tr>
                  <th className="px-4 py-3 font-medium text-gray-600">Business</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Category</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Rating</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Contact</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Stage</th>
                  <th className="px-4 py-3 font-medium text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {data?.items.map((lead) => (
                  <tr key={lead.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className="font-medium">{lead.business_name}</div>
                      {lead.address && (
                        <div className="text-xs text-gray-500 truncate max-w-xs">{lead.address}</div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{lead.category || "-"}</td>
                    <td className="px-4 py-3">
                      {lead.rating ? (
                        <span>{lead.rating}/5 ({lead.review_count})</span>
                      ) : "-"}
                    </td>
                    <td className="px-4 py-3">
                      <div className="text-xs">
                        {lead.phone && <div>{lead.phone}</div>}
                        {lead.email && <div className="text-primary-600">{lead.email}</div>}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <select
                        value={lead.pipeline_stage}
                        onChange={(e) =>
                          updateLead.mutate({ id: lead.id, pipeline_stage: e.target.value } as any)
                        }
                        className={`rounded-full px-2 py-0.5 text-xs font-medium border-0 ${
                          STAGE_COLORS[lead.pipeline_stage] || "bg-gray-100"
                        }`}
                      >
                        {PIPELINE_STAGES.filter(Boolean).map((s) => (
                          <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <Link
                          href={`/dashboard/leads/${lead.id}`}
                          className="text-primary-600 hover:underline text-xs"
                        >
                          View
                        </Link>
                        <button
                          onClick={() => {
                            if (confirm("Delete this lead?")) deleteLead.mutate(lead.id);
                          }}
                          className="text-red-500 hover:underline text-xs"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {data && data.total > filters.per_page && (
            <div className="mt-4 flex items-center justify-between">
              <p className="text-sm text-gray-500">
                Showing {(filters.page - 1) * filters.per_page + 1}-
                {Math.min(filters.page * filters.per_page, data.total)} of {data.total}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setFilter("page", filters.page - 1)}
                  disabled={filters.page <= 1}
                  className="rounded-md border px-3 py-1.5 text-sm disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={() => setFilter("page", filters.page + 1)}
                  disabled={filters.page * filters.per_page >= data.total}
                  className="rounded-md border px-3 py-1.5 text-sm disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
