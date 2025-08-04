# Markdown Blog Generator

A static blog generator that converts Markdown files to a beautiful HTML blog.

## Features

- Convert Markdown files to HTML blog posts
- Support for frontmatter metadata (title, date, author, tags)
- Automatic index page generation with post listings
- Responsive CSS styling
- Syntax highlighting for code blocks
- Clean, readable typography
- Command-line interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Create your blog posts as Markdown files in the `posts/` directory
2. Add frontmatter to your posts:

```markdown
---
title: My Blog Post
date: 2024-01-15
author: Your Name
tags: python, tutorial, web
---

# Your content here...
```

3. Generate your blog:

```bash
python blog_generator.py
```

4. Open `output/index.html` in your browser

## Command Line Options

```bash
# Use custom source and output directories
python blog_generator.py --source my_posts --output my_blog

# Short form
python blog_generator.py -s my_posts -o my_blog
```

## Sample Posts

The generator includes sample posts to get you started:
- `posts/welcome.md` - Welcome post
- `posts/python-tips.md` - Python programming tips

## Output Structure

```
output/
├── index.html          # Main blog page
├── styles.css          # Blog styling
└── posts/
    ├── welcome.html
    └── python-tips.html
```

## Frontmatter Options

- `title`: Post title (required)
- `date`: Publication date (YYYY-MM-DD format)
- `author`: Author name
- `tags`: Comma-separated list of tags

## Requirements

- Python 3.6+
- markdown
- Jinja2
- Pygments (for syntax highlighting)