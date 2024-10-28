import os
import subprocess
from datetime import datetime
import markdown
from markdown.extensions.meta import MetaExtension

def generate_html_for_md_files():
    # Get all .md files in the current directory
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    for md_file in md_files:
        # Call the previously created script to convert each .md file to .html
        subprocess.run(['python3', 'trans.py', md_file])

    # Generate index.html
    generate_index_html(md_files)

def generate_index_html(md_files):
    # Get the current date
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # HTML template for the index file
    index_html_template = f"""
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/colin.jpg">

  <!-- Need to change in every new file  -->
  <link rel="canonical" href="https://www.oyyko.com/blog">

  <title>Colin Zhang</title>
  <!-- <meta name="title" content="Colin Zhang"> -->
  <!-- <meta name="description" content="Colin Zhang's personal website"> -->

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Edu+AU+VIC+WA+NT+Hand:wght@400..700&family=IBM+Plex+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Prata&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/atom-one-light.min.css">
</head>

<body>
  <header>
    <h1>Colin Zhang</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/blog/">Blog</a>
      <a href="/about/">About</a>
      <a href="/resume.pdf">Resume</a>
    </nav>
  </header>

  <div class="blog-list">
    {generate_blog_list(md_files)}
  </div>
  
  

  <footer>
    <p>© 2024 Colin Zhang. All rights reserved.</p>
    <p>Last updated on {current_date}.</p>
  </footer>
</body>

</html>
"""

    # Write the index.html content to the output file
    with open('index.html', 'w', encoding='utf-8') as index_file:
        index_file.write(index_html_template)

    print("Generated index.html")

def generate_blog_list(md_files):
    blog_list_html = ""
    for md_file in md_files:
        # Parse the markdown file to extract meta information
        with open(md_file, 'r', encoding='utf-8') as file:
            text = file.read()
            md = markdown.Markdown(extensions=[MetaExtension()])
            md.convert(text)
            meta_info = md.Meta

        # Use meta information for the post title and date
        post_title = meta_info.get('title', [os.path.splitext(md_file)[0]])[0]
        post_date = meta_info.get('date', [datetime.fromtimestamp(os.path.getmtime(md_file)).strftime("%Y-%m-%d")])[0]
        post_link = os.path.splitext(md_file)[0] + ".html"
        
        blog_list_html += f"""
    <div class="blog-item">
      <div class="link"><a href="/blog/{post_link}">{post_title}</a></div>
      <div class="date">{post_date}</div>
    </div>
"""
    return blog_list_html

if __name__ == "__main__":
    generate_html_for_md_files()
