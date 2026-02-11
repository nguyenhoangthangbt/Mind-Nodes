"use client";

import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useUpdateLead, useDeleteLead } from "@/hooks/use-leads";
import { LeadMap } from "@/components/leads/lead-map";
import type { Lead, Note, Reminder } from "@/types";

const STAGE_COLORS: Record<string, string> = {
  new: "bg-blue-100 text-blue-700",
  contacted: "bg-yellow-100 text-yellow-700",
  responded: "bg-green-100 text-green-700",
  meeting: "bg-purple-100 text-purple-700",
  proposal: "bg-orange-100 text-orange-700",
  won: "bg-emerald-100 text-emerald-700",
  lost: "bg-red-100 text-red-700",
};

export default function LeadDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const qc = useQueryClient();
  const updateLead = useUpdateLead();
  const deleteLead = useDeleteLead();

  const { data: lead, isLoading } = useQuery({
    queryKey: ["lead", id],
    queryFn: () => api.get<Lead>(`/api/v1/leads/${id}`),
  });

  const { data: notes } = useQuery({
    queryKey: ["notes", id],
    queryFn: () => api.get<Note[]>(`/api/v1/leads/${id}/notes`),
  });

  const { data: reminders } = useQuery({
    queryKey: ["reminders", id],
    queryFn: () => api.get<Reminder[]>(`/api/v1/leads/${id}/reminders`),
  });

  // Note creation
  const [newNote, setNewNote] = useState("");
  const addNote = useMutation({
    mutationFn: (content: string) => api.post(`/api/v1/leads/${id}/notes`, { content }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["notes", id] });
      setNewNote("");
    },
  });

  // Reminder creation
  const [reminderForm, setReminderForm] = useState({ title: "", due_at: "" });
  const addReminder = useMutation({
    mutationFn: (data: { title: string; due_at: string }) =>
      api.post(`/api/v1/leads/${id}/reminders`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["reminders", id] });
      setReminderForm({ title: "", due_at: "" });
    },
  });

  const completeReminder = useMutation({
    mutationFn: (reminderId: string) =>
      api.patch(`/api/v1/reminders/${reminderId}`, { is_completed: true }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["reminders", id] }),
  });

  if (isLoading) return <p className="text-gray-500">Loading...</p>;
  if (!lead) return <p className="text-gray-500">Lead not found.</p>;

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-700 mb-2">
            &larr; Back to Leads
          </button>
          <h1 className="text-2xl font-bold">{lead.business_name}</h1>
          {lead.category && <p className="text-gray-500">{lead.category}</p>}
        </div>
        <div className="flex items-center gap-3">
          <select
            value={lead.pipeline_stage}
            onChange={(e) => updateLead.mutate({ id: lead.id, pipeline_stage: e.target.value } as any)}
            className={`rounded-full px-3 py-1 text-sm font-medium ${STAGE_COLORS[lead.pipeline_stage] || "bg-gray-100"}`}
          >
            {Object.keys(STAGE_COLORS).map((s) => (
              <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
          <button
            onClick={() => {
              if (confirm("Delete this lead permanently?")) {
                deleteLead.mutate(lead.id, { onSuccess: () => router.push("/dashboard/leads") });
              }
            }}
            className="text-sm text-red-500 hover:text-red-700"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Left column: Info + Map */}
        <div className="col-span-2 space-y-6">
          {/* Business details */}
          <div className="rounded-lg border bg-white p-6">
            <h2 className="text-lg font-semibold mb-4">Business Details</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              {lead.address && <div><span className="text-gray-500">Address:</span> {lead.address}</div>}
              {lead.phone && <div><span className="text-gray-500">Phone:</span> {lead.phone}</div>}
              {lead.email && <div><span className="text-gray-500">Email:</span> <a href={`mailto:${lead.email}`} className="text-primary-600">{lead.email}</a></div>}
              {lead.website && <div><span className="text-gray-500">Website:</span> <a href={lead.website} target="_blank" rel="noopener noreferrer" className="text-primary-600">{lead.website}</a></div>}
              {lead.rating && <div><span className="text-gray-500">Rating:</span> {lead.rating}/5 ({lead.review_count} reviews)</div>}
              <div><span className="text-gray-500">Source:</span> <span className="capitalize">{lead.source.replace("_", " ")}</span></div>
              {lead.contact_name && <div><span className="text-gray-500">Contact:</span> {lead.contact_name}</div>}
              {lead.contact_email && <div><span className="text-gray-500">Contact Email:</span> {lead.contact_email}</div>}
            </div>
          </div>

          {/* Map — individual lead location */}
          {lead.latitude && lead.longitude && (
            <div className="rounded-lg border bg-white p-6">
              <h2 className="text-lg font-semibold mb-4">Location</h2>
              <LeadMap
                leads={[lead]}
                center={{ lat: lead.latitude, lng: lead.longitude }}
                zoom={15}
                height="300px"
              />
            </div>
          )}

          {/* Notes */}
          <div className="rounded-lg border bg-white p-6">
            <h2 className="text-lg font-semibold mb-4">Notes</h2>
            <div className="flex gap-2 mb-4">
              <input
                type="text"
                placeholder="Add a note..."
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && newNote.trim()) addNote.mutate(newNote);
                }}
                className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
              />
              <button
                onClick={() => newNote.trim() && addNote.mutate(newNote)}
                disabled={addNote.isPending}
                className="rounded-md bg-primary-600 px-4 py-2 text-sm text-white hover:bg-primary-700 disabled:opacity-50"
              >
                Add
              </button>
            </div>
            <div className="space-y-3">
              {notes?.map((note) => (
                <div key={note.id} className="border-l-2 border-primary-200 pl-3 py-1">
                  <p className="text-sm">{note.content}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(note.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
              {notes?.length === 0 && <p className="text-sm text-gray-400">No notes yet.</p>}
            </div>
          </div>
        </div>

        {/* Right column: Reminders + Tags */}
        <div className="space-y-6">
          {/* Reminders */}
          <div className="rounded-lg border bg-white p-6">
            <h2 className="text-lg font-semibold mb-4">Reminders</h2>
            <div className="space-y-2 mb-4">
              <input
                type="text"
                placeholder="Reminder title"
                value={reminderForm.title}
                onChange={(e) => setReminderForm({ ...reminderForm, title: e.target.value })}
                className="w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm"
              />
              <input
                type="datetime-local"
                value={reminderForm.due_at}
                onChange={(e) => setReminderForm({ ...reminderForm, due_at: e.target.value })}
                className="w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm"
              />
              <button
                onClick={() => {
                  if (reminderForm.title && reminderForm.due_at) {
                    addReminder.mutate({
                      title: reminderForm.title,
                      due_at: new Date(reminderForm.due_at).toISOString(),
                    });
                  }
                }}
                disabled={addReminder.isPending}
                className="w-full rounded-md bg-primary-600 py-1.5 text-sm text-white hover:bg-primary-700 disabled:opacity-50"
              >
                Add Reminder
              </button>
            </div>
            <div className="space-y-2">
              {reminders?.map((r) => (
                <div
                  key={r.id}
                  className={`flex items-start gap-2 p-2 rounded ${r.is_completed ? "opacity-50" : ""}`}
                >
                  <input
                    type="checkbox"
                    checked={r.is_completed}
                    onChange={() => !r.is_completed && completeReminder.mutate(r.id)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <p className={`text-sm ${r.is_completed ? "line-through" : ""}`}>{r.title}</p>
                    <p className="text-xs text-gray-400">
                      Due: {new Date(r.due_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
              {reminders?.length === 0 && <p className="text-sm text-gray-400">No reminders.</p>}
            </div>
          </div>

          {/* Tags */}
          <div className="rounded-lg border bg-white p-6">
            <h2 className="text-lg font-semibold mb-4">Tags</h2>
            <div className="flex flex-wrap gap-2">
              {lead.tags.length > 0
                ? lead.tags.map((tag) => (
                    <span
                      key={tag.id}
                      className="rounded-full px-2.5 py-0.5 text-xs font-medium text-white"
                      style={{ backgroundColor: tag.color }}
                    >
                      {tag.name}
                    </span>
                  ))
                : <p className="text-sm text-gray-400">No tags.</p>}
            </div>
          </div>

          {/* Quick actions */}
          <div className="rounded-lg border bg-white p-6">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-2">
              {lead.phone && (
                <a
                  href={`tel:${lead.phone}`}
                  className="block w-full rounded-md border px-3 py-2 text-center text-sm hover:bg-gray-50"
                >
                  Call {lead.phone}
                </a>
              )}
              {lead.email && (
                <a
                  href={`mailto:${lead.email}`}
                  className="block w-full rounded-md border px-3 py-2 text-center text-sm hover:bg-gray-50"
                >
                  Email {lead.email}
                </a>
              )}
              {lead.website && (
                <a
                  href={lead.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full rounded-md border px-3 py-2 text-center text-sm hover:bg-gray-50"
                >
                  Visit Website
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
