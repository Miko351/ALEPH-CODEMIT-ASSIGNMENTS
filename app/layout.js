import Link from "next/link";
import Icon from "@/components/Icon";
import "./globals.css";

export const metadata = {
  title: { default: "기록의 방 · Next.js 메모", template: "%s · 기록의 방" },
  description:
    "배운 것을 한 줄씩 남기는 작은 메모 공간. Next.js와 React state 실습.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body>
        <a className="skip-link" href="#main">
          본문으로 이동
        </a>
        <header className="site-header">
          <div className="header-inner">
            <Link href="/" className="brand">
              <span className="brand-mark">
                <Icon name="notebook" size={22} />
              </span>
              <span>
                기록의 방<small>NOTE ROOM</small>
              </span>
            </Link>
            <nav aria-label="주 메뉴">
              <Link href="/">홈</Link>
              <Link href="/notes">메모</Link>
              <Link href="/db-notes">DB 메모</Link>
            </nav>
            <span className="header-label">ALEPH · NEXT PRACTICE</span>
          </div>
        </header>
        <main id="main" className="page-container">
          {children}
        </main>
        <footer className="site-footer">
          <span>
            기록의 방 <span className="footer-dot">·</span> 작은 배움을 오래
            기억하는 방법
          </span>
          <span>NEXT.JS + REACT</span>
        </footer>
      </body>
    </html>
  );
}
