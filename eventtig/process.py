from .siteconfig import SiteConfig
from .reader import Reader
from .sqlite import DataStoreSQLite


def go(source_dir, source_config, args):

    config = SiteConfig(source_dir, args.sqlite)
    config.load_from_file(source_config)

    datastore = DataStoreSQLite(config, args.sqlite)

    reader = Reader(config, datastore)
    reader.go()
