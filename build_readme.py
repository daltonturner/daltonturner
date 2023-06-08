import feedparser
import requests
from datetime import datetime

def fetch_blog_entries():
    entries = feedparser.parse("https://daltonturner.xyz/feed.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": "https://daltonturner.xyz" + entry["link"],
            "published": datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d"),
        }
        for entry in entries[:5]
    ]

def main():
    blog_entries = fetch_blog_entries()
    blog_entries_markdown = "\n".join(
        [f"* [{entry['title']}]({entry['url']}) - Published on {entry['published']}" for entry in blog_entries]
    )

    with open('README.md', 'r') as f:
        lines = f.readlines()
    with open('README.md', 'w') as f:
        in_blog_entries_section = False
        for line in lines:
            if line.strip() == "## Recent blog posts":
                in_blog_entries_section = True
            if not in_blog_entries_section:
                f.write(line)
        f.write("\n## Recent blog posts\n")
        f.write(blog_entries_markdown)

if __name__ == "__main__":
    main()

