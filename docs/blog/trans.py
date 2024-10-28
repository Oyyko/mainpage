from datetime import datetime
import markdown
import sys
import os

def convert_md_to_html(md_filename):
    # 读取 Markdown 文件
    with open(md_filename, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()

    # 初始化 Markdown 转换器，添加 'fenced_code', 'meta', 和 'toc' 扩展
    md = markdown.Markdown(extensions=['fenced_code', 'meta', 'toc'])

    # 将 Markdown 转换为 HTML
    html_content = md.convert(markdown_text)

    # 获取生成的目录 HTML
    toc_html = md.toc

    # 获取元数据
    meta_info = md.Meta

    # 提取标题和日期
    post_title = meta_info.get('title', [os.path.splitext(md_filename)[0]])[0]
    post_date = meta_info.get('date', [datetime.fromtimestamp(os.path.getmtime(md_filename)).strftime("%Y-%m-%d")])[0]

    # 格式化日期（确保为 YYYY-MM-DD 格式）
    try:
        parsed_date = datetime.strptime(post_date, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        # 如果日期格式不正确，使用默认格式
        formatted_date = post_date

    # 获取当前日期
    current_date = datetime.now().strftime("%B %d, %Y")

    # HTML 模板，包含标题、日期、分割线和目录部分
    html_template = f"""
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/colin.jpg">

  <!-- 每个新文件需要更改 -->
  <link rel="canonical" href="https://www.oyyko.com/blog">

  <title>{post_title} - Colin Zhang</title>
  <!-- <meta name="title" content="{post_title}"> -->
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

  <!-- 文章标题 -->
  <div class="post-title">{post_title}</div>

  <!-- 文章日期 -->
  <div class="post-date">{formatted_date}</div>

  <!-- 分割线 -->

  <!-- 目录部分开始 -->
  <div class="table-of-contents">
    <h2>Table of Contents</h2>
    {toc_html}
  </div>
  <!-- 目录部分结束 -->

  <!-- 正文内容开始 -->
  {html_content}
  <!-- 正文内容结束 -->

  <footer>
      <p>© 2024 Colin Zhang. All rights reserved.</p>
      <p>Last updated on {current_date}.</p>
  </footer>
  
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/highlight.min.js"></script>
  <script>hljs.highlightAll();</script>
</body>

</html>
"""

    # 将 HTML 内容写入输出文件
    html_filename = md_filename.replace('.md', '.html')
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_template)

    print(f"Converted {md_filename} to {html_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trans.py <filename.md>")
    else:
        md_filename = sys.argv[1]
        convert_md_to_html(md_filename)
