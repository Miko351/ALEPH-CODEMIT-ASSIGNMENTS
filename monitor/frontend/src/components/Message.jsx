export default function Message({ children, type = 'error' }) {
  if (!children) return null;
  return <div className={`message ${type}`} role={type === 'error' ? 'alert' : 'status'}>{children}</div>;
}
