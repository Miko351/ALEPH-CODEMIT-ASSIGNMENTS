import { useEffect, useState } from 'react';
import { getCurrentUser, logout } from './api/auth.js';
import LoginForm from './components/LoginForm.jsx';
import Dashboard from './components/Dashboard.jsx';
import Message from './components/Message.jsx';

export default function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    getCurrentUser().then(data => { if (active) setUser(data.user); })
      .catch(error => { if (active && error.status !== 401) setError(error.message); })
      .finally(() => { if (active) setChecking(false); });
    return () => { active = false; };
  }, []);
  useEffect(() => {
    const expired = () => { setUser(null); setError('로그인이 만료되었습니다. 다시 로그인해 주세요.'); };
    window.addEventListener('session-expired', expired);
    return () => window.removeEventListener('session-expired', expired);
  }, []);
  async function signOut() {
    setError('');
    try { await logout(); setUser(null); }
    catch (error) { setError(error.message); }
  }
  if (checking) return <main className="session-loading" role="status">로그인 상태를 확인하는 중입니다…</main>;
  return user
    ? <><div className="session-message"><Message>{error}</Message></div><Dashboard user={user} onLogout={signOut} /></>
    : <LoginForm onLogin={user => { setError(''); setUser(user); }} sessionError={error} />;
}
