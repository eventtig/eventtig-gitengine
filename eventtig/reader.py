import os
import yaml
from .event import Event
from .tag import Tag

class Reader:

    def __init__(self, config, datastore):
        self.config = config
        self.datastore = datastore

    def go(self):
        # Tags
        start_dir = os.path.join(self.config.source_dir, "tags")
        full_start_dir = os.path.abspath(start_dir)
        for path, subdirs, files in os.walk(start_dir):
            for name in files:
                if name.endswith('tag.yaml'):
                    full_filename = os.path.abspath(os.path.join(path, name))
                    self.process_tag_file(full_filename,  full_filename[len(full_start_dir)+1:])

        # Events
        start_dir = os.path.join(self.config.source_dir, "events")
        full_start_dir = os.path.abspath(start_dir)
        for path, subdirs, files in os.walk(start_dir):
            for name in files:
                if name.endswith('event.yaml'):
                    full_filename = os.path.abspath(os.path.join(path, name))
                    self.process_event_file(full_filename,  full_filename[len(full_start_dir)+1:])


    def process_event_file(self, filename_absolute, filename_relative_to_data_folder):

        id = filename_relative_to_data_folder[:-len('/event.yaml')]

        with open(filename_absolute) as fp:
            data = yaml.safe_load(fp)
        event = Event()
        event.load_from_yaml_data(id, data)
        self.datastore.store_event(event)

    def process_tag_file(self, filename_absolute, filename_relative_to_data_folder):

        id = filename_relative_to_data_folder[:-len('/tag.yaml')]

        with open(filename_absolute) as fp:
            data = yaml.safe_load(fp)
        tag = Tag()
        tag.load_from_yaml_data(id, data)
        self.datastore.store_tag(tag)
