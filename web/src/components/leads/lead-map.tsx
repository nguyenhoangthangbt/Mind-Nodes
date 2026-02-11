"use client";

import { useEffect, useRef, useState } from "react";
import type { Lead } from "@/types";

const STAGE_COLORS: Record<string, string> = {
  new: "#3b82f6",
  contacted: "#eab308",
  responded: "#22c55e",
  meeting: "#a855f7",
  proposal: "#f97316",
  won: "#10b981",
  lost: "#ef4444",
};

interface LeadMapProps {
  leads: Lead[];
  center?: { lat: number; lng: number };
  zoom?: number;
  onLeadClick?: (lead: Lead) => void;
  selectedLeadId?: string;
  height?: string;
}

/**
 * Interactive map component showing lead locations with pipeline-stage colored pins.
 * Uses Google Maps JavaScript API.
 * Falls back to a static list view if the API key is not configured.
 */
export function LeadMap({
  leads,
  center,
  zoom = 12,
  onLeadClick,
  selectedLeadId,
  height = "500px",
}: LeadMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.marker.AdvancedMarkerElement[]>([]);
  const [infoWindow, setInfoWindow] = useState<google.maps.InfoWindow | null>(null);
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY;

  // Filter leads that have coordinates
  const mappableLeads = leads.filter((l) => l.latitude && l.longitude);

  // Calculate center from leads if not provided
  const mapCenter = center || (mappableLeads.length > 0
    ? {
        lat: mappableLeads.reduce((sum, l) => sum + l.latitude!, 0) / mappableLeads.length,
        lng: mappableLeads.reduce((sum, l) => sum + l.longitude!, 0) / mappableLeads.length,
      }
    : { lat: 40.7128, lng: -74.006 }); // Default to NYC

  // Load Google Maps script
  useEffect(() => {
    if (!apiKey) return;
    if (document.getElementById("google-maps-script")) return;

    const script = document.createElement("script");
    script.id = "google-maps-script";
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=marker&v=weekly`;
    script.async = true;
    script.defer = true;
    script.onload = () => initMap();
    document.head.appendChild(script);

    return () => {
      // Cleanup not needed for script tag
    };
  }, [apiKey]);

  // Initialize map
  const initMap = () => {
    if (!mapRef.current || !window.google) return;

    const newMap = new google.maps.Map(mapRef.current, {
      center: mapCenter,
      zoom,
      mapId: "leadlocal-map",
      disableDefaultUI: false,
      zoomControl: true,
      streetViewControl: false,
      mapTypeControl: false,
    });

    const newInfoWindow = new google.maps.InfoWindow();

    setMap(newMap);
    setInfoWindow(newInfoWindow);
  };

  // Update markers when leads change
  useEffect(() => {
    if (!map || !infoWindow) return;

    // Clear old markers
    markers.forEach((m) => (m.map = null));

    const newMarkers = mappableLeads.map((lead) => {
      const color = STAGE_COLORS[lead.pipeline_stage] || "#6b7280";

      // Create colored pin element
      const pinEl = document.createElement("div");
      pinEl.style.cssText = `
        width: 24px; height: 24px; border-radius: 50%;
        background: ${color}; border: 2px solid white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        cursor: pointer;
        ${selectedLeadId === lead.id ? "width: 32px; height: 32px; border-width: 3px;" : ""}
      `;

      const marker = new google.maps.marker.AdvancedMarkerElement({
        map,
        position: { lat: lead.latitude!, lng: lead.longitude! },
        title: lead.business_name,
        content: pinEl,
      });

      marker.addListener("click", () => {
        infoWindow.setContent(`
          <div style="max-width: 250px; font-family: sans-serif;">
            <h3 style="margin: 0 0 4px; font-size: 14px; font-weight: 600;">${lead.business_name}</h3>
            ${lead.category ? `<p style="margin: 0; font-size: 12px; color: #6b7280;">${lead.category}</p>` : ""}
            ${lead.address ? `<p style="margin: 4px 0 0; font-size: 12px;">${lead.address}</p>` : ""}
            <div style="margin-top: 6px; display: flex; gap: 8px; font-size: 11px;">
              <span style="background: ${color}; color: white; padding: 1px 6px; border-radius: 9999px;">
                ${lead.pipeline_stage}
              </span>
              ${lead.rating ? `<span>Rating: ${lead.rating}/5</span>` : ""}
            </div>
            ${lead.phone ? `<p style="margin: 4px 0 0; font-size: 12px;">${lead.phone}</p>` : ""}
          </div>
        `);
        infoWindow.open(map, marker);
        onLeadClick?.(lead);
      });

      return marker;
    });

    setMarkers(newMarkers);
  }, [map, infoWindow, leads, selectedLeadId]);

  // No API key fallback — simple list with coordinates
  if (!apiKey) {
    return (
      <div className="rounded-lg border bg-white p-4" style={{ height }}>
        <p className="text-sm text-gray-500 mb-3">
          Map view requires a Google Maps API key. Set NEXT_PUBLIC_GOOGLE_MAPS_KEY in your .env file.
        </p>
        <div className="space-y-2 overflow-auto" style={{ maxHeight: `calc(${height} - 60px)` }}>
          {mappableLeads.map((lead) => (
            <div
              key={lead.id}
              onClick={() => onLeadClick?.(lead)}
              className={`flex items-center gap-3 p-2 rounded cursor-pointer hover:bg-gray-50 ${
                selectedLeadId === lead.id ? "bg-primary-50 ring-1 ring-primary-300" : ""
              }`}
            >
              <div
                className="w-3 h-3 rounded-full flex-shrink-0"
                style={{ backgroundColor: STAGE_COLORS[lead.pipeline_stage] || "#6b7280" }}
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{lead.business_name}</p>
                <p className="text-xs text-gray-500 truncate">{lead.address}</p>
              </div>
              <span className="text-xs text-gray-400 capitalize">{lead.pipeline_stage}</span>
            </div>
          ))}
          {mappableLeads.length === 0 && (
            <p className="text-sm text-gray-400 text-center py-8">No leads with location data</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div ref={mapRef} style={{ height, width: "100%", borderRadius: "0.5rem" }} />
      {/* Legend */}
      <div className="mt-2 flex flex-wrap gap-3">
        {Object.entries(STAGE_COLORS).map(([stage, color]) => (
          <div key={stage} className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-xs text-gray-500 capitalize">{stage}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
