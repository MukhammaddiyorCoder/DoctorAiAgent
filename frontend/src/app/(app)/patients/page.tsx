"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreatePatient, usePatients } from "@/hooks/useApi";

type FormValues = {
  full_name: string;
  phone: string;
  email?: string;
};

export default function PatientsPage() {
  const [search, setSearch] = useState("");
  const { data: patients = [] } = usePatients(search);
  const create = useCreatePatient();
  const { register, handleSubmit, reset } = useForm<FormValues>();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Bemorlar</h1>

      <Card>
        <CardHeader>
          <CardTitle>Yangi bemor qo&apos;shish</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) =>
              create.mutate(v, {
                onSuccess: () => {
                  toast.success("Bemor qo'shildi");
                  reset();
                },
                onError: () => toast.error("Xatolik"),
              }),
            )}
            className="grid gap-3 sm:grid-cols-4"
          >
            <div className="space-y-1">
              <Label>Ism</Label>
              <Input {...register("full_name", { required: true })} />
            </div>
            <div className="space-y-1">
              <Label>Telefon</Label>
              <Input {...register("phone", { required: true })} />
            </div>
            <div className="space-y-1">
              <Label>Email</Label>
              <Input type="email" {...register("email")} />
            </div>
            <div className="flex items-end">
              <Button type="submit" disabled={create.isPending}>
                Qo&apos;shish
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex-row items-center justify-between">
          <CardTitle>Bemorlar ro&apos;yxati</CardTitle>
          <Input
            className="max-w-xs"
            placeholder="Qidirish..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </CardHeader>
        <CardContent>
          {!patients.length ? (
            <p className="text-muted-foreground">Bemorlar topilmadi.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b text-muted-foreground">
                  <tr>
                    <th className="pb-2 pr-4">Ism</th>
                    <th className="pb-2 pr-4">Telefon</th>
                    <th className="pb-2 pr-4">Email</th>
                    <th className="pb-2">Ro&apos;yxatga olingan</th>
                  </tr>
                </thead>
                <tbody>
                  {patients.map((p) => (
                    <tr key={p.id} className="border-b">
                      <td className="py-2 pr-4">{p.full_name}</td>
                      <td className="py-2 pr-4">{p.phone}</td>
                      <td className="py-2 pr-4">{p.email || "-"}</td>
                      <td className="py-2">
                        {new Date(p.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
