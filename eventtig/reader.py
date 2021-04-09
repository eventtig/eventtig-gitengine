import os

import yaml

from .event import Event
from .tag import Tag


class Reader:
    def __init__(self, config, datastore):
        self.config = config
        self.datastore = datastore

    def go(self):
        had_errors = False

        # Tags
        start_dir = os.path.join(self.config.source_dir, "tags")
        full_start_dir = os.path.abspath(start_dir)
        for path, subdirs, files in os.walk(start_dir):
            for name in files:
                if name.endswith("tag.yaml"):
                    try:
                        full_filename = os.path.abspath(os.path.join(path, name))
                        self.process_tag_file(
                            full_filename, full_filename[len(full_start_dir) + 1 :]
                        )
                    except Exception as e:
                        print("ERROR WHILE PARSING TAG: " + full_filename)
                        print(e)
                        had_errors = True

        # Events
        start_dir = os.path.join(self.config.source_dir, "events")
        full_start_dir = os.path.abspath(start_dir)
        for path, subdirs, files in os.walk(start_dir):
            for name in files:
                if name.endswith("event.yaml"):
                    try:
                        full_filename = os.path.abspath(os.path.join(path, name))
                        self.process_event_file(
                            full_filename, full_filename[len(full_start_dir) + 1 :]
                        )
                    except Exception as e:
                        print("ERROR WHILE PARSING EVENT: " + full_filename)
                        print(e)
                        had_errors = True

        return had_errors

    def process_event_file(self, filename_absolute, filename_relative_to_data_folder):

        id = filename_relative_to_data_folder[: -len("/event.yaml")]

        # TODO Put this in some kind of Verbose mode only
        # print("Processing Event " + id)

        with open(filename_absolute) as fp:
            data = yaml.safe_load(fp)
        event = Event()
        event.load_from_yaml_data(
            id, data, "events/" + filename_relative_to_data_folder
        )
        self.datastore.store_event(event)

    def process_tag_file(self, filename_absolute, filename_relative_to_data_folder):

        id = filename_relative_to_data_folder[: -len("/tag.yaml")]

        # TODO Put this in some kind of Verbose mode only
        # print("Processing Tag " + id)

        with open(filename_absolute) as fp:
            data = yaml.safe_load(fp)
        tag = Tag()
        tag.load_from_yaml_data(id, data)
        self.datastore.store_tag(tag)
