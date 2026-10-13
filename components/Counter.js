"use client";
import { useState } from "react";
import Icon from "./Icon";

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <section className="counter-card" aria-labelledby="counter-heading">
      <div className="counter-top">
        <span className="eyebrow">PLAY WITH STATE</span>
        <span className="quiet-tag">연습 공간</span>
      </div>
      <h2 id="counter-heading">숫자 카운터</h2>
      <output
        className="counter-number"
        aria-label="현재 숫자"
        aria-live="polite"
      >
        {count.toString().padStart(2, "0")}
      </output>
      <p>작은 클릭이 쌓이는 모습을 확인해 보세요.</p>
      <div className="counter-actions">
        <button
          className="button primary"
          onClick={() => setCount((value) => value + 1)}
        >
          <Icon name="plus" size={16} /> 숫자 올리기
        </button>
        <button className="button secondary" onClick={() => setCount(0)}>
          <Icon name="reset" size={16} /> 초기화
        </button>
      </div>
    </section>
  );
}
