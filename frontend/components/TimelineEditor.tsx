'use client';

import { useState } from 'react';
import { CollapsibleCard } from '@/components/ui/collapsible-card';

export function TimelineEditor() {
  const [sceneOrder, setSceneOrder] = useState('scene-1,scene-2,scene-3');
  const [duration, setDuration] = useState(4);
  const [subtitles, setSubtitles] = useState(true);
  const [voice, setVoice] = useState(80);
  const [music, setMusic] = useState(35);

  return (
    <CollapsibleCard title="Timeline Editor">
      <div className="grid">
        <div className="field">
          <label>Scene order (comma separated)</label>
          <input value={sceneOrder} onChange={(event) => setSceneOrder(event.target.value)} />
        </div>
        <div className="field">
          <label>Clip duration: {duration}s</label>
          <input type="range" min={2} max={12} value={duration} onChange={(event) => setDuration(Number(event.target.value))} />
        </div>
        <label>
          <input type="checkbox" checked={subtitles} onChange={(event) => setSubtitles(event.target.checked)} /> Subtitle toggle
        </label>
        <div className="field">
          <label>Voice volume: {voice}%</label>
          <input type="range" min={0} max={100} value={voice} onChange={(event) => setVoice(Number(event.target.value))} />
        </div>
        <div className="field">
          <label>Music volume: {music}%</label>
          <input type="range" min={0} max={100} value={music} onChange={(event) => setMusic(Number(event.target.value))} />
        </div>
      </div>
    </CollapsibleCard>
  );
}
