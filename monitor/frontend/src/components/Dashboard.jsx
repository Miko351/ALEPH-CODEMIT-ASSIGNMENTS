import { useEffect, useRef, useState } from 'react';
import { Activity, ArrowUpRight, RefreshCw, LogOut, LayoutDashboard, AlertCircle, NotebookPen } from 'lucide-react';
import { getEvents } from '../api/events.js';
import { getNotes, getNote, createNote, updateNote, deleteNote } from '../api/notes.js';
import Brand from './Brand.jsx';
import EventList from './EventList.jsx';
import NoteList from './NoteList.jsx';
import NoteDetail from './NoteDetail.jsx';
import NoteForm from './NoteForm.jsx';
import DeleteConfirmation from './DeleteConfirmation.jsx';
import Message from './Message.jsx';

export default function Dashboard({ user, onLogout }) {
  const [events, setEvents] = useState([]), [notes, setNotes] = useState([]);
  const [selected, setSelected] = useState(null), [view, setView] = useState('detail');
  const [loading, setLoading] = useState(false), [detailLoading, setDetailLoading] = useState(false), [busy, setBusy] = useState(false);
  const [eventsError, setEventsError] = useState(''), [notesError, setNotesError] = useState(''), [error, setError] = useState(''), [notice, setNotice] = useState('');
  const [query, setQuery] = useState(''), [status, setStatus] = useState('all'), [refreshed, setRefreshed] = useState(null);
  const selectionVersion = useRef(0);

  async function loadLists() {
    setLoading(true); setEventsError(''); setNotesError('');
    const [eventResult, noteResult] = await Promise.allSettled([getEvents(), getNotes()]);
    if (eventResult.status === 'fulfilled') setEvents(eventResult.value.events);
    else setEventsError(eventResult.reason.message);
    if (noteResult.status === 'fulfilled') setNotes(noteResult.value.notes);
    else setNotesError(noteResult.reason.message);
    if (eventResult.status === 'fulfilled' && noteResult.status === 'fulfilled') setRefreshed(new Date());
    setLoading(false);
  }
  useEffect(() => { loadLists(); }, []);

  async function select(id) {
    const version = ++selectionVersion.current;
    setError(''); setNotice(''); setView('detail'); setDetailLoading(true);
    try { const data = await getNote(id); if (version === selectionVersion.current) setSelected(data.note); }
    catch (error) { if (version === selectionVersion.current) { setError(error.message); setSelected(null); } }
    finally { if (version === selectionVersion.current) setDetailLoading(false); }
  }
  async function refresh() {
    setError(''); setNotice('');
    await loadLists();
    if (selected && view === 'detail') await select(selected.id);
  }
  async function save(values) {
    const data = view === 'edit' ? await updateNote(selected.id, values) : await createNote(values);
    setSelected(data.note); setView('detail'); setError(''); setNotice('메모를 저장했습니다.');
    await loadLists();
  }
  async function confirmDelete() {
    setBusy(true); setError(''); setNotice('');
    try { await deleteNote(selected.id); setSelected(null); setView('detail'); setNotice('메모를 삭제했습니다.'); await loadLists(); }
    catch (error) { setError(error.message); }
    finally { setBusy(false); }
  }
  function newNote() { ++selectionVersion.current; setDetailLoading(false); setView('new'); setError(''); setNotice(''); }
  function changeView(next) { setView(next); setError(''); setNotice(''); }
  const filtered = events.filter(event => event.path.toLowerCase().includes(query.trim().toLowerCase()) && (
    status === 'all' || status === 'error' && event.status_code >= 400 || status === 'success' && event.status_code >= 200 && event.status_code < 400 || status === '404' && event.status_code === 404 || status === '500' && event.status_code >= 500
  ));
  const errorCount = filtered.filter(event => event.status_code >= 400).length;
  const disabled = busy || detailLoading;
  return <div className="dashboard-shell"><aside className="sidebar"><Brand /><div className="sidebar-label">WORKSPACE</div><a className="nav-current" href="#dashboard"><LayoutDashboard size={19} />감시 대시보드<span>01</span></a><a className="nav-link" href={import.meta.env.VITE_GENERAL_URL || 'http://127.0.0.1:5100'} target="_blank" rel="noreferrer"><ArrowUpRight size={19} />일반 게시판 열기</a><div className="sidebar-note"><span className="status-dot" /><strong>기록은 다음 관찰의 시작</strong><p>서비스의 작은 변화들을<br />차곡차곡 남겨 보세요.</p></div><div className="sidebar-user"><span className="avatar">{user.name.slice(0, 1)}</span><div><strong>{user.name}</strong><small>운영자 · {user.username}</small></div><button aria-label="로그아웃" className="icon-button" onClick={onLogout}><LogOut size={18} /></button></div></aside>
    <main className="dashboard-main" id="dashboard"><header className="topbar"><span>WORKSPACE <span className="slash">/</span> 감시 대시보드</span><span className="topbar-status"><span className="status-dot" /> MINI WATCH</span></header><div className="main-content"><div className="page-heading"><div><span className="eyebrow">MONITORING OVERVIEW</span><h1>오늘의 서비스 관찰</h1><p>{user.name}님, 요청의 흐름을 살피고 관찰을 기록해 보세요.</p></div><div className="refresh-group"><button className="secondary refresh-button" onClick={refresh} disabled={loading || disabled}><RefreshCw size={16} className={loading ? 'spinning' : ''} />{loading ? '조회 중…' : '목록 새로고침'}</button><small>{refreshed ? `마지막 조회 ${refreshed.toLocaleTimeString('ko-KR', { hour12: false })}` : '최신 기록을 불러옵니다'}</small></div></div>
      <div className="stats"><div className="stat-card"><div><span>전체 요청 수</span><strong>{filtered.length}<small>건</small></strong><p>현재 검색 조건에 맞는 조회 기록</p></div><span className="stat-icon"><Activity size={21} /></span></div><div className="stat-card"><div><span>오류 요청 수</span><strong>{errorCount}<small>건</small></strong><p>현재 목록 중 상태 코드 400 이상</p></div><span className="stat-icon amber"><AlertCircle size={21} /></span></div><div className="stat-card"><div><span>관찰 메모</span><strong>{notes.length}<small>개</small></strong><p>기록하고 이어 가는 나의 관찰</p></div><span className="stat-icon"><NotebookPen size={21} /></span></div></div>
      <EventList events={filtered} totalCount={events.length} query={query} status={status} onQuery={setQuery} onStatus={setStatus} onReset={() => { setQuery(''); setStatus('all'); }} loading={loading} error={eventsError} />
      <Message>{error}</Message><Message type="success">{notice}</Message><div className="notes-grid"><NoteList notes={notes} selectedId={selected?.id} onSelect={select} onNew={newNote} loading={loading} disabled={disabled} error={notesError} />
        {(view === 'new' || view === 'edit') ? <NoteForm key={view + (selected?.id || '')} note={view === 'edit' ? selected : null} onSave={save} onCancel={() => changeView('detail')} onBusy={setBusy} /> : view === 'delete' && selected ? <DeleteConfirmation note={selected} onConfirm={confirmDelete} onCancel={() => changeView('detail')} busy={busy} /> : <NoteDetail note={selected} onEdit={() => changeView('edit')} onDelete={() => changeView('delete')} loading={detailLoading} />}
      </div><footer className="page-footer"><span>사이 워치 · MINI WATCH</span><span>관찰은 가볍게, 기록은 선명하게.</span></footer></div></main>
  </div>;
}
