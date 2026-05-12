"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { useMe } from "@/hooks/useAuth";
import { useAuthStore, type User } from "@/stores/auth";

type FormValues = {
  full_name: string;
  phone: string;
};

export default function ProfilePage() {
  const { data: user } = useMe();
  const setUser = useAuthStore((s) => s.setUser);
  const qc = useQueryClient();
  const { register, handleSubmit, reset } = useForm<FormValues>();

  useEffect(() => {
    if (user) reset({ full_name: user.full_name, phone: user.phone });
  }, [user, reset]);

  const update = useMutation({
    mutationFn: async (v: FormValues) => (await api.patch<User>("/auth/me/", v)).data,
    onSuccess: (u) => {
      setUser(u);
      qc.invalidateQueries({ queryKey: ["me"] });
      toast.success("Profil yangilandi");
    },
    onError: () => toast.error("Xatolik"),
  });

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Profil</h1>
      <Card>
        <CardHeader>
          <CardTitle>Shaxsiy ma&apos;lumotlar</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) => update.mutate(v))}
            className="grid gap-4 sm:grid-cols-2"
          >
            <div className="space-y-1">
              <Label>Email</Label>
              <Input value={user?.email ?? ""} disabled />
            </div>
            <div className="space-y-1">
              <Label>Rol</Label>
              <Input value={user?.role ?? ""} disabled />
            </div>
            <div className="space-y-1">
              <Label>To&apos;liq ism</Label>
              <Input {...register("full_name")} />
            </div>
            <div className="space-y-1">
              <Label>Telefon</Label>
              <Input {...register("phone")} />
            </div>
            <div className="sm:col-span-2">
              <Button type="submit" disabled={update.isPending}>
                Saqlash
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
