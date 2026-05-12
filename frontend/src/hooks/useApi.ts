"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { api } from "@/lib/api";
import type {
  Appointment,
  Clinic,
  DashboardStats,
  Paginated,
  Patient,
  Service,
} from "@/types";

// ----------------- Clinic -----------------
export function useClinic() {
  return useQuery({
    queryKey: ["clinic"],
    queryFn: async () => (await api.get<Clinic>("/clinic/")).data,
  });
}

export function useUpdateClinic() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Clinic>) =>
      (await api.put<Clinic>("/clinic/", payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["clinic"] }),
  });
}

// ----------------- Services -----------------
export function useServices() {
  return useQuery({
    queryKey: ["services"],
    queryFn: async () =>
      (await api.get<Paginated<Service>>("/services/")).data.results,
  });
}

export function useCreateService() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Service>) =>
      (await api.post<Service>("/services/", payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["services"] }),
  });
}

export function useUpdateService() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...payload }: Partial<Service> & { id: number }) =>
      (await api.patch<Service>(`/services/${id}/`, payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["services"] }),
  });
}

export function useDeleteService() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => api.delete(`/services/${id}/`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["services"] }),
  });
}

// ----------------- Patients -----------------
export function usePatients(search?: string) {
  return useQuery({
    queryKey: ["patients", search],
    queryFn: async () => {
      const { data } = await api.get<Paginated<Patient>>("/patients/", {
        params: { search },
      });
      return data.results;
    },
  });
}

export function useCreatePatient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Patient>) =>
      (await api.post<Patient>("/patients/", payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["patients"] }),
  });
}

// ----------------- Appointments -----------------
export function useAppointments(params?: {
  from?: string;
  to?: string;
  status?: string;
}) {
  return useQuery({
    queryKey: ["appointments", params],
    queryFn: async () => {
      const { data } = await api.get<Paginated<Appointment>>(
        "/appointments/",
        { params },
      );
      return data.results;
    },
  });
}

export function useCreateAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Partial<Appointment>) =>
      (await api.post<Appointment>("/appointments/", payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["appointments"] }),
  });
}

export function useUpdateAppointment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...payload }: Partial<Appointment> & { id: number }) =>
      (await api.patch<Appointment>(`/appointments/${id}/`, payload)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["appointments"] }),
  });
}

export function useDashboardStats() {
  return useQuery({
    queryKey: ["appointments", "stats"],
    queryFn: async () =>
      (await api.get<DashboardStats>("/appointments/stats/")).data,
  });
}

export interface TrendPoint {
  date: string;
  count: number;
  ai: number;
}

export function useAppointmentTrend(days = 14) {
  return useQuery({
    queryKey: ["appointments", "trend", days],
    queryFn: async () =>
      (await api.get<TrendPoint[]>("/appointments/trend/", { params: { days } }))
        .data,
  });
}
