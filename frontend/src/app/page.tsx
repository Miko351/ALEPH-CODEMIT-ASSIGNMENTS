import { SignupForm } from "@/components/signup/signup-form";
import { Icon } from "@/components/ui/icon";
import Link from "next/link";

export default function Home() {
  return (
    <main className="signup-shell">
      <aside className="story-panel" aria-label="ALEPH 소개">
        <Link className="wordmark" href="/" aria-label="ALEPH 홈">
          <span className="brand-symbol">a</span>ALEPH
          <span className="brand-dot">®</span>
        </Link>
        <div className="story-copy">
          <span className="eyebrow">
            <span /> YOUR NEXT CHAPTER
          </span>
          <h1>
            가능성은 무한하게.
            <br />
            시작은 가볍게.
          </h1>
          <p>
            새로운 생각과 더 넓은 일상.
            <br />
            당신의 다음 이야기를 ALEPH에서 시작하세요.
          </p>
          <div className="orbit-art" aria-hidden="true">
            <div className="orbit orbit-one" />
            <div className="orbit orbit-two" />
            <div className="orbit orbit-three" />
            <div className="orbit-core">
              a<span>끝없는 가능성의 시작</span>
            </div>
            <span className="orbit-spark spark-one" />
            <span className="orbit-spark spark-two" />
          </div>
        </div>
        <div className="story-bottom">
          <span>작은 시작, 무한한 가능성.</span>
          <span>01 — START</span>
        </div>
      </aside>
      <section className="form-panel" aria-labelledby="signup-heading">
        <div className="panel-top">
          <span>처음 오셨나요? 반가워요.</span>
          <span className="secure-badge">
            <Icon name="lock" /> 안전한 가입
          </span>
        </div>
        <div className="form-content">
          <div className="step-label">
            <span>01</span> CREATE YOUR ACCOUNT
          </div>
          <h2 id="signup-heading">나만의 시작을 만들어보세요</h2>
          <p className="form-intro">몇 가지 정보만 입력하면 준비가 끝나요.</p>
          <SignupForm />
        </div>
        <footer className="panel-footer">
          <span>© {new Date().getFullYear()} ALEPH</span>
          <span>당신의 정보를 소중하게 지킵니다.</span>
        </footer>
      </section>
    </main>
  );
}
