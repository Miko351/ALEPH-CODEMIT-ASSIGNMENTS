import { useState } from 'react';
import LoginForm from './components/LoginForm.jsx';
import Dashboard from './components/Dashboard.jsx';

export default function App() {
  const [user, setUser] = useState(null);
  return user
    ? <Dashboard user={user} onLogout={() => setUser(null)} />
    : <LoginForm onLogin={setUser} />;
}
