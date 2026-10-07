import { Trash2 } from 'lucide-react';

export default function DeleteConfirmation({ note, onConfirm, onCancel, busy }) {
  return <section className="panel note-detail delete-confirm" aria-label="메모 삭제 확인"><span className="delete-icon"><Trash2 size={25} /></span><h2>이 메모를 삭제할까요?</h2><p className="delete-title">{note.title}</p><p className="muted">삭제한 메모는 되돌릴 수 없습니다.<br />취소하면 메모가 그대로 유지됩니다.</p><div className="form-actions"><button className="secondary" onClick={onCancel} disabled={busy}>취소</button><button className="danger" onClick={onConfirm} disabled={busy}>{busy ? '삭제 중…' : '삭제 확정'}</button></div></section>;
}
