"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Calendar,
  CreditCard,
  LayoutDashboard,
  MessageSquare,
  Settings,
  Stethoscope,
  Users,
  UserCog,
  Wrench,
} from "lucide-react";

import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/calendar", label: "Kalendar", icon: Calendar },
  { href: "/appointments", label: "Uchrashuvlar", icon: Stethoscope },
  { href: "/patients", label: "Bemorlar", icon: Users },
  { href: "/services", label: "Xizmatlar", icon: Wrench },
  { href: "/ai-settings", label: "AI Sozlamalari", icon: MessageSquare },
  { href: "/settings", label: "Sozlamalar", icon: Settings },
  { href: "/billing", label: "Billing", icon: CreditCard },
  { href: "/profile", label: "Profil", icon: UserCog },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="hidden w-64 flex-col border-r bg-card md:flex">
      <div className="flex h-16 items-center border-b px-6 text-lg font-semibold">
        Doctor AI
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href || pathname.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
