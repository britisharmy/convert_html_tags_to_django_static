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
            if not src.startswith('{% static'):
                tag['src'] = "{% static '" + src + "' %}"

    # Convert <link> tags
    link_tags = soup.find_all('link')
    for tag in link_tags:
        if 'href' in tag.attrs:
            href = tag['href']
            if not href.startswith('{% static'):
                tag['href'] = "{% static '" + href + "' %}"

    # Convert <img> tags
    img_tags = soup.find_all('img')
    for tag in img_tags:
        if 'src' in tag.attrs:
            src = tag['src']
            if not src.startswith('{% static'):
                tag['src'] = "{% static '" + src + "' %}"

    # Pretty-print the modified HTML
    modified_html = soup.prettify()

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(modified_html)


if __name__ == "__main__":
    html_file_path = input("Enter the HTML file path: ")
    if os.path.exists(html_file_path):
        convert_static_tags(html_file_path)
        print("Conversion completed.")
    else:
        print("File not found. Please provide the correct file path.")
