import yaml


class SiteConfig:
    def __init__(self, source_dir):
        self.config = {}

        self.source_dir = source_dir

    def load_from_file(self, filename):
        with open(filename) as fp:
            self.config = yaml.safe_load(fp)

    def get_tags_extra_fields(self):
        return self.config.get("tags", {}).get("extra_fields", {})

    def get_title(self):
        return self.config.get("title", "Events")

    def get_description(self):
        return self.config.get("description", "")

    def has_github(self):
        return (
            self.config.get("githost", {}).get("type").strip().lowercase() == "github"
        )

    def get_github_url(self):
        return self.config.get("githost", {}).get("url")

    def get_github_default_branch(self):
        return self.config.get("githost", {}).get("default_branch", "main")
