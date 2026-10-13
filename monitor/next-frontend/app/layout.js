import Link from "next/link";
import Icon from "../components/Icon";
import "./globals.css";

export const metadata = {
  title: "DB 관찰 메모 · 기록의 방",
  description: "기존 Flask·PostgreSQL 관찰 메모 API를 사용하는 Next.js 화면",
};
export default function Layout({ children }) {
  return (
    <html lang="ko">
      <body>
        <header className="site-header">
          <div className="header-inner">
            <Link className="brand" href="/">
              <span className="brand-mark">
                <Icon name="notebook" size={22} />
              </span>
              <span>
                기록의 방<small>DATABASE NOTES</small>
              </span>
            </Link>
            <nav aria-label="주 메뉴">
              <Link href="/">감시 대시보드</Link>
              <Link href="/notes">관찰 메모</Link>
            </nav>
            <span className="header-label">FLASK · POSTGRESQL</span>
          </div>
        </header>
        <main className="page-container">{children}</main>
        <footer className="site-footer">
          <span>DB에 저장하는 관찰 메모</span>
          <span>NEXT.JS → FLASK → POSTGRESQL</span>
        </footer>
      </body>
    </html>
  );
}
