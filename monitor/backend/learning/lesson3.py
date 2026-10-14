import json
from .support import read_observation
from .normalize import normalize_events
from .http_rules import select_views

def main():
    rows = normalize_events(read_observation())
    views = select_views(rows)
    print(json.dumps({'original_count': len(rows), 'view_count': len(views), 'view_ids': [row['id'] for row in views], 'threshold': 10, 'candidate': len(views) >= 10}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
