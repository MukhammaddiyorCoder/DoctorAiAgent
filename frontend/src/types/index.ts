export interface Clinic {
  id: number;
  name: string;
  slug: string;
  phone: string;
  email: string;
  address: string;
  website: string;
  description: string;
  timezone: string;
  work_start: string;
  work_end: string;
  slot_duration_minutes: number;
  ai_enabled: boolean;
  ai_system_prompt: string;
  ai_welcome_message: string;
}

export interface Service {
  id: number;
  name: string;
  description: string;
  duration_minutes: number;
  price: string;
  currency: string;
  is_active: boolean;
}

export interface Patient {
  id: number;
  full_name: string;
  phone: string;
  email: string;
  date_of_birth: string | null;
  gender: string;
  notes: string;
  created_at: string;
}

export type AppointmentStatus =
  | "pending"
  | "confirmed"
  | "cancelled"
  | "completed"
  | "no_show";

export type AppointmentSource = "manual" | "ai" | "public";

export interface Appointment {
  id: number;
  patient: number;
  patient_name: string;
  service: number;
  service_name: string;
  starts_at: string;
  ends_at: string;
  status: AppointmentStatus;
  source: AppointmentSource;
  note: string;
  created_at: string;
}

export interface DashboardStats {
  total: number;
  today: number;
  upcoming: number;
  by_status: Record<string, number>;
  ai_booked: number;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
