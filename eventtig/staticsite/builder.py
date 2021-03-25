from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil


class StaticSiteBuilder:

    def __init__(self, site_config, datastore, out_directory):
        self.site_config = site_config
        self.datastore = datastore
        self.out_directory = out_directory

    def go(self):
        # Templates
        self._jinja2_env = Environment(
            loader=FileSystemLoader(searchpath=os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Vars
        self._template_variables = {
            'site_config': self.site_config,
            'site_title': 'Events',
        }

        # Out Dir
        os.makedirs(self.out_directory, exist_ok=True)

        # Top Level Static Pages
        for page in ['robots.txt','index.html']:
            self._write_template('', page, page, {})

        # Events
        events = self.datastore.get_events()
        self._write_template('event', 'index.html', 'event/index.html', {'events': events })
        for event in events:
            self._write_template('event/'+event.id, 'index.html', 'event/event/index.html', {'event': event })

        # Assets
        assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets')
        for filename in [f for f in os.listdir(assets_dir) if os.path.isfile(os.path.join(assets_dir, f))]:
            name_bits = filename.split(".")
            if name_bits[-1] in ['css','js']:
                shutil.copy(
                    os.path.join(assets_dir, filename),
                    os.path.join(self.out_directory, filename)
                )

        # All Data
        shutil.copy(self.datastore.get_file_name(), os.path.join(self.out_directory, "database.sqlite"))


    def _write_template(self, dirname, filename, templatename, variables):
        os.makedirs(os.path.join(self.out_directory, dirname), exist_ok=True)
        variables.update(self._template_variables)
        with open(os.path.join(self.out_directory, dirname, filename),
                  "w") as fp:
            fp.write(self._jinja2_env.get_template(templatename).render(**variables))