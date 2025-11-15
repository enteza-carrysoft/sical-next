// src/app/layout.tsx
import "./globals.css";
import type { Metadata } from "next";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";

export const metadata: Metadata = {
  title: "Tramitador de Facturas - SICAL Next",
  description: "MVP de tramitación de facturas sobre SICAL",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="h-screen bg-slate-100">
        <div className="flex h-screen">
          <Sidebar />
          <div className="flex flex-col flex-1">
            <Topbar />
            <main className="flex-1 overflow-y-auto p-6">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
