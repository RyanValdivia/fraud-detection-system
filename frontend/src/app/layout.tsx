import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Fraud Detection System",
  description: "Panel de scoring de fraude en tiempo real",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="es"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <header className="border-b">
          <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-4">
            <span className="font-semibold tracking-tight">
              Fraud Detection System
            </span>
            <span className="text-xs text-muted-foreground">API v0.1.0</span>
          </div>
        </header>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
