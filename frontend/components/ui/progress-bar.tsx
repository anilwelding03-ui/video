export function ProgressBar({ value }: { value: number }) {
  return (
    <div style={{ background: '#2c3444', borderRadius: 999, height: 10, width: '100%' }}>
      <div
        style={{
          background: '#4f7cff',
          width: `${Math.max(0, Math.min(value, 100))}%`,
          borderRadius: 999,
          height: '100%',
          transition: 'width 0.2s ease'
        }}
      />
    </div>
  );
}
