export const noteStatuses = [
  { value: 'pending', label: '확인 전' },
  { value: 'in_progress', label: '확인 중' },
  { value: 'completed', label: '완료' },
];

export default function NoteStatus({ status }) {
  const label = noteStatuses.find(item => item.value === status)?.label || '확인 전';
  return <span className={`note-status ${status || 'pending'}`}>{label}</span>;
}
