import { useState } from 'react';
import { ArrowRight, ScanLine, NotebookPen, Radio } from 'lucide-react';
import { login } from '../api/auth.js';
import Brand from './Brand.jsx';
import Message from './Message.jsx';

export default function LoginForm({ onLogin, sessionError }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  async function submit(event) {
    event.preventDefault();
    setError(''); setBusy(true);
    try { const data = await login(username, password); onLogin(data.user); }
    catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }
  return <main className="login-page">
    <section className="login-story"><Brand /><div className="story-copy"><span className="eyebrow">작은 신호도 놓치지 않도록</span><h1>서비스의 흐름을 읽고,<br /><em>관찰을 기록하세요.</em></h1><p>게시판에서 발생한 요청을 한눈에 살피고<br />확인한 내용을 관찰 메모로 남기는 공간입니다.</p><div className="signal-art" aria-hidden="true"><Radio size={44} /><div className="signal-line" /><span className="signal-chip">GET /board/3 <b>200</b></span><span className="signal-chip secondary">관찰 기록이 모이는 곳</span></div><div className="story-features"><span><ScanLine size={18} /> 실제 요청 기록</span><span><NotebookPen size={18} /> 나의 관찰 메모</span></div></div><small className="story-footer">사이 게시판과 함께하는 작은 관제실</small></section>
    <section className="login-panel"><div className="login-card"><span className="eyebrow">OPERATOR ACCESS</span><h2>운영자 로그인</h2><p className="muted">계정으로 로그인해 감시 대시보드를 열어 주세요.</p><form onSubmit={submit} noValidate>
      <label htmlFor="username">아이디</label><input id="username" name="username" autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} placeholder="운영자 아이디" disabled={busy} />
      <label htmlFor="password">비밀번호</label><input id="password" name="password" type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} placeholder="비밀번호 입력" disabled={busy} />
      <Message>{error || sessionError}</Message><button className="primary login-submit" disabled={busy}>{busy ? '계정 확인 중…' : '대시보드 열기'}<ArrowRight size={18} /></button>
    </form><div className="login-hint"><span className="status-dot" /> 일반 서비스의 기록과 메모를 한곳에서</div></div><small className="login-bottom">MINI WATCH · 서비스 관찰 대시보드</small></section>
  </main>;
}
