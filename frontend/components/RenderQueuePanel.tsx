'use client';

import { useState } from 'react';
import { apiClient, JobStatus, RenderMode } from '@/app/api/client';
import { ProgressBar } from '@/components/ui/progress-bar';
import { StatusBadge } from '@/components/ui/status-badge';

interface QueueItem {
  id: string;
  status: JobStatus;
  progress: number;
  mode: RenderMode;
}

export function RenderQueuePanel({ projectId }: { projectId: string }) {
  const [mode, setMode] = useState<RenderMode>('standard');
  const [note, setNote] = useState('');
  const [jobs, setJobs] = useState<QueueItem[]>([
    { id: 'job-1001', status: 'rendering', progress: 62, mode: 'standard' },
    { id: 'job-1000', status: 'complete', progress: 100, mode: 'draft' }
  ]);

  async function queueRender() {
    try {
      const job = await apiClient.enqueueRender(projectId, mode);
      setJobs([{ id: job.id, status: job.status, progress: job.progressPercent, mode: job.mode }, ...jobs]);
      setNote(`Render requested in ${mode} mode.`);
    } catch (error) {
      setNote(`Render could not be queued. ${String((error as Error).message)}. Check provider configuration in setup docs.`);
    }
  }

  return (
    <div className="card grid">
      <h3 style={{ margin: 0 }}>Render Queue</h3>
      <div className="field">
        <label>Render mode</label>
        <select value={mode} onChange={(event) => setMode(event.target.value as RenderMode)}>
          <option value="draft">draft</option>
          <option value="standard">standard</option>
          <option value="high-quality">high-quality</option>
        </select>
      </div>
      <button onClick={queueRender}>Queue render ({mode})</button>
      {note && <small>{note}</small>}
      {jobs.map((job) => (
        <div key={job.id} className="grid" style={{ gap: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <small>
              {job.id} · {job.mode}
            </small>
            <StatusBadge label={job.status} tone={job.status} />
          </div>
          <ProgressBar value={job.progress} />
        </div>
      ))}
    </div>
  );
}
