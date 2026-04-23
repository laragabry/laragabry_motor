from models.event import Event
from structures.hash_table import HashTable
_DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def _is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
def _weekday(year, month, day):
    
    if month < 3:
        month += 12
        year -= 1

    k = year % 100
    j = year // 100

    h = (day + (13*(month+1))//5 + k + k//4 + j//4 - 2*j) % 7
    return (h + 5) % 7


def load_data(file_path):
    
    events = []
    with open(file_path, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 7:
                continue
            ev = Event(
                parts[0],
                parts[1],
                parts[2],
                parts[3],
                parts[4],
                parts[5],
                parts[6],
            )
            y, m, d = int(ev.date[:4]), int(ev.date[5:7]), int(ev.date[8:10])
            ev.weekday = _weekday(y, m, d)
            events.append(ev)
    idx_zone      = HashTable(size=64)
    idx_date      = HashTable(size=256)
    idx_type      = HashTable(size=8)
    idx_zone_date = HashTable(size=512)
    for ev in events:
        lst = idx_zone.get(ev.zone_id)
        if lst is None:
            lst = []
            idx_zone.insert(ev.zone_id, lst)
        lst.append(ev)
        lst = idx_date.get(ev.date)
        if lst is None:
            lst = []
            idx_date.insert(ev.date, lst)
        lst.append(ev)
        lst = idx_type.get(ev.event_type)
        if lst is None:
            lst = []
            idx_type.insert(ev.event_type, lst)
        lst.append(ev)
        key = f"{ev.zone_id}|{ev.date}"
        lst = idx_zone_date.get(key)
        if lst is None:
            lst = []
            idx_zone_date.insert(key, lst)
        lst.append(ev)
    return events, idx_zone, idx_date, idx_type, idx_zone_date