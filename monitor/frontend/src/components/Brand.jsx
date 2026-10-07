import { Activity } from 'lucide-react';
export default function Brand({ compact = false }) {
  return <div className="brand"><span className="brand-icon"><Activity size={23} /></span><div><strong>사이 워치<span className="brand-dot">.</span></strong>{!compact && <small>MINI WATCH / MONITOR</small>}</div></div>;
}
