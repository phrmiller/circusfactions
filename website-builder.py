import os
import glob
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

# Start virtual environment with `source env/bin/activate`
# Deactivate the virtual environment with `deactivate`

# This program builds all of the web pages for Circus Factions.

# Before creating new web pages, delete all of the old web pages.
old_files = glob.glob('html/*.html')
for f in old_files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

# Create the empty dictionary 'posts', 
# then use markdown2 to populate 'posts' with each markdown post from the posts folder,
# then sort the posts in the dictionary by date metadata from newest to oldest.
posts = {}
for markdown_post in os.listdir('posts'):
    file_path = os.path.join('posts', markdown_post)
    with open(file_path, 'r') as file:
        posts[markdown_post] = markdown(file.read(), extras=['metadata'])
posts = {
    post: posts[post] for post in sorted(posts, key=lambda post: datetime.strptime(posts[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

# Load jinja2 templates for each type of page you want to create.
env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')

# Create a new list 'posts_metadata', where each item is the dictionary of metadata from each post in the 'posts' dictionary
posts_metadata = [posts[post].metadata for post in posts]

# Create a new list 'tags', where each item is the tags
# tags = [post['tags'] for post in posts_metadata]

# Create a new list 'posts_urls', where each item is the post name and '.md' is replaced with '.html'.
posts_urls = [post.replace('.md','.html') for post in posts]

# Render html for index page and write to index.html
index_html = index_template.render(posts=zip(posts_metadata, posts_urls))
with open('html/index.html', 'w') as file:
    file.write(index_html)

# Render each post's html and write to post-file-name.html
for post in posts:
    post_metadata = posts[post].metadata
    post_data = {
        'content': posts[post],
        'title': post_metadata['title'],
        'date': post_metadata['date']
    }
    post_html = post_template.render(post=post_data)
    post_file_path = 'html/{title}.html'.format(title=post.replace('.md',''))

    with open(post_file_path, 'w') as file:
        file.write(post_html)