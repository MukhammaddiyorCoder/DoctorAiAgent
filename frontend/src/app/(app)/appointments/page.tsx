"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppointments } from "@/hooks/useApi";
import type { AppointmentStatus } from "@/types";

const statusVariant: Record<AppointmentStatus, "default" | "success" | "destructive" | "warning" | "secondary"> = {
  pending: "warning",
  confirmed: "success",
  cancelled: "destructive",
  completed: "secondary",
  no_show: "destructive",
};

export default function AppointmentsPage() {
  const { data: appointments = [], isLoading } = useAppointments();

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Uchrashuvlar</h1>

      <Card>
        <CardHeader>
          <CardTitle>Barcha uchrashuvlar</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-muted-foreground">Yuklanmoqda...</p>
          ) : !appointments.length ? (
            <p className="text-muted-foreground">
              Hali uchrashuvlar mavjud emas.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b text-muted-foreground">
                  <tr>
                    <th className="pb-2 pr-4">Bemor</th>
                    <th className="pb-2 pr-4">Xizmat</th>
                    <th className="pb-2 pr-4">Vaqt</th>
                    <th className="pb-2 pr-4">Manba</th>
                    <th className="pb-2">Holat</th>
                  </tr>
                </thead>
                <tbody>
                  {appointments.map((a) => (
                    <tr key={a.id} className="border-b">
                      <td className="py-2 pr-4">{a.patient_name}</td>
                      <td className="py-2 pr-4">{a.service_name}</td>
                      <td className="py-2 pr-4">
                        {new Date(a.starts_at).toLocaleString()}
                      </td>
                      <td className="py-2 pr-4 capitalize">{a.source}</td>
                      <td className="py-2">
                        <Badge variant={statusVariant[a.status]}>{a.status}</Badge>
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
