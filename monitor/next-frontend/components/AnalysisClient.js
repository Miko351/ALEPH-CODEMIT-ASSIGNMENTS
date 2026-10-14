"use client";
import { useState } from "react";
import { startObservation, getAnalysis } from "../api/analysis";

export default function AnalysisClient() {
  const [threshold, setThreshold] = useState("10");
  const [afterId, setAfterId] = useState(null);
  const [referenceTime, setReferenceTime] = useState(null);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function start() {
    setBusy(true);
    setError("");
    setReport(null);
    setReferenceTime(null);
    setAfterId(null);
    try {
      setAfterId((await startObservation()).after_id);
    } catch (reason) {
      setError(reason.message);
    } finally {
      setBusy(false);
    }
  }
  async function load() {
    setBusy(true);
    setError("");
    try {
      const next = await getAnalysis({ threshold, afterId, referenceTime });
      setReferenceTime(next.reference_time);
      setReport(next);
    } catch (reason) {
      setError(reason.message);
    } finally {
      setBusy(false);
    }
  }
  const card = report?.cards[0];
  return (
    <section
      className="request-records analysis-panel"
      aria-label="HTTP 조회 분석"
    >
      <span className="eyebrow">LIVE HTTP EVIDENCE</span>
      <h2>HTTP 조회 분석</h2>
      <p className="muted">
        새 관찰은 ID 경계를 바꿉니다. 첫 결과의 기준시각까지 최근 60초를 읽으며
        자동 수집 타이머는 아닙니다.
      </p>
      <div className="analysis-controls">
        <button className="button secondary" onClick={start} disabled={busy}>
          새 관찰 시작
        </button>
        <label htmlFor="analysis-threshold">비교 기준</label>
        <input
          id="analysis-threshold"
          type="number"
          min="1"
          max="10000"
          value={threshold}
          onChange={(event) => setThreshold(event.target.value)}
          disabled={busy}
        />
        <button
          className="button primary"
          onClick={load}
          disabled={busy || afterId === null}
        >
          결과 불러오기
        </button>
      </div>
      <p className="muted">
        시작 ID:{" "}
        <span data-testid="analysis-after-id">
          {afterId === null ? "미설정" : afterId}
        </span>{" "}
        · 기준시각:{" "}
        <span data-testid="analysis-reference">
          {referenceTime || "첫 결과 요청 때 고정"}
        </span>
      </p>
      {error && (
        <p className="message error" role="alert">
          {error}
        </p>
      )}
      {card && (
        <article className="analysis-card">
          <h3>{card.title}</h3>
          <div className="analysis-metrics">
            <div>
              <small>관찰값</small>
              <strong data-testid="analysis-count">
                {card.observed_value}
              </strong>
            </div>
            <div>
              <small>비교 기준</small>
              <strong data-testid="analysis-rule">{card.threshold}</strong>
            </div>
            <div>
              <small>판정</small>
              <strong data-testid="analysis-verdict">{card.verdict}</strong>
            </div>
            <div>
              <small>근거 행</small>
              <strong data-testid="analysis-evidence-count">
                {card.records.length}
              </strong>
            </div>
          </div>
          <p>{card.reason}</p>
          <p className="muted">{card.limitations}</p>
          <details>
            <summary>근거 보기 ({card.records.length}행)</summary>
            <div className="records-scroll">
              <table aria-label="분석 원본 근거">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>수신시각</th>
                    <th>방법</th>
                    <th>경로</th>
                    <th>상태</th>
                    <th>종류</th>
                  </tr>
                </thead>
                <tbody>
                  {card.records.map((row) => (
                    <tr key={row.id} data-source-id={row.source_id}>
                      <td>{row.id}</td>
                      <td>{row.occurred_at}</td>
                      <td>{row.method}</td>
                      <td>{row.path}</td>
                      <td>{row.status_code}</td>
                      <td>{row.kind}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {card.records.length === 0 && (
              <p>해당 관찰 구간의 근거가 없습니다. 이전 DB 행은 보존됩니다.</p>
            )}
          </details>
        </article>
      )}
    </section>
  );
}
