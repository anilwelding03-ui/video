import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Video Studio',
  description: 'Project creation, script editing, timeline tuning, and exports'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
