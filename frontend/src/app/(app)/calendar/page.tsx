"use client";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppointments } from "@/hooks/useApi";

export default function CalendarPage() {
  const { data: appointments = [] } = useAppointments();

  const events = appointments.map((a) => ({
    id: String(a.id),
    title: `${a.patient_name} — ${a.service_name}`,
    start: a.starts_at,
    end: a.ends_at,
    color:
      a.status === "confirmed"
        ? "#10b981"
        : a.status === "pending"
          ? "#f59e0b"
          : a.status === "cancelled"
            ? "#ef4444"
            : "#6366f1",
  }));

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Kalendar</h1>
      <Card>
        <CardHeader>
          <CardTitle>Uchrashuvlar jadvali</CardTitle>
        </CardHeader>
        <CardContent>
          <FullCalendar
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="timeGridWeek"
            headerToolbar={{
              left: "prev,next today",
              center: "title",
              right: "dayGridMonth,timeGridWeek,timeGridDay",
            }}
            events={events}
            height="auto"
            allDaySlot={false}
            locale="en"
          />
        </CardContent>
      </Card>
    </div>
  );
}
