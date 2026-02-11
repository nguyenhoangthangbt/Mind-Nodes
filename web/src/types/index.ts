// Auth
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  company: string | null;
  tier: string;
  is_verified: boolean;
  created_at: string;
}

// Leads
export interface Lead {
  id: string;
  business_name: string;
  google_place_id: string | null;
  address: string | null;
  phone: string | null;
  email: string | null;
  website: string | null;
  category: string | null;
  rating: number | null;
  review_count: number | null;
  latitude: number | null;
  longitude: number | null;
  pipeline_stage: string;
  source: string;
  contact_name: string | null;
  contact_email: string | null;
  created_at: string;
  updated_at: string;
  tags: Tag[];
  notes_count: number;
}

export interface LeadListResponse {
  items: Lead[];
  total: number;
  page: number;
  per_page: number;
}

export interface Tag {
  id: string;
  name: string;
  color: string;
}

export interface PipelineStats {
  new: number;
  contacted: number;
  responded: number;
  meeting: number;
  proposal: number;
  won: number;
  lost: number;
}

// Search
export interface SearchResult {
  google_place_id: string | null;
  business_name: string;
  address: string | null;
  phone: string | null;
  website: string | null;
  category: string | null;
  rating: number | null;
  review_count: number | null;
  latitude: number | null;
  longitude: number | null;
  source: string;
  already_saved: boolean;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
  cached: boolean;
}

// Notes & Reminders
export interface Note {
  id: string;
  lead_id: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface Reminder {
  id: string;
  lead_id: string;
  title: string;
  description: string | null;
  due_at: string;
  is_completed: boolean;
  created_at: string;
}

// Billing
export interface UsageResponse {
  tier: string;
  leads_used: number;
  leads_limit: number;
  searches_used: number;
  searches_limit: number;
}

// Analytics
export interface LeadAnalytics {
  total_leads: number;
  pipeline: PipelineStats;
  by_source: { source: string; count: number }[];
  by_category: { category: string; count: number }[];
  by_month: { month: string; count: number }[];
  rating_distribution: { bucket: string; count: number }[];
  avg_rating: number | null;
  with_email_count: number;
  with_phone_count: number;
  with_website_count: number;
  conversion_rate: number;
}
