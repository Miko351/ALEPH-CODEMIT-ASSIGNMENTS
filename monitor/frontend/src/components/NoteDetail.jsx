import { Pencil, Trash2, NotebookPen } from 'lucide-react';
import NoteStatus from './NoteStatus.jsx';

export default function NoteDetail({ note, onEdit, onDelete, loading }) {
  if (loading) return <section className="panel note-detail"><div className="empty-state">메모 상세를 불러오는 중입니다…</div></section>;
  if (!note) return <section className="panel note-detail"><div className="detail-placeholder"><NotebookPen size={34} /><h3>관찰을 이어 가는 공간</h3><p>목록에서 메모를 선택하거나<br />새 메모를 작성해 주세요.</p></div></section>;
  return <section className="panel note-detail" aria-label="메모 상세"><div className="detail-top"><span className="eyebrow">NOTE / {String(note.id).padStart(3, '0')}</span><div className="detail-actions"><button className="text-button" onClick={onEdit}><Pencil size={15} /> 수정</button><button className="text-button danger-text" onClick={onDelete}><Trash2 size={15} /> 삭제</button></div></div><h2>{note.title}</h2><div className="detail-status"><NoteStatus status={note.status} /></div><span className="detail-date">마지막 수정 {new Date(note.updated_at).toLocaleString('ko-KR')}</span><div className="note-body">{note.body}</div><div className="detail-footnote">기록한 관찰은 다음 확인의 출발점이 됩니다.</div></section>;
}
