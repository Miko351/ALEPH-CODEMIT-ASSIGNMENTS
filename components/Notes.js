"use client";
import { useRef, useState } from "react";
import Icon from "./Icon";
import DeleteDialog from "./DeleteDialog";

const INITIAL_NOTES = [
  { id: "note-1", content: "배운 내용을 내 말로 정리하기." },
  { id: "note-2", content: "작은 기능부터 하나씩 완성하기." },
];

export default function Notes() {
  const [notes, setNotes] = useState(INITIAL_NOTES);
  const [draft, setDraft] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [deleting, setDeleting] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const input = useRef(null);
  function resetForm() {
    setDraft("");
    setEditingId(null);
    setError("");
  }
  function save(event) {
    event.preventDefault();
    const content = draft.trim();
    setNotice("");
    if (!content) {
      setError("메모 내용을 입력해 주세요. 공백만 입력할 수 없습니다.");
      input.current.focus();
      return;
    }
    if (editingId !== null) {
      setNotes((current) =>
        current.map((note) =>
          note.id === editingId ? { ...note, content } : note,
        ),
      );
      setNotice("메모를 수정했습니다.");
    } else {
      const newNote = { id: crypto.randomUUID(), content };
      setNotes((current) => [...current, newNote]);
      setNotice("새 메모를 등록했습니다.");
    }
    resetForm();
    input.current.focus();
  }
  function edit(note) {
    setEditingId(note.id);
    setDraft(note.content);
    setError("");
    setNotice("");
    input.current.focus();
  }
  function remove() {
    const id = deleting.id;
    setNotes((current) => current.filter((note) => note.id !== id));
    if (editingId === id) resetForm();
    setDeleting(null);
    setNotice("메모를 삭제했습니다.");
  }
  return (
    <div className="notes-workspace">
      <aside className="note-compose">
        <div className="compose-heading">
          <span className="compose-icon">
            <Icon name={editingId !== null ? "edit" : "plus"} />
          </span>
          <div>
            <span className="eyebrow">
              {editingId !== null ? "EDIT YOUR NOTE" : "WRITE SOMETHING"}
            </span>
            <h2>{editingId !== null ? "메모 수정" : "새 메모 작성"}</h2>
          </div>
        </div>
        <form onSubmit={save} noValidate>
          <label htmlFor="note-content">메모 내용</label>
          <textarea
            ref={input}
            id="note-content"
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder="지금 기억하고 싶은 생각을 적어 주세요."
            rows={7}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? "note-error" : "note-hint"}
          />
          <div className="input-foot">
            <small id="note-hint">한 줄이어도 괜찮아요.</small>
            <span>{draft.length}자</span>
          </div>
          {error && (
            <p className="message error" id="note-error" role="alert">
              {error}
            </p>
          )}
          <div className="compose-actions">
            {editingId !== null && (
              <button
                type="button"
                className="button secondary"
                onClick={() => {
                  resetForm();
                  setNotice("수정을 취소했습니다.");
                }}
              >
                수정 취소
              </button>
            )}
            <button className="button primary">
              <Icon name={editingId !== null ? "check" : "plus"} size={16} />
              {editingId !== null ? "수정 저장" : "메모 등록"}
            </button>
          </div>
        </form>
        <div className="compose-tip">
          <Icon name="spark" size={17} />
          <p>
            메모는 지금 열린 화면에 보관됩니다.
            <br />
            새로고침하면 처음의 메모로 돌아와요.
          </p>
        </div>
      </aside>
      <section className="notes-section" aria-labelledby="note-list-heading">
        <div className="list-heading">
          <div>
            <span className="eyebrow">YOUR COLLECTION</span>
            <h2 id="note-list-heading">
              메모 목록 <span className="count-pill">{notes.length}</span>
            </h2>
          </div>
          <span className="list-caption">작은 기록이 모이는 곳</span>
        </div>
        {notice && (
          <p className="message success" role="status">
            {notice}
          </p>
        )}
        <div className="notes-grid">
          {notes.map((note, index) => (
            <article
              key={note.id}
              className={`note-card ${editingId === note.id ? "editing" : ""}`}
              data-note-id={note.id}
            >
              <div className="note-card-top">
                <span className="note-index">
                  NOTE {String(index + 1).padStart(2, "0")}
                </span>
                {editingId === note.id && (
                  <span className="editing-badge">수정 중</span>
                )}
                <Icon name="notebook" size={16} />
              </div>
              <p className="note-content">{note.content}</p>
              <div className="note-card-footer">
                <span>
                  {index < 2 && note.id.startsWith("note-")
                    ? "처음의 기록"
                    : "나의 기록"}
                </span>
                <div>
                  <button
                    className="icon-button"
                    aria-label={`메모 ${index + 1} 수정`}
                    onClick={() => edit(note)}
                  >
                    <Icon name="edit" size={16} />
                  </button>
                  <button
                    className="icon-button delete-button"
                    aria-label={`메모 ${index + 1} 삭제`}
                    onClick={() => {
                      setDeleting(note);
                      setNotice("");
                    }}
                  >
                    <Icon name="trash" size={16} />
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
        {notes.length === 0 && (
          <div className="empty-notes">
            <Icon name="notebook" size={36} />
            <h3>등록된 메모가 없습니다.</h3>
            <p>새로운 생각을 첫 메모로 남겨 보세요.</p>
          </div>
        )}
        <div className="notes-bottom-note">
          <span className="tiny-dot" /> 작성·수정·삭제는 각 메모의 고유한 ID를
          기준으로 처리됩니다.
        </div>
      </section>
      {deleting && (
        <DeleteDialog
          content={deleting.content}
          onConfirm={remove}
          onCancel={() => setDeleting(null)}
        />
      )}
    </div>
  );
}
