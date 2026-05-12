import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <div className="max-w-2xl space-y-6">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Doctor AI Agent
        </h1>
        <p className="text-lg text-muted-foreground">
          Klinikangiz uchun aqlli AI assistent. Bemorlar uchrashuvlarni
          chatbot orqali bron qilishadi, siz esa boshqaruv paneli bilan
          kliniкangizni oson boshqarasiz.
        </p>
        <div className="flex justify-center gap-3">
          <Button asChild size="lg">
            <Link href="/register">Boshlash</Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link href="/login">Kirish</Link>
          </Button>
        </div>
      </div>
    </main>
  );
}
