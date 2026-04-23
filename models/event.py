class Event:
    def __init__(self, event_id, timestamp, zone_id, event_type, duration, gender, age):
        self.event_id = event_id
        self.timestamp = timestamp
        self.zone_id = zone_id
        self.event_type = event_type
        self.duration = int(duration)
        self.gender = gender
        self.age = age
        self.date = timestamp[:10]
        self.hour = int(timestamp[11:13])
        self.minute = int(timestamp[14:16])
        self.weekday = None
    def __repr__(self):
        return f"<Event {self.event_id} {self.event_type} {self.zone_id} {self.timestamp}>"