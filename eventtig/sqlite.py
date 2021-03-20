import sqlite3

class DataStoreSQLite:

    def __init__(self, site_config, out_filename):
        self.site_config = site_config
        self.out_filename = out_filename
        self.connection =  sqlite3.connect(out_filename)

        # Create table
        cur = self.connection.cursor()
        cur.execute('''CREATE TABLE event (
            id TEXT PRIMARY KEY, 
            title text, 
            description text
            )'''
        )
        cur.execute('''CREATE TABLE tag (
            id TEXT PRIMARY KEY, 
            title text
            )'''
        )

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
        ]
        cur.execute("INSERT INTO event (id, title, description) VALUES (?, ?, ?)", insert_data)
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
        self.connection.commit()

