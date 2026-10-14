from .normalize import normalize_events, event_time
from .http_rules import select_views, find_following_errors


def build_report(original_rows, threshold=10):
    if type(threshold) is not int or not 1 <= threshold <= 10000:
        raise ValueError('threshold must be an integer between 1 and 10000')
    normalized = normalize_events(original_rows)
    views = select_views(normalized)
    following = find_following_errors(normalized, views)
    count = len(views)
    candidate = count >= threshold
    records = sorted(views + following, key=lambda row: (event_time(row['occurred_at']), row['source_id']))
    return {'cards': [{
        'key': 'http-post-list', 'title': 'HTTP 목록 조회', 'source': 'http_live',
        'observed_value': count, 'threshold': threshold, 'is_candidate': candidate,
        'verdict': '검토 후보' if candidate else '기준 미해당',
        'reason': f'네 조건을 만족한 목록 조회 {count}회를 기준 {threshold}과 >=로 비교했습니다. 뒤따른 404 {len(following)}건은 횟수가 아닌 문맥 근거입니다.',
        'view_ids': [row['id'] for row in views],
        'following_error_ids': [row['id'] for row in following],
        'evidence': [row['id'] for row in records], 'records': records,
        'limitations': '같은 서비스에서 시간상 뒤따른 기록입니다. 동일 사용자·IP·인과관계·침해를 확정하지 않으며 기준 미해당도 정상 입증이 아닙니다.',
    }]}
