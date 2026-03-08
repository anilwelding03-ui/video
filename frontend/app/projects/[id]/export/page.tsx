import { ExportPanel } from '@/components/ExportPanel';

export default function ExportPage({ params }: { params: { id: string } }) {
  return (
    <main className="container grid">
      <h1>Export · {params.id}</h1>
      <ExportPanel />
    </main>
  );
}
