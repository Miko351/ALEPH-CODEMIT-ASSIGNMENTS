"use client";
import { useEffect, useRef } from "react";
import Icon from "./Icon";

export default function DeleteDialog({
  content,
  onConfirm,
  onCancel,
  busy = false,
}) {
  const reference = useRef(null);
  useEffect(() => {
    const dialog = reference.current;
    dialog.showModal();
    return () => dialog.close();
  }, []);
  return (
    <dialog
      ref={reference}
      className="delete-dialog"
      onCancel={(event) => {
        event.preventDefault();
        if (!busy) onCancel();
      }}
      aria-labelledby="delete-heading"
    >
      <span className="delete-emblem">
        <Icon name="trash" size={24} />
      </span>
      <h2 id="delete-heading">이 메모를 삭제할까요?</h2>
      <p className="delete-preview">{content}</p>
      <p className="muted">
        취소하면 메모는 그대로 남습니다.
        <br />
        삭제한 메모는 되돌릴 수 없습니다.
      </p>
      <div className="dialog-actions">
        <button className="button secondary" onClick={onCancel} disabled={busy}>
          취소
        </button>
        <button className="button danger" onClick={onConfirm} disabled={busy}>
          {busy ? "삭제 중…" : "삭제 확정"}
        </button>
      </div>
    </dialog>
  );
}
