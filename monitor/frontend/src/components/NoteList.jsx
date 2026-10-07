import { Plus, ChevronRight, StickyNote } from 'lucide-react';
import Message from './Message.jsx';
import NoteStatus from './NoteStatus.jsx';

export default function NoteList({ notes, selectedId, onSelect, onNew, loading, disabled, error }) {
  return <section className="panel note-list" aria-labelledby="notes-heading"><div className="panel-heading"><div><span className="eyebrow">OBSERVATION NOTES</span><h2 id="notes-heading">관찰 메모 <span className="count">{notes.length}</span></h2></div><button className="primary small" onClick={onNew} disabled={disabled}><Plus size={16} /> 새 메모</button></div><Message>{error}</Message>
    <div className="note-items">{notes.map(note => <button key={note.id} className={`note-item ${selectedId === note.id ? 'selected' : ''}`} onClick={() => onSelect(note.id)} disabled={disabled}><span className="note-number">#{note.id}</span><span className="note-item-copy"><strong>{note.title}</strong><small><NoteStatus status={note.status} /> {new Date(note.updated_at).toLocaleDateString('ko-KR')} 업데이트</small></span><ChevronRight size={16} /></button>)}</div>
    {!notes.length && !error && <div className="empty-state"><StickyNote size={29} /><span>{loading ? '메모를 불러오는 중입니다…' : '아직 관찰 메모가 없습니다.'}</span><small>첫 번째 관찰을 기록해 보세요.</small></div>}
  </section>;
}
