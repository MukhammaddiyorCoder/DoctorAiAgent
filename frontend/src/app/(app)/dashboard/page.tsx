"use client";

import { Calendar, Clock, Stethoscope, Bot } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppointments, useDashboardStats } from "@/hooks/useApi";

export default function DashboardPage() {
  const { data: stats } = useDashboardStats();
  const { data: upcoming } = useAppointments();

  const cards = [
    { title: "Bugun", value: stats?.today ?? 0, Icon: Clock },
    { title: "Jami uchrashuvlar", value: stats?.total ?? 0, Icon: Stethoscope },
    { title: "Kelgusi", value: stats?.upcoming ?? 0, Icon: Calendar },
    { title: "AI tomonidan bron", value: stats?.ai_booked ?? 0, Icon: Bot },
  ];

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

      <Card>
        <CardHeader>
          <CardTitle>Kelgusi uchrashuvlar</CardTitle>
        </CardHeader>
        <CardContent>
          {!upcoming?.length ? (
            <p className="text-sm text-muted-foreground">
              Uchrashuvlar hali yo&apos;q.
            </p>
          ) : (
            <div className="space-y-2">
              {upcoming.slice(0, 5).map((a) => (
                <div
                  key={a.id}
                  className="flex items-center justify-between rounded-md border p-3 text-sm"
                >
                  <div>
                    <div className="font-medium">{a.patient_name}</div>
                    <div className="text-muted-foreground">{a.service_name}</div>
                  </div>
                  <div className="text-right text-muted-foreground">
                    {new Date(a.starts_at).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
