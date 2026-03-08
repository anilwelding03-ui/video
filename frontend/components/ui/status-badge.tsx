import { JobStatus } from '@/app/api/client';

const COLORS: Record<JobStatus | 'ok' | 'warning', string> = {
  queued: '#646cff',
  rendering: '#17a2b8',
  complete: '#28a745',
  failed: '#dc3545',
  ok: '#28a745',
  warning: '#f39c12'
};

export function StatusBadge({ label, tone }: { label: string; tone: JobStatus | 'ok' | 'warning' }) {
  return (
    <span
      style={{
        background: `${COLORS[tone]}22`,
        color: COLORS[tone],
        border: `1px solid ${COLORS[tone]}77`,
        borderRadius: '999px',
        padding: '2px 10px',
        fontSize: 12,
        fontWeight: 600
      }}
    >
      {label}
    </span>
  );
}
