import datetime
import re

import pytz

from .exceptions import EndIsBeforeStartException


class Event:
    def __init__(self):
        pass

    def load_from_database_row(self, data):
        self.title = data["title"]
        self.description = data["description"]
        self.id = data["id"]
        self.cancelled = bool(data["cancelled"])
        self.deleted = bool(data["deleted"])
        self.url = data["url"]
        self.data = data
        self.start_year = data["start_year"]
        self.start_month = data["start_month"]
        self.start_day = data["start_day"]
        self.start_hour = data["start_hour"]
        self.start_minute = data["start_minute"]
        self.end_year = data["end_year"]
        self.end_month = data["end_month"]
        self.end_day = data["end_day"]
        self.end_hour = data["end_hour"]
        self.end_minute = data["end_minute"]

    def load_from_yaml_data(self, id, data):
        # Load
        self.title = data.get("title")
        self.description = data.get("description")
        self.id = id
        self.tag_ids = data.get("tags")
        self.cancelled = data.get("cancelled", False)
        self.deleted = data.get("deleted", False)
        self.url = data.get("url")
        (
            self.start_year,
            self.start_month,
            self.start_day,
            self.start_hour,
            self.start_minute,
        ) = self._parse_string_to_datetime(data.get("start"))
        if data.get("end"):
            (
                self.end_year,
                self.end_month,
                self.end_day,
                self.end_hour,
                self.end_minute,
            ) = self._parse_string_to_datetime(data.get("end"))
        else:
            self.end_year = self.start_year
            self.end_month = self.start_month
            self.end_day = self.start_day
            self.end_hour = self.start_hour
            self.end_minute = self.start_minute
        # Check
        start = datetime.datetime(
            self.start_year,
            self.start_month,
            self.start_day,
            self.start_hour,
            self.start_minute,
            tzinfo=pytz.timezone("Europe/London"),
        )
        end = datetime.datetime(
            self.end_year,
            self.end_month,
            self.end_day,
            self.end_hour,
            self.end_minute,
            tzinfo=pytz.timezone("Europe/London"),
        )
        if end < start:
            raise EndIsBeforeStartException("The End can not be before the Start!")

    def _parse_string_to_datetime(self, value):
        m = re.search("([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)", value)
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
            tzinfo=pytz.timezone("Europe/London"),
        )
        return start.timestamp()

    def get_start_strftime(self):
        start = datetime.datetime(
            self.start_year,
            self.start_month,
            self.start_day,
            self.start_hour,
            self.start_minute,
            tzinfo=pytz.timezone("Europe/London"),
        )
        return start.strftime("%a %d %b %Y %I:%M%p")

    def get_end_epoch(self):
        end = datetime.datetime(
            self.end_year,
            self.end_month,
            self.end_day,
            self.end_hour,
            self.end_minute,
            tzinfo=pytz.timezone("Europe/London"),
        )
        return end.timestamp()

    def get_api_json_contents(self, datastore):
        out = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "deleted": self.deleted,
            "cancelled": self.cancelled,
            "timezone": {"code": "Europe/London"},
            "start_timezone": {
                "year": self.start_year,
                "month": self.start_month,
                "day": self.start_day,
                "hour": self.start_hour,
                "minute": self.start_minute,
            },
            "end_timezone": {
                "year": self.end_year,
                "month": self.end_month,
                "day": self.end_day,
                "hour": self.end_hour,
                "minute": self.end_minute,
            },
            "tags": {},
        }
        for tag in datastore.get_tags_for_event(self.id):
            out["tags"][tag.id] = {"title": tag.title}
        return out
