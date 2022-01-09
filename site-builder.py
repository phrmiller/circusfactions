import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

posts = {}

for markdown_post in os.listdir('posts'):
    file_path = os.path.join('posts', markdown_post)

    with open(file_path, 'r') as file:
        posts[markdown_post] = markdown(file.read(), extras=['metadata'])

posts = {
    post: posts[post] for post in sorted(posts, key=lambda post: datetime.strptime(posts[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

env = Environment(loader=PackageLoader('site-builder', 'templates'))
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')

posts_metadata = [posts[post].metadata for post in posts]
tags = [post['tags'] for post in posts_metadata]
index_html = index_template.render(posts=posts_metadata, tags=tags)

with open('html/index.html', 'w') as file:
    file.write(index_html)

for post in posts:
    post_metadata = posts[post].metadata

    post_data = {
        'content': posts[post],
        'title': post_metadata['title'],
        'date': post_metadata['date']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'html/{title}.html'.format(title=post_metadata['title'])

    with open(post_file_path, 'w') as file:
        file.write(post_html)