import Notes from "@/components/Notes";
export const metadata = { title: "나의 메모" };

export default function NotesPage() {
  return <><div className="page-heading"><span className="eyebrow">COLLECT YOUR LITTLE THOUGHTS</span><h1>나의 메모</h1><p>배운 것, 떠오른 생각, 다음에 하고 싶은 일까지.<br className="mobile-break" /> 지금 기억하고 싶은 것을 남겨 주세요.</p></div><Notes /></>;
}
