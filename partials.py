from bs4 import BeautifulSoup
import os

def add_load_static_tag(soup):
    head_tag = soup.find('head')
    if head_tag and not any(tag.name == 'script' and "{% load static %}" in tag for tag in head_tag.find_all()):
        load_static_tag = soup.new_string("{% load static %}")
        head_tag.insert(0, load_static_tag)

def convert_static_tags(soup):
    # Convert <script> tags
    script_tags = soup.find_all('script')
    for tag in script_tags:
        if 'src' in tag.attrs:
            src = tag['src']
            if not (src.startswith('{% static') or src.startswith('https://') or src.startswith('http://')):
                tag['src'] = "{% static '" + src + "' %}"

    # Convert <link> tags
    link_tags = soup.find_all('link')
    for tag in link_tags:
        if 'href' in tag.attrs:
            href = tag['href']
            if not (href.startswith('{% static') or href.startswith('https://') or href.startswith('http://')):
                tag['href'] = "{% static '" + href + "' %}"

    # Convert <img> tags
    img_tags = soup.find_all('img')
    for tag in img_tags:
        if 'src' in tag.attrs:
            src = tag['src']
            if not (src.startswith('{% static') or src.startswith('https://') or src.startswith('http://')):
                tag['src'] = "{% static '" + src + "' %}"

def create_header_footer_files(html_path, header_file, footer_file):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    header_tag = soup.find('header')
    if header_tag:
        with open(header_file, 'w', encoding='utf-8') as header_file:
            header_file.write(header_tag.prettify())

    footer_tag = soup.find('footer')
    if footer_tag:
        with open(footer_file, 'w', encoding='utf-8') as footer_file:
            footer_file.write(footer_tag.prettify())

def include_header_footer(html_path, header_file, footer_file):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    header_include = soup.new_tag('div')
    header_include.string = "{% include 'header.html' %}"

    footer_include = soup.new_tag('div')
    footer_include.string = "{% include 'footer.html' %}"

    # Place header include at the beginning of the body
    body_tag = soup.find('body')
    if body_tag:
        body_tag.insert(0, header_include)

    # Place footer include at the end of the body
    if body_tag:
        body_tag.append(footer_include)

    # Pretty-print the modified HTML
    modified_html = soup.prettify()

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(modified_html)

if __name__ == "__main__":
    html_file_path = input("Enter the HTML file path: ")
    header_file = "header.html"
    footer_file = "footer.html"

    if os.path.exists(html_file_path):
        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        add_load_static_tag(soup)
        convert_static_tags(soup)
        create_header_footer_files(html_file_path, header_file, footer_file)
        include_header_footer(html_file_path, header_file, footer_file)

        print("Conversion completed.")
    else:
        print("File not found. Please provide the correct file path.")
