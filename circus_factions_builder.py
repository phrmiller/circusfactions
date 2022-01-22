import os
import glob
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown


# PREP TASKS #

# Delete old pages.
old_files = glob.glob('html/*.html*') + glob.glob('html/categories/*.html*')
for f in old_files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

# Generate CSS from SCSS.
os.system("sass style.scss ./html/styles/style.css")


# GATHER POSTS, CATEGORY, AND ABOUT INFO #

# Use markdown2 to load each post into 'posts'.
posts = {}
for markdown_post in os.listdir('posts'):
    if markdown_post.endswith('.md'): # Avoids an issues with Mac OS's ds_store file.
        file_path = os.path.join('posts', markdown_post)
        with open(file_path, 'r') as file:
            posts[markdown_post] = markdown(file.read(), extras=['metadata'])

# Convert 'posts' 'date' metadata to datetime.
for post in posts:
    posts[post].metadata['date'] = datetime.strptime(posts[post].metadata['date'], '%Y-%m-%d')

# Sort 'posts' by 'date'.
posts = {
    post: posts[post] for post in sorted(posts, key=lambda post: posts[post].metadata['date'], reverse=True)
}

# Gather 'all_categories' from posts metadata.
all_categories = []
for post in posts:
    all_categories.extend(posts[post].metadata['categories'].split(","" "))

# Gather 'category_counts' for each category in 'all_categories'.
category_counts = {}
for i in all_categories:
    category_counts[i] = category_counts.get(i, 0) + 1

# Sort 'category_counts' by count.
category_counts = {
    category: category_counts[category] for category in sorted(category_counts, key=lambda category: category_counts[category], reverse=True)
}

# Use markdown2 to load 'about.md' to 'about_content'. 
with open('./templates/about.md', 'r') as file:
    about_content = markdown(file.read())


# LOAD JINJA TEMPLATES

env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')
all_template = env.get_template('all.html')
categories_template = env.get_template('categories.html')
category_template = env.get_template('category.html')
about_template = env.get_template('about.html')


# BUILD PAGES

# Build 'index.html' page.
index_html = index_template.render(posts=posts)
with open('html/index.html', 'w') as file:
    file.write(index_html)

# Build each 'post' page.
for post in posts:
    post_html = post_template.render(posts=posts, post=post)
    post_file_path = 'html/{title}.html'.format(title=post.replace('.md',''))
    with open(post_file_path, 'w') as file:
        file.write(post_html)

# Build 'all' page.
all_html = all_template.render(posts=posts)
with open('html/all.html', 'w') as file:
    file.write(all_html)

# Build 'categories' page.
categories_html = categories_template.render(categories=category_counts)
with open('html/categories.html', 'w') as file:
    file.write(categories_html)

# Build each 'category' page.
for category in category_counts:
    category_html = category_template.render(posts=posts, category=category)
    category_file_path = 'html/categories/{title}.html'.format(title=category)
    with open(category_file_path, 'w') as file:
        file.write(category_html)

# Build 'about' page.
about_html = about_template.render(about=about_content)
with open('html/about.html', 'w') as file:
    file.write(about_html)