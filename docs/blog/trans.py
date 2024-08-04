#!/usr
import markdown
import sys

def convert_md_to_html(md_filename):
    # Read the Markdown file
    with open(md_filename, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text)
    
    current_date = datetime.now().strftime("%B %d, %Y")

    # HTML template with the specified header and footer
    html_template = f"""
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
  <link href="https://fonts.googleapis.com/css2?family=Edu+AU+VIC+WA+NT+Hand:wght@400..700&family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
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

  {html_content}

  <footer>
      <p>© 2024 Colin Zhang. All rights reserved.</p>
      <p>Last updated on {current_date}.</p>
  </footer>
</body>

</html>
"""

    # Write the HTML content to the output file
    html_filename = md_filename.replace('.md', '.html')
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_template)

    print(f"Converted {md_filename} to {html_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_md_to_html.py <filename.md>")
    else:
        md_filename = sys.argv[1]
        convert_md_to_html(md_filename)
