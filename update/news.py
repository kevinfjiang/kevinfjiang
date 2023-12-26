import yaml
from config import PATH, SUBMOD
from dateutil import parser
from mdutils import MdUtils

with open(PATH / "news.yml") as news:
    news_info = yaml.load(news, Loader=yaml.FullLoader)


def format_news(news_entry: list[dict[str, str]]) -> list[str]:
    for entry in sorted(
        news_entry, key=lambda en: parser.parse(en["date"], fuzzy=True), reverse=True
    ):
        date = parser.parse(entry["date"])
        raw = f"<strong>[{date.strftime('%b. %Y')}]</strong> {entry['description']}"
        yield f"[{raw}]({entry['link']})" if "link" in entry else raw


def update_website_news():
    news = MdUtils(str(SUBMOD / "_includes" / "news.md"))
    news.new_line("## News")
    news.new_list(format_news(news_info["news"]))
    news.create_md_file()
