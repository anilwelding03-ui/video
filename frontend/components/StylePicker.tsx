'use client';

import { useState } from 'react';

const presets = ['cinematic', 'anime', 'documentary', 'photoreal'];

export function StylePicker() {
  const [style, setStyle] = useState(presets[0]);
  const [custom, setCustom] = useState('');

  return (
    <div className="card grid">
      <h3 style={{ margin: 0 }}>Style Picker</h3>
      <div className="field">
        <label>Preset</label>
        <select value={style} onChange={(event) => setStyle(event.target.value)}>
          {presets.map((preset) => (
            <option key={preset} value={preset}>
              {preset}
            </option>
          ))}
        </select>
      </div>
      <div className="field">
        <label>Custom style override</label>
        <input value={custom} onChange={(event) => setCustom(event.target.value)} placeholder="e.g. vintage 16mm, warm grain" />
      </div>
    </div>
  );
}
