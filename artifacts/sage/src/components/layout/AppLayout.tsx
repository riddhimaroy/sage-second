import { Navbar } from "./Navbar";

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="min-h-[100dvh] bg-background text-foreground flex flex-col font-sans">
      <Navbar />
      <main className="flex-1 w-full max-w-4xl mx-auto px-4 pt-24 pb-12">
        {children}
      </main>
    </div>
  );
}
