"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";

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
import { useLogin } from "@/hooks/useAuth";

type FormValues = { email: string; password: string };

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormValues>({
    defaultValues: { email: "demo@doctor.com", password: "demo1234" },
  });
  const login = useLogin();

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Kirish</CardTitle>
          <CardDescription>Hisobingizga kiring</CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) => login.mutate(v))}
            className="space-y-4"
          >
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                {...register("email", { required: true })}
              />
              {errors.email && (
                <p className="text-xs text-destructive">Email majburiy</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Parol</Label>
              <Input
                id="password"
                type="password"
                {...register("password", { required: true })}
              />
            </div>

            <Button type="submit" className="w-full" disabled={login.isPending}>
              {login.isPending ? "Kiryapti..." : "Kirish"}
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              Hisobingiz yo&apos;qmi?{" "}
              <Link href="/register" className="text-primary hover:underline">
                Ro&apos;yxatdan o&apos;ting
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
