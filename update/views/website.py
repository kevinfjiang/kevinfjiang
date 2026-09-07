import shutil
from pathlib import Path
import yaml
from mdutils import MdUtils
from typer import echo

from update.config import SUBMOD
from update.models import ReadmeData
from update.views.base import BaseView


class WebsiteView(BaseView):
    """View responsible for rendering and updating Jekyll website include files and configs."""

    def __init__(
        self,
        data: ReadmeData,
        submodule_path: str | Path | None = None,
        output_dir: str | Path | None = None,
    ) -> None:
        super().__init__(data)
        target = output_dir or submodule_path or SUBMOD
        self.submodule_path = Path(target)

    def update_user(self) -> None:
        """Update website user section: aboutme.md and _config.yml."""
        includes_dir = self.submodule_path / "_includes"
        includes_dir.mkdir(parents=True, exist_ok=True)

        aboutme_file = str(includes_dir / "aboutme.md")
        aboutme_md = MdUtils(file_name=aboutme_file)
        aboutme_md.new_line("## About Me")
        aboutme_md.new_line(self.data.about_me.get("description", ""))
        aboutme_md.create_md_file()

        base_config_path = self.submodule_path / "config_base.yml"
        config_path = self.submodule_path / "_config.yml"

        base_config = {}
        if base_config_path.exists():
            with open(base_config_path, "r", encoding="utf-8") as base:
                base_config = yaml.load(base, Loader=yaml.FullLoader) or {}

        web_config = {**self.data.user, **base_config}
        with open(config_path, "w", encoding="utf-8") as conf:
            yaml.dump(web_config, conf, default_flow_style=False)

        echo("website user section updated")

    def update_projects(self) -> None:
        """Copy projects.yml to the website _data directory."""
        data_dir = self.submodule_path / "_data"
        data_dir.mkdir(parents=True, exist_ok=True)

        projects_file = self.data.data_dir / "projects.yml"
        if projects_file.exists():
            shutil.copy(projects_file, data_dir / "projects.yml")
        else:
            with open(data_dir / "projects.yml", "w", encoding="utf-8") as f:
                yaml.dump(
                    {
                        "projects": self.data.projects,
                        "publications": self.data.publications,
                    },
                    f,
                    default_flow_style=False,
                )

    def update_services(self) -> None:
        """Update website services.md include file."""
        includes_dir = self.submodule_path / "_includes"
        includes_dir.mkdir(parents=True, exist_ok=True)

        services_file = str(includes_dir / "services.md")
        serve_md = MdUtils(file_name=services_file)
        serve_md.new_line("## Services")

        for category, service_list in self.data.services.items():
            serve_md.new_line(f"#### {category}")
            serve_md.new_list(service_list)

        serve_md.create_md_file()

    def update_news(self) -> None:
        """Update website news.md include file."""
        includes_dir = self.submodule_path / "_includes"
        includes_dir.mkdir(parents=True, exist_ok=True)

        news_file = str(includes_dir / "news.md")
        news_md = MdUtils(file_name=news_file)
        news_md.new_line("## News")
        news_md.new_list(self.data.formatted_news)
        news_md.create_md_file()

    def generate(self) -> None:
        """Generate all website markdown files and configurations."""
        self.update_user()
        self.update_projects()
        self.update_services()
        self.update_news()
        echo("Website created!")
