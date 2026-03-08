import { TimelineEditor } from '@/components/TimelineEditor';

export default function TimelinePage({ params }: { params: { id: string } }) {
  return (
    <main className="container grid">
      <h1>Timeline · {params.id}</h1>
      <TimelineEditor />
    </main>
  );
}
