"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { api } from "@/lib/api";
import { useAuthStore, type User } from "@/stores/auth";

export function useLogin() {
  const router = useRouter();
  const { setTokens, setUser } = useAuthStore();

  return useMutation({
    mutationFn: async (payload: { email: string; password: string }) => {
      const { data } = await api.post("/auth/login/", payload);
      return data as { access: string; refresh: string };
    },
    onSuccess: async (data) => {
      setTokens(data.access, data.refresh);
      const me = await api.get<User>("/auth/me/");
      setUser(me.data);
      toast.success("Xush kelibsiz!");
      router.push("/dashboard");
    },
    onError: () => toast.error("Email yoki parol noto'g'ri"),
  });
}

export function useRegister() {
  const router = useRouter();

  return useMutation({
    mutationFn: async (payload: {
      email: string;
      password: string;
      full_name: string;
      phone?: string;
      clinic_name?: string;
    }) => {
      const { data } = await api.post("/auth/register/", payload);
      return data;
    },
    onSuccess: () => {
      toast.success("Ro'yxatdan o'tdingiz! Endi kiring.");
      router.push("/login");
    },
    onError: () => toast.error("Ro'yxatdan o'tishda xatolik"),
  });
}

export function useMe() {
  const { accessToken, setUser } = useAuthStore();
  return useQuery({
    queryKey: ["me"],
    enabled: !!accessToken,
    queryFn: async () => {
      const { data } = await api.get<User>("/auth/me/");
      setUser(data);
      return data;
    },
  });
}

export function useLogout() {
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);
  return () => {
    logout();
    router.push("/login");
  };
}
