from pathlib import Path
from typing import Annotated
from typer import Option, Typer

from update.config import PATH, ROOT_DIR, SUBMOD
from update.models import ReadmeData
from update.views import GithubView, WebsiteView

app = Typer(help="CLI tool to update GitHub README and website content.")


@app.command()
def github(
    data_dir: Annotated[
        Path, Option("--data-dir", "-d", help="Path to data directory.")
    ] = PATH,
    output_dir: Annotated[
        Path, Option("--output-dir", "-o", help="Output directory for README file.")
    ] = ROOT_DIR,
    output_file: Annotated[
        str, Option("--output-file", "-f", help="Output file name (e.g. README).")
    ] = "README",
) -> None:
    """Generate GitHub README.md file."""
    data = ReadmeData.from_dir(data_dir)
    view = GithubView(data, file_name=output_file, output_dir=output_dir)
    view.generate()


@app.command()
def website(
    data_dir: Annotated[
        Path, Option("--data-dir", "-d", help="Path to data directory.")
    ] = PATH,
    output_dir: Annotated[
        Path, Option("--output-dir", "-o", "--submodule", help="Output directory for website.")
    ] = SUBMOD,
) -> None:
    """Generate website markdown files and configurations."""
    data = ReadmeData.from_dir(data_dir)
    view = WebsiteView(data, output_dir=output_dir)
    view.generate()


if __name__ == "__main__":
    app()
