'use client';

import { useState } from 'react';

export function CollapsibleCard({
  title,
  defaultOpen = true,
  children
}: {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <section className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>{title}</h3>
        <button onClick={() => setOpen((value) => !value)}>{open ? 'Collapse' : 'Expand'}</button>
      </div>
      {open && <div style={{ marginTop: 12 }}>{children}</div>}
    </section>
  );
}
