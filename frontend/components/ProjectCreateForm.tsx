'use client';

import { useState } from 'react';
import { apiClient, ScriptInputMode } from '@/app/api/client';

export function ProjectCreateForm() {
  const [name, setName] = useState('My New Video');
  const [mode, setMode] = useState<ScriptInputMode>('text');
  const [script, setScript] = useState('Opening scene: sunrise over city skyline.');
  const [result, setResult] = useState<string>('');

  async function submit() {
    try {
      const project = await apiClient.createProject({
        name,
        scriptInputMode: mode,
        initialScript: script
      });
      setResult(`Created project ${project.name} (${project.id})`);
    } catch (error) {
      setResult(`Could not create project: ${(error as Error).message}`);
    }
  }

  return (
    <div className="card grid">
      <div className="field">
        <label>Project Name</label>
        <input value={name} onChange={(event) => setName(event.target.value)} />
      </div>
      <div className="field">
        <label>Script Input Mode</label>
        <select value={mode} onChange={(event) => setMode(event.target.value as ScriptInputMode)}>
          <option value="text">Text</option>
          <option value="screenplay">Screenplay</option>
        </select>
      </div>
      <div className="field">
        <label>Initial Script</label>
        <textarea rows={8} value={script} onChange={(event) => setScript(event.target.value)} />
      </div>
      <button onClick={submit}>Create Project</button>
      {result && <small>{result}</small>}
    </div>
  );
}
