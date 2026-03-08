import { RenderQueuePanel } from '@/components/RenderQueuePanel';
import { SceneInspector } from '@/components/SceneInspector';
import { ScriptEditor } from '@/components/ScriptEditor';
import { StylePicker } from '@/components/StylePicker';

export default function EditorPage({ params }: { params: { id: string } }) {
  return (
    <main className="container grid">
      <h1>Editor · {params.id}</h1>
      <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
        <ScriptEditor />
        <StylePicker />
      </div>
      <SceneInspector />
      <RenderQueuePanel projectId={params.id} />
    </main>
  );
}
