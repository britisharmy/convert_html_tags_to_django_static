from bs4 import BeautifulSoup
import os

def convert_static_tags(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Convert <script> tags
    script_tags = soup.find_all('script')
    for tag in script_tags:
        if 'src' in tag.attrs:
            src = tag['src']
            if not src.startswith('{% static') and not (src.startswith('https://') or src.startswith('http://')):
                tag['src'] = "{% static '" + src + "' %}"

    # Convert <link> tags
    link_tags = soup.find_all('link')
    for tag in link_tags:
        if 'href' in tag.attrs:
            href = tag['href']
            if not href.startswith('{% static') and not (href.startswith('https://') or href.startswith('http://')):
                tag['href'] = "{% static '" + href + "' %}"

    # Convert <img> tags
    img_tags = soup.find_all('img')
    for tag in img_tags:
        if 'src' in tag.attrs:
            src = tag['src']
            if not src.startswith('{% static') and not (src.startswith('https://') or src.startswith('http://')):
                tag['src'] = "{% static '" + src + "' %}"

    # Pretty-print the modified HTML
    modified_html = soup.prettify()

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(modified_html)


if __name__ == "__main__":
    folder_path = input("Enter the folder path containing HTML files: ")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]
        for html_file in html_files:
            html_file_path = os.path.join(folder_path, html_file)
            convert_static_tags(html_file_path)
        print("Conversion completed for all HTML files in the folder.")
    else:
        print("Folder not found. Please provide the correct folder path.")
