"use client";

import { Trash2 } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  useCreateService,
  useDeleteService,
  useServices,
} from "@/hooks/useApi";

type FormValues = {
  name: string;
  duration_minutes: number;
  price: string;
  currency: string;
};

export default function ServicesPage() {
  const { data: services = [] } = useServices();
  const create = useCreateService();
  const remove = useDeleteService();
  const { register, handleSubmit, reset } = useForm<FormValues>({
    defaultValues: { duration_minutes: 30, currency: "UZS" },
  });

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Xizmatlar</h1>

      <Card>
        <CardHeader>
          <CardTitle>Yangi xizmat</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) =>
              create.mutate(v, {
                onSuccess: () => {
                  toast.success("Xizmat qo'shildi");
                  reset();
                },
                onError: () => toast.error("Xatolik"),
              }),
            )}
            className="grid gap-3 sm:grid-cols-5"
          >
            <div className="space-y-1 sm:col-span-2">
              <Label>Nomi</Label>
              <Input {...register("name", { required: true })} />
            </div>
            <div className="space-y-1">
              <Label>Davomiyligi (min)</Label>
              <Input type="number" {...register("duration_minutes", { required: true, valueAsNumber: true })} />
            </div>
            <div className="space-y-1">
              <Label>Narxi</Label>
              <Input {...register("price", { required: true })} />
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
        <CardHeader>
          <CardTitle>Mavjud xizmatlar</CardTitle>
        </CardHeader>
        <CardContent>
          {!services.length ? (
            <p className="text-muted-foreground">Xizmatlar yo&apos;q.</p>
          ) : (
            <div className="divide-y">
              {services.map((s) => (
                <div
                  key={s.id}
                  className="flex items-center justify-between py-3 text-sm"
                >
                  <div>
                    <div className="font-medium">{s.name}</div>
                    <div className="text-muted-foreground">
                      {s.duration_minutes} min · {s.price} {s.currency}
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() =>
                      remove.mutate(s.id, {
                        onSuccess: () => toast.success("O'chirildi"),
                      })
                    }
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
