"use client";
import { useEffect, useState } from "react";
import { listEvents } from "../api/events";

export default function RequestRecords() {
  const [events, setEvents] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function refresh() {
    setBusy(true);
    setError("");
    try {
      setEvents((await listEvents()).events);
    } catch (reason) {
      setError(reason.message);
    } finally {
      setBusy(false);
    }
  }
  useEffect(() => {
    let active = true;
    listEvents()
      .then((data) => {
        if (active) setEvents(data.events);
      })
      .catch((reason) => {
        if (active) setError(reason.message);
      });
    return () => {
      active = false;
    };
  }, []);
  const visible = events.filter((event) =>
    `${event.path} ${event.status_code} ${event.event_kind}`.includes(
      query.trim(),
    ),
  );
  return (
    <section className="request-records" aria-label="일반 서비스 요청 기록">
      <div className="section-heading">
        <div>
          <span className="eyebrow">GENERAL SERVICE EVENTS</span>
          <h2>요청 기록</h2>
        </div>
        <button className="button secondary" onClick={refresh} disabled={busy}>
          기록 불러오기
        </button>
      </div>
      <p className="muted">
        전체 {events.length}건 · 오류{" "}
        {events.filter((event) => event.status_code >= 400).length}건
      </p>
      <label htmlFor="record-query">경로 · 상태 코드 · 기록 종류 검색</label>
      <input
        id="record-query"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="예: login_failure 또는 401"
      />
      {error && (
        <p className="message error" role="alert">
          {error}
        </p>
      )}
      <div className="records-scroll">
        <table>
          <thead>
            <tr>
              <th>종류</th>
              <th>메서드</th>
              <th>경로</th>
              <th>상태</th>
              <th>시각</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((event) => (
              <tr key={event.id}>
                <td>{event.event_kind}</td>
                <td>{event.method}</td>
                <td>{event.path}</td>
                <td>{event.status_code}</td>
                <td>{new Date(event.occurred_at).toLocaleString("ko-KR")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {visible.length === 0 && (
        <p className="empty-state">
          표시할 요청 기록이 없습니다. 일반 서비스에서 로그인한 뒤 다시
          불러오세요.
        </p>
      )}
    </section>
  );
}
