import feedparser
import requests
from datetime import datetime

def fetch_blog_entries():
    entries = feedparser.parse("https://daltonturner.xyz/feed.xml")["entries"]
    
    # Convert the published date to datetime and sort the entries in descending order
    sorted_entries = sorted(
        entries,
        key=lambda entry: datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %Z"),
        reverse=True  # This ensures the entries are in descending order
    )
    
    return [
        {
            "title": entry.title,
            "url": entry.link,
            "published": datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
        }
        for entry in sorted_entries[:5]
    ]

def main():
    blog_entries = fetch_blog_entries()
    blog_entries_markdown = "\n".join(
        [f"* [{entry['title']}]({entry['url']}) - Published on {entry['published']}" for entry in blog_entries]
    )

    with open('README.md', 'r') as f:
        lines = f.readlines()

    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if "## Recent blog posts" in line:
            start_index = i
        elif start_index is not None and line.strip() == "":
            end_index = i
            break

    # If end_index is not set, assume the section goes until the end of the file
    if end_index is None:
        end_index = len(lines) - 1

    if start_index is not None:
        del lines[start_index:end_index + 1]
        lines.insert(start_index, "## Recent blog posts\n" + blog_entries_markdown + "\n")
    else:
        new_section = "## Recent blog posts\n" + blog_entries_markdown + "\n"
        lines.extend(new_section.splitlines())


    with open('README.md', 'w') as f:
        f.writelines(lines)

if __name__ == "__main__":
    main()
