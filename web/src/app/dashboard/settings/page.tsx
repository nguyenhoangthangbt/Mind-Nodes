"use client";

import { useAuth } from "@/stores/auth";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { UsageResponse } from "@/types";

const TIERS = [
  { tier: "free", name: "Free", price: "$0", features: ["50 leads", "10 searches/mo"] },
  { tier: "starter", name: "Starter", price: "$19/mo", features: ["500 leads", "50 searches/mo"] },
  { tier: "pro", name: "Pro", price: "$39/mo", features: ["2,000 leads", "200 searches/mo"] },
  { tier: "agency", name: "Agency", price: "$79/mo", features: ["10,000 leads", "Unlimited searches"] },
];

export default function SettingsPage() {
  const { user } = useAuth();
  const { data: usage } = useQuery({
    queryKey: ["usage"],
    queryFn: () => api.get<UsageResponse>("/api/v1/billing/usage"),
  });

  const handleUpgrade = async (priceId: string) => {
    try {
      const resp = await api.post<{ checkout_url: string }>("/api/v1/billing/checkout", {
        price_id: priceId,
      });
      window.location.href = resp.checkout_url;
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleManageBilling = async () => {
    try {
      const resp = await api.post<{ portal_url: string }>("/api/v1/billing/portal");
      window.location.href = resp.portal_url;
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      {/* Profile */}
      <section className="mb-8 rounded-lg border bg-white p-6">
        <h2 className="text-lg font-semibold mb-4">Profile</h2>
        <div className="space-y-2 text-sm">
          <p><span className="text-gray-500 w-24 inline-block">Name:</span> {user?.full_name}</p>
          <p><span className="text-gray-500 w-24 inline-block">Email:</span> {user?.email}</p>
          <p><span className="text-gray-500 w-24 inline-block">Company:</span> {user?.company || "-"}</p>
          <p><span className="text-gray-500 w-24 inline-block">Plan:</span>
            <span className="font-medium uppercase">{user?.tier}</span>
          </p>
        </div>
      </section>

      {/* Plans */}
      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Plans</h2>
        <div className="grid grid-cols-4 gap-4">
          {TIERS.map((t) => (
            <div
              key={t.tier}
              className={`rounded-lg border p-4 ${
                user?.tier === t.tier ? "border-primary-500 ring-1 ring-primary-500" : ""
              }`}
            >
              <h3 className="font-semibold">{t.name}</h3>
              <p className="text-2xl font-bold mt-1">{t.price}</p>
              <ul className="mt-3 space-y-1">
                {t.features.map((f) => (
                  <li key={f} className="text-sm text-gray-600">- {f}</li>
                ))}
              </ul>
              {user?.tier === t.tier ? (
                <p className="mt-3 text-sm text-primary-600 font-medium">Current Plan</p>
              ) : t.tier !== "free" ? (
                <button
                  onClick={() => handleUpgrade(`price_${t.tier}`)}
                  className="mt-3 w-full rounded-md bg-primary-600 py-1.5 text-sm text-white hover:bg-primary-700"
                >
                  Upgrade
                </button>
              ) : null}
            </div>
          ))}
        </div>
      </section>

      {/* Billing portal */}
      {user?.tier !== "free" && (
        <section>
          <button
            onClick={handleManageBilling}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
          >
            Manage Billing (invoices, cancel, update card)
          </button>
        </section>
      )}
    </div>
  );
}
