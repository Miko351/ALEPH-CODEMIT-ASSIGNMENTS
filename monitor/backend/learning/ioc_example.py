"""Exact-string comparison of documentation IPs; unrelated to live HTTP rows."""
import json

def match_indicator(observed_ip, indicators):
    return observed_ip in indicators

def main():
    indicators = {'203.0.113.7'}
    print(json.dumps({'source': 'documentation_ip_example', 'match': match_indicator('203.0.113.7', indicators), 'no_match': match_indicator('203.0.113.8', indicators), 'limitation': 'Live HTTP records have no IP field; this example cannot identify their users or requests.'}, indent=2))

if __name__ == '__main__':
    main()
