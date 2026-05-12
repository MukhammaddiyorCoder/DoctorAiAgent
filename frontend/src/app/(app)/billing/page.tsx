"use client";

import { useQuery } from "@tanstack/react-query";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { api } from "@/lib/api";

interface Plan {
  id: number;
  name: string;
  tier: string;
  price_monthly: string;
  currency: string;
  features: string[];
}

export default function BillingPage() {
  const { data: plans = [] } = useQuery({
    queryKey: ["plans"],
    queryFn: async () => (await api.get<Plan[]>("/billing/plans/")).data,
  });

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Billing</h1>
      <p className="text-muted-foreground">
        Klinikangiz uchun mos keladigan tarifni tanlang.
      </p>

      <div className="grid gap-4 md:grid-cols-3">
        {plans.map((plan) => (
          <Card key={plan.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                {plan.name}
                <Badge variant="secondary">{plan.tier}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-3xl font-bold">
                {plan.price_monthly} {plan.currency}
                <span className="text-sm font-normal text-muted-foreground">
                  /oy
                </span>
              </div>
              <ul className="space-y-1 text-sm">
                {plan.features.map((f) => (
                  <li key={f}>• {f}</li>
                ))}
              </ul>
              <Button className="w-full">Tanlash</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
