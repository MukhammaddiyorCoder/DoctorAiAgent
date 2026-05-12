"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppointmentTrend } from "@/hooks/useApi";

export function TrendChart() {
  const { data = [], isLoading } = useAppointmentTrend(14);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Oxirgi 14 kun</CardTitle>
      </CardHeader>
      <CardContent className="h-72">
        {isLoading ? (
          <p className="text-muted-foreground">Yuklanmoqda...</p>
        ) : !data.length ? (
          <p className="text-muted-foreground">Ma&apos;lumot yo&apos;q.</p>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 10, bottom: 0, left: -20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="date"
                fontSize={12}
                tickFormatter={(d) => d.slice(5)}
              />
              <YAxis fontSize={12} allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="count"
                name="Jami"
                stroke="hsl(var(--primary))"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="ai"
                name="AI"
                stroke="#10b981"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
