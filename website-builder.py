import os
import glob
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

# This script builds pages for Circus Factions.


# PREP TASKS #

# Before creating new pages, delete old pages.
old_files = glob.glob('html/*.html*') + glob.glob('html/categories/*.html*')
for f in old_files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

# Generate new CSS file from SCSS file.
os.system("sass style.scss ./html/styles/style.css")


# GATHER POSTS #

# Use markdown2 gather each markdown post, then sort posts by date metadata.
posts = {}
for markdown_post in os.listdir('posts'):
    if markdown_post.endswith('.md'): # Avoids an issues with Mac OS's ds_store file.
        file_path = os.path.join('posts', markdown_post)
        with open(file_path, 'r') as file:
            posts[markdown_post] = markdown(file.read(), extras=['metadata'])
for post in posts:
    posts[post].metadata['date'] = datetime.strptime(posts[post].metadata['date'], '%Y-%m-%d')
posts = {
    post: posts[post] for post in sorted(posts, key=lambda post: posts[post].metadata['date'], reverse=True)
}


# ESTABLISH ENTITIES THAT WILL BE PASSED TO JINJA TEMPLATES #

# Create a new list 'posts_metadata', where each item is the dictionary of metadata from each post in the 'posts' dictionary.
posts_metadata = [posts[post].metadata for post in posts]
# Create a new list 'posts_urls', where each item is the post name and '.md' is replaced with '.html'.
posts_urls = [post.replace('.md','.html') for post in posts]
# Create a new dictionary for category counts, sort based on count.
category_counts = {}
all_categories = []
for post in posts:
    all_categories.extend(posts[post].metadata['categories'].split(","" "))
for i in all_categories:
    category_counts[i] = category_counts.get(i, 0) + 1
category_counts = {
    category: category_counts[category] for category in sorted(category_counts, key=lambda category: category_counts[category], reverse=True)
}


# LOAD JINJA TEMPLATES #

env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')
all_template = env.get_template('all.html')
categories_template = env.get_template('categories.html')
category_template = env.get_template('category.html')
about_template = env.get_template('about.html')


# BUILD PAGES #

# Render Index page.
index_html = index_template.render(posts=list(zip(posts_metadata, posts_urls,)), categories=category_counts)
with open('html/index.html', 'w') as file:
    file.write(index_html)
# Render each Post page.
for post in posts:
    post_metadata = posts[post].metadata
    post_data = {
        'content': posts[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'categories': post_metadata['categories']
    }
    post_html = post_template.render(post=post_data)
    post_file_path = 'html/{title}.html'.format(title=post.replace('.md',''))
    with open(post_file_path, 'w') as file:
        file.write(post_html)
# Render All page.
all_html = all_template.render(posts=list(zip(posts_metadata, posts_urls)))
with open('html/all.html', 'w') as file:
    file.write(all_html)
# Render Categories page
categories_html = categories_template.render(categories=category_counts)
with open('html/categories.html', 'w') as file:
    file.write(categories_html)
# Render each Category page
for category in category_counts:
    category_html = category_template.render(posts=list(zip(posts_metadata, posts_urls)), categories=category)
    category_file_path = 'html/categories/{title}.html'.format(title=category)
    with open(category_file_path, 'w') as file:
        file.write(category_html)
# Render About page
with open('./templates/about.md', 'r') as file:
    about_content = markdown(file.read())
about_html = about_template.render(about=about_content)
with open('html/about.html', 'w') as file:
    file.write(about_html)