import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "RouteSetu",
  description: "Find connected GSRTC-style bus journeys when no direct bus exists.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
