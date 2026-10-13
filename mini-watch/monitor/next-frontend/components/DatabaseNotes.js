"use client";
import { useEffect, useState } from "react";
import * as auth from "../api/auth";
import * as api from "../api/notes";
import Icon from "./Icon";
import DeleteDialog from "./DeleteDialog";

const statuses = {
  pending: "확인 전",
  in_progress: "확인 중",
  completed: "완료",
};
export default function DatabaseNotes() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [notes, setNotes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [status, setStatus] = useState("pending");
  const [deleting, setDeleting] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [fields, setFields] = useState({});
  const [notice, setNotice] = useState("");

  async function reload() {
    const data = await api.listNotes();
    setNotes(data.notes);
  }
  useEffect(() => {
    let active = true;
    auth
      .currentUser()
      .then(async (data) => {
        if (!active) return;
        setUser(data.user);
        try {
          const response = await api.listNotes();
          if (active) setNotes(response.notes);
        } catch (error) {
          if (active) setError(error.message);
        }
      })
      .catch((error) => {
        if (active && error.status !== 401) setError(error.message);
      })
      .finally(() => {
        if (active) setChecking(false);
      });
    return () => {
      active = false;
    };
  }, []);
  useEffect(() => {
    const expired = () => {
      setUser(null);
      setError("로그인이 만료되었습니다. 다시 로그인해 주세요.");
    };
    window.addEventListener("session-expired", expired);
    return () => window.removeEventListener("session-expired", expired);
  }, []);
  function resetForm() {
    setEditingId(null);
    setTitle("");
    setBody("");
    setStatus("pending");
    setFields({});
  }
  async function signIn(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const data = await auth.login(username, password);
      setUser(data.user);
      setPassword("");
      await reload();
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }
  async function signOut() {
    setBusy(true);
    setError("");
    try {
      await auth.logout();
      setUser(null);
      setSelected(null);
      setNotes([]);
      resetForm();
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }
  async function select(id) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const data = await api.findNote(id);
      setSelected(data.note);
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }
  function edit() {
    setEditingId(selected.id);
    setTitle(selected.title);
    setBody(selected.body);
    setStatus(selected.status);
    setError("");
    setNotice("");
    setFields({});
  }
  async function save(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setNotice("");
    setFields({});
    try {
      const values = { title, body, status };
      const data =
        editingId === null
          ? await api.createNote(values)
          : await api.updateNote(editingId, values);
      setSelected(data.note);
      resetForm();
      await reload();
      setNotice("DB에 메모를 저장했습니다.");
    } catch (error) {
      setError(error.message);
      setFields(error.fields || {});
    } finally {
      setBusy(false);
    }
  }
  async function remove() {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await api.deleteNote(deleting.id);
      if (selected?.id === deleting.id) setSelected(null);
      if (editingId === deleting.id) resetForm();
      setDeleting(null);
      await reload();
      setNotice("DB에서 메모를 삭제했습니다.");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }
  async function refresh() {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await reload();
      if (selected) {
        const data = await api.findNote(selected.id);
        setSelected(data.note);
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }
  if (checking)
    return (
      <p className="db-loading" role="status">
        로그인 상태를 확인하는 중입니다…
      </p>
    );
  if (!user)
    return (
      <section className="db-login">
        <span className="eyebrow">DATABASE NOTES · OPERATOR ACCESS</span>
        <h1>DB 메모 로그인</h1>
        <p className="muted">기존 감시 API의 운영자 계정으로 로그인하세요.</p>
        <form onSubmit={signIn} noValidate>
          <label htmlFor="username">아이디</label>
          <input
            id="username"
            autoComplete="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            disabled={busy}
          />
          <label htmlFor="password">비밀번호</label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={busy}
          />
          {error && (
            <p className="message error" role="alert">
              {error}
            </p>
          )}
          <button className="button primary" disabled={busy}>
            {busy ? "확인 중…" : "로그인"}
          </button>
        </form>
      </section>
    );
  return (
    <>
      <div className="page-heading db-heading">
        <div>
          <span className="eyebrow">SAVED IN YOUR DATABASE</span>
          <h1>DB 관찰 메모</h1>
          <p>{user.name}님, 새로고침해도 남는 관찰을 기록하세요.</p>
        </div>
        <button className="button secondary" onClick={signOut} disabled={busy}>
          로그아웃
        </button>
      </div>
      {error && (
        <p className="message error db-error" role="alert">
          {error}
        </p>
      )}
      {notice && (
        <p className="message success" role="status">
          {notice}
        </p>
      )}
      <div className="notes-workspace">
        <aside className="note-compose">
          <div className="compose-heading">
            <span className="compose-icon">
              <Icon name={editingId === null ? "plus" : "edit"} />
            </span>
            <div>
              <span className="eyebrow">
                {editingId === null
                  ? "NEW DATABASE NOTE"
                  : "EDIT DATABASE NOTE"}
              </span>
              <h2>{editingId === null ? "새 DB 메모" : "DB 메모 수정"}</h2>
            </div>
          </div>
          <form onSubmit={save} noValidate>
            <label htmlFor="db-title">제목</label>
            <input
              id="db-title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              disabled={busy}
              aria-invalid={Boolean(fields.title)}
            />
            {fields.title && (
              <small className="field-error">{fields.title}</small>
            )}
            <label htmlFor="db-body">내용</label>
            <textarea
              id="db-body"
              rows={6}
              value={body}
              onChange={(event) => setBody(event.target.value)}
              disabled={busy}
              aria-invalid={Boolean(fields.body)}
            />
            {fields.body && (
              <small className="field-error">{fields.body}</small>
            )}
            <label htmlFor="db-status">처리 상태</label>
            <select
              id="db-status"
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              disabled={busy}
            >
              {Object.entries(statuses).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
            <div className="compose-actions">
              {editingId !== null && (
                <button
                  className="button secondary"
                  type="button"
                  onClick={() => {
                    resetForm();
                    setError("");
                  }}
                  disabled={busy}
                >
                  수정 취소
                </button>
              )}
              <button className="button primary" disabled={busy}>
                {busy ? "저장 중…" : "DB 저장"}
              </button>
            </div>
          </form>
          <p className="compose-tip">Next.js → Flask API → PostgreSQL</p>
        </aside>
        <section className="notes-section">
          <div className="list-heading">
            <div>
              <span className="eyebrow">DATABASE COLLECTION</span>
              <h2>
                관찰 메모 <span className="count-pill">{notes.length}</span>
              </h2>
            </div>
            <div className="db-list-actions">
              <button
                className="button secondary"
                onClick={() => {
                  resetForm();
                  setSelected(null);
                  setError("");
                  setNotice("");
                }}
                disabled={busy}
              >
                새 메모
              </button>
              <button
                className="button secondary"
                onClick={refresh}
                disabled={busy}
              >
                새로고침
              </button>
            </div>
          </div>
          <div className="db-list">
            {notes.map((note) => (
              <button
                key={note.id}
                className={`db-list-item ${selected?.id === note.id ? "selected" : ""}`}
                onClick={() => select(note.id)}
                disabled={busy}
              >
                <span>#{note.id}</span>
                <strong>{note.title}</strong>
                <small>{statuses[note.status]}</small>
              </button>
            ))}
          </div>
          {notes.length === 0 && (
            <div className="empty-notes">
              <Icon name="notebook" size={30} />
              <h3>등록된 관찰 메모가 없습니다.</h3>
            </div>
          )}
          {selected && (
            <article className="db-detail" aria-label="DB 메모 상세">
              <div className="db-detail-top">
                <span className="eyebrow">
                  NOTE #{selected.id} · {statuses[selected.status]}
                </span>
                <div>
                  <button
                    className="button secondary"
                    onClick={edit}
                    disabled={busy}
                  >
                    수정
                  </button>
                  <button
                    className="button secondary"
                    onClick={() => setDeleting(selected)}
                    disabled={busy}
                  >
                    삭제
                  </button>
                </div>
              </div>
              <h2>{selected.title}</h2>
              <p className="note-content">{selected.body}</p>
            </article>
          )}
        </section>
      </div>
      {deleting && (
        <DeleteDialog
          content={deleting.title}
          onConfirm={remove}
          onCancel={() => setDeleting(null)}
          busy={busy}
        />
      )}
    </>
  );
}
