const exportsList = [
  { key: 'mp4', href: '#', label: 'Download MP4' },
  { key: 'json', href: '#', label: 'Download JSON' },
  { key: 'srt', href: '#', label: 'Download SRT' },
  { key: 'wav', href: '#', label: 'Download WAV' },
  { key: 'prompts', href: '#', label: 'Download prompts' }
];

export function ExportPanel() {
  return (
    <div className="card grid">
      <h3 style={{ margin: 0 }}>Export Downloads</h3>
      {exportsList.map((item) => (
        <a key={item.key} href={item.href}>
          {item.label}
        </a>
      ))}
    </div>
  );
}
