import Link from "next/link";
import Counter from "@/components/Counter";
import Icon from "@/components/Icon";

export default function Home() {
  return (
    <>
      <section className="home-hero">
        <div className="hero-copy">
          <span className="eyebrow">
            <span className="tiny-dot" /> A LITTLE NOTE, A LASTING THOUGHT
          </span>
          <h1>
            오늘 배운 것,
            <br />
            <em>내일의 메모로.</em>
          </h1>
          <p>
            스쳐 가는 생각과 새롭게 배운 내용을
            <br />한 줄씩 모아 나만의 기록을 만들어 보세요.
          </p>
          <Link href="/notes" className="button primary hero-button">
            메모 시작하기 <Icon name="arrow" size={17} />
          </Link>
          <span className="hero-footnote">
            완벽한 문장보다, 지금의 작은 기록이면 충분해요.
          </span>
        </div>
        <div className="hero-illustration" aria-hidden="true">
          <span className="orbit orbit-one" />
          <span className="orbit orbit-two" />
          <div className="paper paper-back">
            <span>THOUGHT 02</span>
            <p>
              작은 기능부터
              <br />
              하나씩 완성하기.
            </p>
            <div className="paper-lines" />
          </div>
          <div className="paper paper-front">
            <span>THOUGHT 01</span>
            <Icon name="spark" size={29} />
            <p>
              배운 내용을
              <br />내 말로 정리하기.
            </p>
            <small>오늘의 배움이 쌓이는 곳</small>
          </div>
          <span className="paper-stamp">made of small moments</span>
        </div>
      </section>
      <section className="home-bottom">
        <div className="introduction">
          <span className="eyebrow">작은 실습, 선명한 변화</span>
          <h2>
            버튼 하나에서 시작되는
            <br />
            React의 작은 움직임
          </h2>
          <p>
            오른쪽 숫자를 올려 보고 초기화해 보세요.
            <br />
            버튼을 누르는 순간, 화면도 함께 바뀝니다.
          </p>
          <div className="intro-tags">
            <span>useState</span>
            <span>Client Component</span>
            <span>App Router</span>
          </div>
          <Link href="/notes" className="text-link">
            다음은 메모를 만들어 볼까요? <Icon name="arrow" size={15} />
          </Link>
        </div>
        <Counter />
      </section>
    </>
  );
}
