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
import { useRegister } from "@/hooks/useAuth";

type FormValues = {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  clinic_name?: string;
};

export default function RegisterPage() {
  const { register, handleSubmit } = useForm<FormValues>();
  const signup = useRegister();

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Ro&apos;yxatdan o&apos;tish</CardTitle>
          <CardDescription>Yangi klinika hisobini yarating</CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) => signup.mutate(v))}
            className="space-y-4"
          >
            <div className="space-y-2">
              <Label htmlFor="clinic_name">Klinika nomi</Label>
              <Input id="clinic_name" {...register("clinic_name")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="full_name">To&apos;liq ism</Label>
              <Input id="full_name" {...register("full_name", { required: true })} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" {...register("email", { required: true })} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Telefon</Label>
              <Input id="phone" {...register("phone")} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Parol</Label>
              <Input
                id="password"
                type="password"
                {...register("password", { required: true, minLength: 8 })}
              />
            </div>

            <Button type="submit" className="w-full" disabled={signup.isPending}>
              {signup.isPending ? "Yaratilmoqda..." : "Ro'yxatdan o'tish"}
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              Hisobingiz bormi?{" "}
              <Link href="/login" className="text-primary hover:underline">
                Kirish
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
