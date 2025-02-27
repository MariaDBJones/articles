import os
import re
import json
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import markdown

# Your Medium RSS feed
feed_url = 'https://medium.com/feed/@arbaudie.it'
feed = feedparser.parse(feed_url)

# Create articles directory if it doesn't exist
os.makedirs('articles', exist_ok=True)

# Create or update index file
index_content = "# arbaudie.it's Medium Articles\n\n"
index_content += "Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + "\n\n"

# Process each article
for entry in feed.entries:
    # Extract metadata
    title = entry.title
    link = entry.link
    published = entry.published
    
    try:
        updated = entry.updated
    except AttributeError:
        updated = published
    
    # Create filename from title (sanitize for filesystem)
    filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
    filename = re.sub(r'[\s]+', '-', filename)
    
    # Get article content
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to extract the article content (this varies based on Medium's structure)
    article_section = soup.find('article')
    if article_section:
        content = str(article_section)
    else:
        # Fallback to getting what we can from the RSS feed
        content = entry.content[0].value if 'content' in entry else entry.summary
    
    # Create markdown file with frontmatter
    md_content = f"""---
title: "{title}"
date: {published}
lastUpdated: {updated}
link: {link}
---

{content}
"""
    
    # Write to file
    with open(f'articles/{filename}.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Add to index
    try:
        pub_date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")
    except ValueError:
        # Handle alternative date formats if needed
        pub_date = published
    
    index_content += f"- [{title}](articles/{filename}.md) - {pub_date}\n"

# Write index file
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"Processed {len(feed.entries)} articles from Medium")
