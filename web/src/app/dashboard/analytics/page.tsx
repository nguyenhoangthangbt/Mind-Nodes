"use client";

import { useAnalytics } from "@/hooks/use-leads";

const STAGE_COLORS: Record<string, string> = {
  new: "bg-blue-500",
  contacted: "bg-yellow-500",
  responded: "bg-green-500",
  meeting: "bg-purple-500",
  proposal: "bg-orange-500",
  won: "bg-emerald-500",
  lost: "bg-red-500",
};

export default function AnalyticsPage() {
  const { data, isLoading } = useAnalytics();

  if (isLoading) return <p className="text-gray-500">Loading analytics...</p>;
  if (!data) return <p className="text-gray-500">No data yet. Start by searching and saving leads.</p>;

  const pipelineTotal = Object.values(data.pipeline).reduce((a, b) => a + b, 0);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Analytics</h1>

      {/* Summary cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="rounded-lg border bg-white p-4">
          <p className="text-sm text-gray-500">Total Leads</p>
          <p className="text-3xl font-bold">{data.total_leads}</p>
        </div>
        <div className="rounded-lg border bg-white p-4">
          <p className="text-sm text-gray-500">Avg Rating</p>
          <p className="text-3xl font-bold">{data.avg_rating ? `${data.avg_rating}/5` : "N/A"}</p>
        </div>
        <div className="rounded-lg border bg-white p-4">
          <p className="text-sm text-gray-500">Conversion Rate</p>
          <p className="text-3xl font-bold">{data.conversion_rate}%</p>
        </div>
        <div className="rounded-lg border bg-white p-4">
          <p className="text-sm text-gray-500">With Contact Info</p>
          <p className="text-3xl font-bold">
            {data.total_leads > 0
              ? Math.round(((data.with_email_count + data.with_phone_count) / (data.total_leads * 2)) * 100)
              : 0}
            %
          </p>
        </div>
      </div>

      {/* Pipeline funnel */}
      <div className="mb-8 rounded-lg border bg-white p-6">
        <h2 className="text-lg font-semibold mb-4">Pipeline Funnel</h2>
        <div className="space-y-2">
          {Object.entries(data.pipeline).map(([stage, count]) => (
            <div key={stage} className="flex items-center gap-3">
              <span className="w-24 text-sm text-gray-600 capitalize">{stage}</span>
              <div className="flex-1 h-6 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${STAGE_COLORS[stage] || "bg-gray-400"} rounded-full transition-all`}
                  style={{ width: pipelineTotal > 0 ? `${(count / pipelineTotal) * 100}%` : "0%" }}
                />
              </div>
              <span className="w-12 text-right text-sm font-medium">{count}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* By source */}
        <div className="rounded-lg border bg-white p-6">
          <h2 className="text-lg font-semibold mb-4">Leads by Source</h2>
          {data.by_source.map((s) => (
            <div key={s.source} className="flex justify-between py-1.5 border-b last:border-0">
              <span className="text-sm capitalize">{s.source.replace("_", " ")}</span>
              <span className="text-sm font-medium">{s.count}</span>
            </div>
          ))}
        </div>

        {/* By category */}
        <div className="rounded-lg border bg-white p-6">
          <h2 className="text-lg font-semibold mb-4">Top Categories</h2>
          {data.by_category.map((c) => (
            <div key={c.category} className="flex justify-between py-1.5 border-b last:border-0">
              <span className="text-sm">{c.category}</span>
              <span className="text-sm font-medium">{c.count}</span>
            </div>
          ))}
        </div>

        {/* Rating distribution */}
        <div className="rounded-lg border bg-white p-6">
          <h2 className="text-lg font-semibold mb-4">Rating Distribution</h2>
          {data.rating_distribution.map((r) => (
            <div key={r.bucket} className="flex items-center gap-3 py-1.5">
              <span className="w-12 text-sm text-gray-600">{r.bucket}</span>
              <div className="flex-1 h-4 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-amber-400 rounded-full"
                  style={{
                    width: data.total_leads > 0 ? `${(r.count / data.total_leads) * 100}%` : "0%",
                  }}
                />
              </div>
              <span className="w-8 text-right text-sm">{r.count}</span>
            </div>
          ))}
        </div>

        {/* Contact info coverage */}
        <div className="rounded-lg border bg-white p-6">
          <h2 className="text-lg font-semibold mb-4">Contact Info Coverage</h2>
          <div className="space-y-3">
            {[
              { label: "Has Email", count: data.with_email_count },
              { label: "Has Phone", count: data.with_phone_count },
              { label: "Has Website", count: data.with_website_count },
            ].map((item) => (
              <div key={item.label} className="flex items-center gap-3">
                <span className="w-24 text-sm text-gray-600">{item.label}</span>
                <div className="flex-1 h-4 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-400 rounded-full"
                    style={{
                      width: data.total_leads > 0 ? `${(item.count / data.total_leads) * 100}%` : "0%",
                    }}
                  />
                </div>
                <span className="text-sm font-medium">
                  {item.count}/{data.total_leads}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Monthly trend */}
        <div className="col-span-2 rounded-lg border bg-white p-6">
          <h2 className="text-lg font-semibold mb-4">Monthly Lead Growth</h2>
          <div className="flex items-end gap-2 h-40">
            {data.by_month.map((m) => {
              const maxCount = Math.max(...data.by_month.map((x) => x.count), 1);
              return (
                <div key={m.month} className="flex-1 flex flex-col items-center gap-1">
                  <span className="text-xs font-medium">{m.count}</span>
                  <div
                    className="w-full bg-primary-500 rounded-t"
                    style={{ height: `${(m.count / maxCount) * 100}%`, minHeight: "4px" }}
                  />
                  <span className="text-xs text-gray-500">{m.month.slice(5)}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
