import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "회원가입 | ALEPH",
  description: "새로운 시작을 위한 ALEPH 회원가입",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
