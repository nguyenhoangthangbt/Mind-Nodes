"use client";

import { useState } from "react";
import { useSearch } from "@/hooks/use-search";
import { useSaveLead } from "@/hooks/use-leads";
import type { SearchResult } from "@/types";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");
  const search = useSearch();
  const saveLead = useSaveLead();
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    search.mutate({ query, location: location || undefined });
  };

  const handleSave = async (result: SearchResult) => {
    await saveLead.mutateAsync({
      business_name: result.business_name,
      google_place_id: result.google_place_id,
      address: result.address,
      phone: result.phone,
      website: result.website,
      category: result.category,
      rating: result.rating,
      review_count: result.review_count,
      latitude: result.latitude,
      longitude: result.longitude,
      source: result.source,
    } as any);
    if (result.google_place_id) {
      setSavedIds((prev) => new Set(prev).add(result.google_place_id!));
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Search Local Businesses</h1>

      <form onSubmit={handleSearch} className="mb-8 flex gap-3">
        <input
          type="text"
          placeholder="e.g. restaurants, plumbers, dentists..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        />
        <input
          type="text"
          placeholder="Location (city, zip, or address)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-64 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
        />
        <button
          type="submit"
          disabled={search.isPending}
          className="rounded-md bg-primary-600 px-6 py-2 text-sm font-semibold text-white hover:bg-primary-700 disabled:opacity-50"
        >
          {search.isPending ? "Searching..." : "Search"}
        </button>
      </form>

      {search.data && (
        <div>
          <p className="mb-4 text-sm text-gray-500">
            Found {search.data.total} results for "{search.data.query}"
            {search.data.cached && " (cached)"}
          </p>
          <div className="space-y-3">
            {search.data.results.map((result, i) => {
              const isSaved = result.already_saved || (result.google_place_id && savedIds.has(result.google_place_id));
              return (
                <div key={i} className="flex items-start justify-between rounded-lg border bg-white p-4">
                  <div className="flex-1">
                    <h3 className="font-semibold">{result.business_name}</h3>
                    {result.category && (
                      <span className="text-xs text-gray-500">{result.category}</span>
                    )}
                    {result.address && <p className="mt-1 text-sm text-gray-600">{result.address}</p>}
                    <div className="mt-1 flex gap-4 text-sm text-gray-500">
                      {result.phone && <span>{result.phone}</span>}
                      {result.rating && <span>Rating: {result.rating}/5 ({result.review_count} reviews)</span>}
                    </div>
                  </div>
                  <button
                    onClick={() => handleSave(result)}
                    disabled={!!isSaved || saveLead.isPending}
                    className={`ml-4 rounded-md px-4 py-2 text-sm font-medium ${
                      isSaved
                        ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                        : "bg-primary-50 text-primary-600 hover:bg-primary-100"
                    }`}
                  >
                    {isSaved ? "Saved" : "Save Lead"}
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
