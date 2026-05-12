"use client";

import { useQuery, useMutation } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { publicApi } from "@/lib/api";
import type { Clinic, Service } from "@/types";

type FormValues = {
  full_name: string;
  phone: string;
  email?: string;
  service_id: number;
  starts_at: string;
  note?: string;
};

export default function PublicBookingPage() {
  const { slug } = useParams<{ slug: string }>();
  const { register, handleSubmit, reset } = useForm<FormValues>();

  const clinicQ = useQuery({
    queryKey: ["public-clinic", slug],
    queryFn: async () =>
      (await publicApi.get<Clinic>(`/public/clinic/${slug}/`)).data,
  });

  const servicesQ = useQuery({
    queryKey: ["public-services", slug],
    queryFn: async () =>
      (
        await publicApi.get<Service[] | { results: Service[] }>(
          `/public/clinic/${slug}/services/`,
        )
      ).data,
  });

  const services: Service[] = Array.isArray(servicesQ.data)
    ? servicesQ.data
    : (servicesQ.data?.results ?? []);

  const book = useMutation({
    mutationFn: async (v: FormValues) =>
      (
        await publicApi.post(`/public/clinic/${slug}/book/`, {
          ...v,
          service_id: Number(v.service_id),
        })
      ).data,
    onSuccess: () => {
      toast.success("Uchrashuv muvaffaqiyatli bron qilindi!");
      reset();
    },
    onError: () => toast.error("Band vaqt yoki xatolik"),
  });

  if (clinicQ.isLoading) {
    return <div className="p-10 text-center">Yuklanmoqda...</div>;
  }
  if (!clinicQ.data) {
    return <div className="p-10 text-center">Klinika topilmadi</div>;
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-xl">
        <CardHeader>
          <CardTitle>{clinicQ.data.name}</CardTitle>
          <CardDescription>
            {clinicQ.data.address || clinicQ.data.description || "Uchrashuv bron qiling"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) => book.mutate(v))}
            className="space-y-4"
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
            <div className="space-y-1">
              <Label>Xizmat</Label>
              <select
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
                {...register("service_id", { required: true })}
              >
                <option value="">-- tanlang --</option>
                {services.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.duration_minutes} min)
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-1">
              <Label>Vaqt</Label>
              <Input
                type="datetime-local"
                {...register("starts_at", { required: true })}
              />
            </div>
            <div className="space-y-1">
              <Label>Izoh</Label>
              <Textarea rows={3} {...register("note")} />
            </div>
            <Button type="submit" className="w-full" disabled={book.isPending}>
              {book.isPending ? "Yuborilmoqda..." : "Bron qilish"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
