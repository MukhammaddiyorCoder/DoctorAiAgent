"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useClinic, useUpdateClinic } from "@/hooks/useApi";

type FormValues = {
  name: string;
  phone: string;
  email: string;
  address: string;
  website: string;
  description: string;
  work_start: string;
  work_end: string;
  slot_duration_minutes: number;
};

export default function SettingsPage() {
  const { data: clinic } = useClinic();
  const update = useUpdateClinic();
  const { register, handleSubmit, reset } = useForm<FormValues>();

  useEffect(() => {
    if (clinic) reset(clinic as unknown as FormValues);
  }, [clinic, reset]);

  if (!clinic) return null;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Klinika sozlamalari</h1>

      <Card>
        <CardHeader>
          <CardTitle>Asosiy ma&apos;lumotlar</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) =>
              update.mutate(v, {
                onSuccess: () => toast.success("Saqlandi"),
                onError: () => toast.error("Xatolik"),
              }),
            )}
            className="grid gap-4 sm:grid-cols-2"
          >
            <div className="space-y-1">
              <Label>Nomi</Label>
              <Input {...register("name")} />
            </div>
            <div className="space-y-1">
              <Label>Telefon</Label>
              <Input {...register("phone")} />
            </div>
            <div className="space-y-1">
              <Label>Email</Label>
              <Input type="email" {...register("email")} />
            </div>
            <div className="space-y-1">
              <Label>Vebsayt</Label>
              <Input {...register("website")} />
            </div>
            <div className="space-y-1 sm:col-span-2">
              <Label>Manzil</Label>
              <Input {...register("address")} />
            </div>
            <div className="space-y-1 sm:col-span-2">
              <Label>Tavsif</Label>
              <Textarea rows={3} {...register("description")} />
            </div>
            <div className="space-y-1">
              <Label>Ish boshlanish vaqti</Label>
              <Input type="time" {...register("work_start")} />
            </div>
            <div className="space-y-1">
              <Label>Ish tugash vaqti</Label>
              <Input type="time" {...register("work_end")} />
            </div>
            <div className="space-y-1">
              <Label>Slot (min)</Label>
              <Input
                type="number"
                {...register("slot_duration_minutes", { valueAsNumber: true })}
              />
            </div>
            <div className="flex items-end sm:col-span-2">
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
