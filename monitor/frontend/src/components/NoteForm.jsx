import { useState } from 'react';
import { Save } from 'lucide-react';
import Message from './Message.jsx';
import { noteStatuses } from './NoteStatus.jsx';

export default function NoteForm({ note, onSave, onCancel, onBusy }) {
  const [title, setTitle] = useState(note?.title || '');
  const [body, setBody] = useState(note?.body || '');
  const [status, setStatus] = useState(note?.status || 'pending');
  const [error, setError] = useState('');
  const [fields, setFields] = useState({});
  const [busy, setBusy] = useState(false);
  async function submit(event) {
    event.preventDefault(); setError(''); setFields({}); setBusy(true); onBusy(true);
    try { await onSave({ title, body, status }); }
    catch (error) { setError(error.message); setFields(error.fields || {}); }
    finally { setBusy(false); onBusy(false); }
  }
  return <section className="panel note-detail"><span className="eyebrow">{note ? `EDIT NOTE / ${note.id}` : 'NEW OBSERVATION'}</span><h2>{note ? '메모 수정' : '새 관찰 메모'}</h2><p className="muted">확인한 요청과 다음에 살필 내용을 기록하세요.</p><form className="note-form" onSubmit={submit} noValidate>
    <label htmlFor="note-title">제목</label><input id="note-title" value={title} onChange={e => setTitle(e.target.value)} placeholder="예: 없는 게시글 요청 확인" disabled={busy} aria-invalid={Boolean(fields.title)} aria-describedby={fields.title ? 'title-error' : undefined} />{fields.title && <small className="field-error" id="title-error">{fields.title}</small>}
    <label htmlFor="note-body">내용</label><textarea id="note-body" value={body} onChange={e => setBody(e.target.value)} placeholder="요청 경로, 응답 상태와 관찰한 내용을 적어 주세요." rows={8} disabled={busy} aria-invalid={Boolean(fields.body)} aria-describedby={fields.body ? 'body-error' : undefined} />{fields.body && <small className="field-error" id="body-error">{fields.body}</small>}
    <label htmlFor="note-status">처리 상태</label><select id="note-status" value={status} onChange={e => setStatus(e.target.value)} disabled={busy} aria-invalid={Boolean(fields.status)}>{noteStatuses.map(item => <option key={item.value} value={item.value}>{item.label}</option>)}</select>{fields.status && <small className="field-error">{fields.status}</small>}
    <Message>{error}</Message><div className="form-actions"><button type="button" className="secondary" onClick={onCancel} disabled={busy}>취소</button><button className="primary" disabled={busy}><Save size={16} />{busy ? '저장 중…' : '메모 저장'}</button></div>
  </form></section>;
}
