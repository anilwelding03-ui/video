'use client';

import { useState } from 'react';
import { Scene } from '@/app/api/client';
import { CollapsibleCard } from '@/components/ui/collapsible-card';

const initialScenes: Scene[] = [
  {
    id: 'scene-1',
    title: 'Arrival',
    summary: 'Hero reaches the cliff edge at sunrise.',
    shots: [
      { id: 'shot-1', label: 'Wide establishing', durationSeconds: 4, prompt: 'golden hour mountain panorama' }
    ]
  }
];

export function SceneInspector() {
  const [scenes, setScenes] = useState(initialScenes);

  return (
    <CollapsibleCard title="Scene Inspector">
      <div className="grid">
        {scenes.map((scene) => (
          <div key={scene.id} className="card">
            <h4 style={{ marginTop: 0 }}>{scene.title}</h4>
            <p>{scene.summary}</p>
            {scene.shots.map((shot) => (
              <div key={shot.id} className="field">
                <label>
                  {shot.label} · {shot.durationSeconds}s
                </label>
                <textarea
                  rows={2}
                  value={shot.prompt}
                  onChange={(event) => {
                    const next = scenes.map((item) =>
                      item.id === scene.id
                        ? {
                            ...item,
                            shots: item.shots.map((currentShot) =>
                              currentShot.id === shot.id
                                ? {
                                    ...currentShot,
                                    prompt: event.target.value
                                  }
                                : currentShot
                            )
                          }
                        : item
                    );
                    setScenes(next);
                  }}
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    </CollapsibleCard>
  );
}
