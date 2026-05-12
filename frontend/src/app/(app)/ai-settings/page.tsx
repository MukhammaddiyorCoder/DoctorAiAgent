"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useClinic, useUpdateClinic } from "@/hooks/useApi";

type FormValues = {
  ai_enabled: boolean;
  ai_welcome_message: string;
  ai_system_prompt: string;
};

export default function AiSettingsPage() {
  const { data: clinic } = useClinic();
  const update = useUpdateClinic();
  const { register, handleSubmit, reset } = useForm<FormValues>();

  useEffect(() => {
    if (clinic) {
      reset({
        ai_enabled: clinic.ai_enabled,
        ai_welcome_message: clinic.ai_welcome_message,
        ai_system_prompt: clinic.ai_system_prompt,
      });
    }
  }, [clinic, reset]);

  if (!clinic) return null;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">AI Sozlamalari</h1>

      <Card>
        <CardHeader>
          <CardTitle>Chatbot konfiguratsiyasi</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={handleSubmit((v) =>
              update.mutate(v, {
                onSuccess: () => toast.success("Saqlandi"),
                onError: () => toast.error("Xatolik"),
              }),
            )}
            className="space-y-4"
          >
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" {...register("ai_enabled")} />
              AI chatbot yoqilgan
            </label>

            <div className="space-y-1">
              <Label>Salomlashish xabari</Label>
              <Input {...register("ai_welcome_message")} />
            </div>

            <div className="space-y-1">
              <Label>System prompt (bo&apos;sh qoldirilsa default ishlatiladi)</Label>
              <Textarea rows={8} {...register("ai_system_prompt")} />
            </div>

            <Button type="submit" disabled={update.isPending}>
              Saqlash
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Embed kod</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="overflow-x-auto rounded-md bg-muted p-4 text-xs">
{`<script
  src="${typeof window !== "undefined" ? window.location.origin : ""}/widget/chat-widget.js"
  data-clinic="${clinic.slug}"
  data-color="#3B82F6"
  data-position="bottom-right">
</script>`}
          </pre>
        </CardContent>
      </Card>
    </div>
  );
}
