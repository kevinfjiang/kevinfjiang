from pathlib import Path
import pytest

from update.config import PATH
from update.models import ReadmeData
from update.views import GithubView, WebsiteView


@pytest.fixture
def data():
    return ReadmeData(PATH)


def test_readme_data_properties(data: ReadmeData):
    assert data.github_username == "kevinfjiang"
    assert data.full_name != ""
    assert isinstance(data.projects_sorted, list)
    assert isinstance(data.news_sorted, list)
    assert isinstance(data.services, dict)
    assert "github" in data.links
    assert "github" in data.badges


def test_badge_markdown(data: ReadmeData):
    badge_md = data.get_badge_markdown("github")
    assert "https://github.com/kevinfjiang" in badge_md
    assert "https://img.shields.io/badge/GitHub" in badge_md


def test_github_view_generation(data: ReadmeData, tmp_path: Path):
    target_file = tmp_path / "TEST_README"
    view = GithubView(data, file_name=target_file)
    view.generate()

    output_md = tmp_path / "TEST_README.md"
    assert output_md.exists()

    content = output_md.read_text(encoding="utf-8")
    assert "<details><summary>projectupdate.db</summary>" in content
    assert "<details><summary>music.db</summary>" in content
    assert "<details><summary>informalbio.html</summary>" in content
    assert "AUTHOR:" in content
    assert "LAST UPDATED:" in content


def test_github_view_custom_output_dir(data: ReadmeData, tmp_path: Path):
    custom_dir = tmp_path / "custom_out"
    custom_dir.mkdir()
    view = GithubView(data, file_name="CUSTOM_README.md", output_dir=custom_dir)
    view.generate()

    expected_file = custom_dir / "CUSTOM_README.md"
    assert expected_file.exists()


def test_website_view_generation(data: ReadmeData, tmp_path: Path):
    submod_dir = tmp_path / "website"
    submod_dir.mkdir()
    (submod_dir / "config_base.yml").write_text("title: Test Website\n", encoding="utf-8")

    view = WebsiteView(data, submodule_path=submod_dir)
    view.generate()

    assert (submod_dir / "_includes" / "aboutme.md").exists()
    assert (submod_dir / "_config.yml").exists()
    assert (submod_dir / "_data" / "projects.yml").exists()
    assert (submod_dir / "_includes" / "services.md").exists()
    assert (submod_dir / "_includes" / "news.md").exists()

    aboutme_content = (submod_dir / "_includes" / "aboutme.md").read_text(encoding="utf-8")
    assert "## About Me" in aboutme_content


def test_website_view_custom_output_dir(data: ReadmeData, tmp_path: Path):
    custom_dir = tmp_path / "site_out"
    custom_dir.mkdir()
    (custom_dir / "config_base.yml").write_text("title: Custom Site\n", encoding="utf-8")

    view = WebsiteView(data, output_dir=custom_dir)
    view.generate()

    assert (custom_dir / "_includes" / "aboutme.md").exists()
    assert (custom_dir / "_config.yml").exists()
