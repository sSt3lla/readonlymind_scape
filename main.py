#Made with alof of chatgpt help

import requests
import pdfkit
import argparse
from bs4 import BeautifulSoup

def get_chapter_amount(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    chapter_links = soup.find_all('a', class_='chapter-link')
    return len(chapter_links)

def html_encode_non_ascii(text: str):
    return ''.join(f'&#{ord(char)};' if ord(char) > 127 else char for char in text)

def main(url, output, start_chapter=None, end_chapter=None):
    chapter_amount = get_chapter_amount(url)

    combined_html = '''
<html>
<head>
<style>
body {
    font-family: Arial, sans-serif;
}
h1 {
    text-align: center;
}
.foreword-box {
    background-color: #f0f0f0;
    padding: 10px;
    margin: 20px 0;
    border: 1px solid #ccc;
    line-height: 0.8;
}
</style>
</head>
<body>
    '''

    # Use the provided chapter range or the entire range if not specified
    start_chapter = start_chapter if start_chapter else 1
    end_chapter = end_chapter if end_chapter else chapter_amount

    for i in range(start_chapter, end_chapter + 1):
        chapter_url = f'{url}/{i}'
        page = requests.get(chapter_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        foreword_content = soup.find('section', id='foreword')
        chapter_content = soup.find('section', id='chapter-content')

        foreword_html = str(foreword_content) if foreword_content else ''
        chapter_html = str(chapter_content) if chapter_content else ''

        foreword_html = html_encode_non_ascii(foreword_html)
        chapter_html = html_encode_non_ascii(chapter_html)

        if foreword_content:
            chapter_html = f'''
<h1>Chapter {i}</h1>
<div class="foreword-box">{foreword_html}</div>
            {chapter_html}
            '''
        else:
            chapter_html = f'''
<h1>Chapter {i}</h1>
            {chapter_html}
            '''

        combined_html += chapter_html

    combined_html += '''
</body>
</html>
    '''

    pdfkit.from_string(combined_html, output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape chapters from a website and convert to PDF.')
    parser.add_argument('url', type=str, help='The base URL of the chapters.')
    parser.add_argument('output', type=str, help='The output PDF file path.')
    parser.add_argument('--start', type=int, default=None, help='The starting chapter number.')
    parser.add_argument('--end', type=int, default=None, help='The ending chapter number.')
    
    args = parser.parse_args()
    
    main(args.url, args.output, args.start, args.end)
