"use client";

import { Bot, Calendar, Check, Clock, Stethoscope, X } from "lucide-react";
import { toast } from "sonner";

import { TrendChart } from "@/components/dashboard/trend-chart";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  useAppointments,
  useDashboardStats,
  useUpdateAppointment,
} from "@/hooks/useApi";
import type { AppointmentStatus } from "@/types";

const statusVariant: Record<
  AppointmentStatus,
  "default" | "success" | "destructive" | "warning" | "secondary"
> = {
  pending: "warning",
  confirmed: "success",
  cancelled: "destructive",
  completed: "secondary",
  no_show: "destructive",
};

export default function DashboardPage() {
  const { data: stats } = useDashboardStats();
  const { data: upcoming = [] } = useAppointments();
  const update = useUpdateAppointment();

  const cards = [
    { title: "Bugun", value: stats?.today ?? 0, Icon: Clock },
    { title: "Jami uchrashuvlar", value: stats?.total ?? 0, Icon: Stethoscope },
    { title: "Kelgusi", value: stats?.upcoming ?? 0, Icon: Calendar },
    { title: "AI tomonidan bron", value: stats?.ai_booked ?? 0, Icon: Bot },
  ];

  const act = (id: number, status: AppointmentStatus, label: string) =>
    update.mutate(
      { id, status },
      {
        onSuccess: () => toast.success(label),
        onError: () => toast.error("Xatolik"),
      },
    );

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map(({ title, value, Icon }) => (
          <Card key={title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{title}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <TrendChart />

        <Card>
          <CardHeader>
            <CardTitle>Kelgusi uchrashuvlar</CardTitle>
          </CardHeader>
          <CardContent>
            {!upcoming.length ? (
              <p className="text-sm text-muted-foreground">
                Uchrashuvlar hali yo&apos;q.
              </p>
            ) : (
              <div className="space-y-2">
                {upcoming.slice(0, 6).map((a) => (
                  <div
                    key={a.id}
                    className="flex items-center justify-between rounded-md border p-3 text-sm"
                  >
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="truncate font-medium">
                          {a.patient_name}
                        </span>
                        <Badge variant={statusVariant[a.status]}>
                          {a.status}
                        </Badge>
                      </div>
                      <div className="truncate text-muted-foreground">
                        {a.service_name} ·{" "}
                        {new Date(a.starts_at).toLocaleString()}
                      </div>
                    </div>
                    {a.status === "pending" && (
                      <div className="ml-2 flex gap-1">
                        <Button
                          size="icon"
                          variant="ghost"
                          title="Tasdiqlash"
                          onClick={() => act(a.id, "confirmed", "Tasdiqlandi")}
                        >
                          <Check className="h-4 w-4 text-emerald-600" />
                        </Button>
                        <Button
                          size="icon"
                          variant="ghost"
                          title="Bekor qilish"
                          onClick={() => act(a.id, "cancelled", "Bekor qilindi")}
                        >
                          <X className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
