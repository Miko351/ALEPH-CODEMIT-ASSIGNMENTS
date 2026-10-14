import json
from .support import read_observation, json_default
from .normalize import normalize_events

def main():
    original = read_observation()
    rows = normalize_events(original)
    print(json.dumps({'original_count': len(original), 'normalized_count': len(rows), 'records': rows}, ensure_ascii=False, indent=2, default=json_default))

if __name__ == '__main__':
    main()
