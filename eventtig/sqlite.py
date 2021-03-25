import sqlite3
from .event import Event

class DataStoreSQLite:

    def __init__(self, site_config, out_filename):
        self.site_config = site_config
        self.out_filename = out_filename
        self.connection =  sqlite3.connect(out_filename)
        self.connection.row_factory = sqlite3.Row

        # Create table
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE event (
            id TEXT PRIMARY KEY, 
            title text, 
            description text,
            url text,
            cancelled integer,
            deleted integer,
            start_year integer,
            start_month integer,
            start_day integer,
            start_hour integer,
            start_minute integer,
            start_epoch integer,
            end_year integer,
            end_month integer,
            end_day integer,
            end_hour integer,
            end_minute integer,
            end_epoch integer
            )'''
        )
        cur.execute('''CREATE TABLE tag (
            id TEXT PRIMARY KEY, 
            title text
            )'''
        )

        for extra_field_name, extra_field_data in site_config.get_tags_extra_fields().items():
            if extra_field_data.get('type') == 'string':
                cur.execute('ALTER TABLE tag ADD COLUMN extra_' + extra_field_name + " TEXT")
            elif extra_field_data.get('type') == 'boolean':
                cur.execute('ALTER TABLE tag ADD COLUMN extra_' + extra_field_name + " INTEGER")

        cur.execute('''CREATE TABLE event_has_tag (
            event_id TEXT, 
            tag_id TEXT,
            PRIMARY KEY(event_id, tag_id)
            )'''
        )

        self.connection.commit()

    def store_event(self, event):
        cur = self.connection.cursor()
        insert_data = [
            event.id,
            event.title,
            event.description,
            event.url,
            1 if event.cancelled else 0,
            1 if event.deleted else 0,
            event.start_year,
            event.start_month,
            event.start_day,
            event.start_hour,
            event.start_minute,
            event.get_start_epoch(),
            event.end_year,
            event.end_month,
            event.end_day,
            event.end_hour,
            event.end_minute,
            event.get_end_epoch()
        ]
        cur.execute(
            """INSERT INTO event (
            id, title, description, url, cancelled, deleted,
            start_year, start_month,start_day,start_hour,start_minute,start_epoch,
            end_year,end_month,end_day,end_hour,end_minute,end_epoch
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            insert_data
        )
        for tag_id in event.tag_ids:
            cur.execute("INSERT INTO event_has_tag (event_id, tag_id) VALUES (?, ?)", [ event.id, tag_id ])
        self.connection.commit()


    def store_tag(self, tag):
        cur = self.connection.cursor()
        insert_data = [
            tag.id,
            tag.title,
        ]
        cur.execute("INSERT INTO tag (id, title) VALUES (?, ?)", insert_data)
        for extra_field_name, extra_field_data in self.site_config.get_tags_extra_fields().items():
            if extra_field_data.get('type') == 'string':
                cur.execute('UPDATE tag SET extra_' + extra_field_name + " = ? WHERE id = ?", [tag.extra.get(extra_field_name), tag.id])
            elif extra_field_data.get('type') == 'boolean':
                cur.execute('UPDATE tag SET extra_' + extra_field_name + " = ? WHERE id = ?", [1 if tag.extra.get(extra_field_name) else 0, tag.id])
        self.connection.commit()


    def get_events(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM event ORDER BY start_epoch ASC", [])
        out = []
        for data in cur.fetchall():
            event = Event()
            event.load_from_database_row(data)
            out.append(event)
        return out

    def get_file_name(self):
        return self.out_filename