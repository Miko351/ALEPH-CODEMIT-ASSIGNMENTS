import argparse
import json
from .support import read_observation, json_default
from .report import build_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(build_report(read_observation(), args.threshold), ensure_ascii=False, indent=2, default=json_default))

if __name__ == '__main__':
    main()
