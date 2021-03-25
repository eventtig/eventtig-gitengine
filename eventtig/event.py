import re
import datetime
import pytz


class Event:

    def __init__(self):
        pass

    def load_from_database_row(self, data):
        self.title = data['title']
        self.description = data['description']
        self.id = data['id']
        self.cancelled = data['cancelled']
        self.deleted = data['deleted']
        self.url = data['url']
        self.data = data

    def load_from_yaml_data(self, id, data):
        self.title = data.get('title')
        self.description = data.get('description')
        self.id = id
        self.tag_ids = data.get('tags')
        self.cancelled = data.get('cancelled', False)
        self.deleted = data.get('deleted', False)
        self.url = data.get('url')
        self.start_year, self.start_month, self.start_day, self.start_hour, self.start_minute = self._parse_string_to_datetime(data.get('start'))
        self.end_year, self.end_month, self.end_day, self.end_hour, self.end_minute = self._parse_string_to_datetime(data.get('end'))

    def _parse_string_to_datetime(self, value):
        m = re.search('([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)', value)
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4))
        minute = int(m.group(5))
        return [year, month, day, hour, minute]

    def get_start_epoch(self):
        start = datetime.datetime(
            self.start_year,
            self.start_month,
            self.start_day,
            self.start_hour,
            self.start_minute,
            tzinfo=pytz.timezone('Europe/London')
        )
        return start.timestamp()

    def get_end_epoch(self):
        end = datetime.datetime(
            self.end_year,
            self.end_month,
            self.end_day,
            self.end_hour,
            self.end_minute,
            tzinfo=pytz.timezone('Europe/London')
        )
        return end.timestamp()