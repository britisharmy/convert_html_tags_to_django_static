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
        if 'src' in tag.attrs and not tag['src'].startswith(('{% static', 'https://', 'http://')):
            tag['src'] = "{% static '" + tag['src'] + "' %}"

    # Convert <link> tags
    link_tags = soup.find_all('link')
    for tag in link_tags:
        if 'href' in tag.attrs and not tag['href'].startswith(('{% static', 'https://', 'http://')):
            tag['href'] = "{% static '" + tag['href'] + "' %}"

    # Convert <img> tags
    img_tags = soup.find_all('img')
    for tag in img_tags:
        if 'src' in tag.attrs and not tag['src'].startswith(('{% static', 'https://', 'http://')):
            tag['src'] = "{% static '" + tag['src'] + "' %}"

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing HTML files: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]
        for html_file in html_files:
            html_file_path = os.path.join(folder_path, html_file)

            with open(html_file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            add_load_static_tag(soup)
            convert_static_tags(soup)

            # Pretty-print the modified HTML
            modified_html = soup.prettify()

            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(modified_html)

        print("Conversion completed for all HTML files in the folder.")
    else:
        print("Folder not found. Please provide the correct folder path.")
