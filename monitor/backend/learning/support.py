from datetime import datetime
import json
from pathlib import Path
from monitor.backend.repositories import events

DATA = Path(__file__).with_name('data')
OBSERVATION = DATA / 'observation.json'


def json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f'Unsupported JSON type: {type(value).__name__}')


def read_observation():
    with OBSERVATION.open(encoding='utf-8-sig') as file:
        observation = json.load(file)
    rows = observation['records']
    if not isinstance(rows, list):
        raise ValueError('observation.records must be a list of real DB rows')
    return rows


def read_live(after_id, reference_time):
    return events.read_after(after_id, reference_time=reference_time)
