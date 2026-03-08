'use client';

import { useEffect, useState } from 'react';
import { apiClient, ProviderStatus } from '@/app/api/client';
import { StatusBadge } from '@/components/ui/status-badge';

const fallback: ProviderStatus[] = [
  { provider: 'openai', available: false, guidance: 'Set OPENAI_API_KEY in backend .env and restart services.' },
  { provider: 'elevenlabs', available: false, guidance: 'Set ELEVENLABS_API_KEY in backend .env and restart worker.' },
  { provider: 'runway', available: false, guidance: 'Set RUNWAY_API_KEY and verify provider endpoint availability.' }
];

export function ProviderStatusNotice() {
  const [providers, setProviders] = useState<ProviderStatus[]>(fallback);

  useEffect(() => {
    apiClient
      .getProviderStatuses()
      .then(setProviders)
      .catch(() => setProviders(fallback));
  }, []);

  return (
    <div className="card grid">
      <h3 style={{ margin: 0 }}>Provider status</h3>
      {providers.map((provider) => (
        <div key={provider.provider}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <strong>{provider.provider}</strong>
            <StatusBadge
              label={provider.available ? 'available' : 'setup needed'}
              tone={provider.available ? 'ok' : 'warning'}
            />
          </div>
          {!provider.available && <small>{provider.guidance}</small>}
        </div>
      ))}
    </div>
  );
}
