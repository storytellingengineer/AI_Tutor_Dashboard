import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Tutor",
  description: "A production-ready AI learning workspace",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "Arial, sans-serif", background: "#f6f7fb" }}>
        {children}
      </body>
    </html>
  );
}
