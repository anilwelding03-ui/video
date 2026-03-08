'use client';

import { useMemo, useState } from 'react';

export function ScriptEditor() {
  const [script, setScript] = useState('INT. LAB - NIGHT\nA robot painter studies a blank canvas.');
  const helpers = useMemo(
    () => ['Use INT./EXT. markers', 'Include scene mood in parentheticals', 'Keep action lines short'],
    []
  );

  return (
    <div className="card grid">
      <h3 style={{ margin: 0 }}>Script Editor</h3>
      <textarea rows={12} value={script} onChange={(event) => setScript(event.target.value)} />
      <div>
        <strong>Screenplay helper</strong>
        <ul>
          {helpers.map((helper) => (
            <li key={helper}>{helper}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
