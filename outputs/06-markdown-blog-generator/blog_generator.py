#!/usr/bin/env python3
import os
import re
import markdown
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import argparse

class BlogGenerator:
    def __init__(self, source_dir="posts", output_dir="output"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.posts = []
        
    def parse_post_metadata(self, content):
        """Parse frontmatter metadata from markdown content."""
        metadata = {
            'title': 'Untitled',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tags': [],
            'author': 'Anonymous'
        }
        
        # Check for frontmatter
        if content.startswith('---'):
            try:
                end_index = content.index('---', 3)
                frontmatter = content[3:end_index].strip()
                content = content[end_index + 3:].strip()
                
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        if key == 'tags':
                            metadata[key] = [tag.strip() for tag in value.split(',')]
                        else:
                            metadata[key] = value
            except ValueError:
                pass
        
        return metadata, content

    def generate_slug(self, title):
        """Generate URL-friendly slug from title."""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def process_posts(self):
        """Process all markdown files in the source directory."""
        if not self.source_dir.exists():
            print(f"❌ Source directory '{self.source_dir}' does not exist!")
            return
        
        markdown_files = list(self.source_dir.glob('*.md'))
        
        if not markdown_files:
            print(f"📝 No markdown files found in '{self.source_dir}'")
            return
        
        print(f"🔍 Found {len(markdown_files)} markdown files")
        
        for md_file in markdown_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata, markdown_content = self.parse_post_metadata(content)
                
                # Convert markdown to HTML
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=['codehilite', 'fenced_code', 'tables']
                )
                
                # Generate slug
                slug = self.generate_slug(metadata['title'])
                
                post = {
                    'title': metadata['title'],
                    'date': metadata['date'],
                    'author': metadata['author'],
                    'tags': metadata['tags'],
                    'slug': slug,
                    'content': html_content,
                    'filename': md_file.stem
                }
                
                self.posts.append(post)
                print(f"✅ Processed: {metadata['title']}")
                
            except Exception as e:
                print(f"❌ Error processing {md_file}: {e}")
        
        # Sort posts by date (newest first)
        self.posts.sort(key=lambda x: x['date'], reverse=True)

    def generate_post_pages(self):
        """Generate individual post HTML pages."""
        post_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ post.title }} - My Blog</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <header>
        <nav>
            <a href="../index.html">← Back to Blog</a>
        </nav>
    </header>
    
    <main class="post-content">
        <article>
            <header class="post-header">
                <h1>{{ post.title }}</h1>
                <div class="post-meta">
                    <span class="date">{{ post.date }}</span>
                    <span class="author">by {{ post.author }}</span>
                    {% if post.tags %}
                    <div class="tags">
                        {% for tag in post.tags %}
                        <span class="tag">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
            </header>
            
            <div class="post-body">
                {{ post.content | safe }}
            </div>
        </article>
    </main>
</body>
</html>
        """)
        
        posts_dir = self.output_dir / 'posts'
        posts_dir.mkdir(parents=True, exist_ok=True)
        
        for post in self.posts:
            html_content = post_template.render(post=post)
            post_file = posts_dir / f"{post['slug']}.html"
            
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

    def generate_index_page(self):
        """Generate the main blog index page."""
        index_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>📝 My Blog</h1>
        <p>Welcome to my personal blog</p>
    </header>
    
    <main>
        <div class="posts-list">
            {% for post in posts %}
            <article class="post-preview">
                <h2><a href="posts/{{ post.slug }}.html">{{ post.title }}</a></h2>
                <div class="post-meta">
                    <span class="date">{{ post.date }}</span>
                    <span class="author">by {{ post.author }}</span>
                    {% if post.tags %}
                    <div class="tags">
                        {% for tag in post.tags %}
                        <span class="tag">{{ tag }}</span>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                <div class="post-excerpt">
                    {{ post.content[:200] | striptags }}...
                </div>
                <a href="posts/{{ post.slug }}.html" class="read-more">Read more →</a>
            </article>
            {% endfor %}
        </div>
    </main>
</body>
</html>
        """)
        
        html_content = index_template.render(posts=self.posts)
        index_file = self.output_dir / 'index.html'
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def generate_css(self):
        """Generate CSS styles for the blog."""
        css_content = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    color: #333;
    background-color: #f9f9f9;
}

header {
    background: #2c3e50;
    color: white;
    padding: 2rem 0;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

nav {
    padding: 1rem;
    background: #34495e;
}

nav a {
    color: white;
    text-decoration: none;
    font-weight: bold;
}

nav a:hover {
    text-decoration: underline;
}

main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 2rem;
}

.posts-list {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.post-preview {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.post-preview h2 {
    margin-bottom: 1rem;
}

.post-preview h2 a {
    color: #2c3e50;
    text-decoration: none;
}

.post-preview h2 a:hover {
    color: #3498db;
}

.post-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #666;
    flex-wrap: wrap;
}

.tags {
    display: flex;
    gap: 0.5rem;
}

.tag {
    background: #3498db;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    font-size: 0.8rem;
}

.post-excerpt {
    margin-bottom: 1rem;
    color: #555;
}

.read-more {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}

.read-more:hover {
    text-decoration: underline;
}

.post-content {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.post-header {
    border-bottom: 1px solid #eee;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}

.post-header h1 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.post-body {
    font-size: 1.1rem;
}

.post-body h1, .post-body h2, .post-body h3 {
    margin: 2rem 0 1rem 0;
    color: #2c3e50;
}

.post-body p {
    margin-bottom: 1rem;
}

.post-body code {
    background: #f4f4f4;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
}

.post-body pre {
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1rem 0;
}

@media (max-width: 768px) {
    main {
        padding: 0 1rem;
    }
    
    .post-preview, .post-content {
        padding: 1rem;
    }
    
    .post-meta {
        flex-direction: column;
        gap: 0.5rem;
    }
}
        """
        
        css_file = self.output_dir / 'styles.css'
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)

    def generate_blog(self):
        """Generate the complete blog."""
        print("🚀 Starting blog generation...")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process posts
        self.process_posts()
        
        if not self.posts:
            print("❌ No posts to generate!")
            return
        
        # Generate pages
        print("📄 Generating post pages...")
        self.generate_post_pages()
        
        print("🏠 Generating index page...")
        self.generate_index_page()
        
        print("🎨 Generating CSS...")
        self.generate_css()
        
        print(f"✅ Blog generated successfully!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Generated {len(self.posts)} posts")

def main():
    parser = argparse.ArgumentParser(description="Generate a static blog from Markdown files")
    parser.add_argument('--source', '-s', default='posts', help='Source directory for markdown files')
    parser.add_argument('--output', '-o', default='output', help='Output directory for generated blog')
    
    args = parser.parse_args()
    
    generator = BlogGenerator(args.source, args.output)
    generator.generate_blog()

if __name__ == "__main__":
    main()
        """