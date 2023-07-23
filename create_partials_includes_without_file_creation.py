from bs4 import BeautifulSoup
import os

def add_load_static_tag(soup):
    head_tag = soup.find('head')
    if head_tag and not any(tag.name == 'script' and "{% load static %}" in tag.string for tag in head_tag.find_all()):
        load_static_tag = soup.new_string("{% load static %}")
        head_tag.insert(0, load_static_tag)

def convert_to_django_static(soup, attribute):
    elements = soup.find_all(attrs={attribute: True})
    for el in elements:
        attr_value = el[attribute]
        if not (attr_value.startswith('{% static') or attr_value.startswith('https://') or attr_value.startswith('http://')):
            if not attr_value.startswith(('https://', 'http://')):
                # Add quotes around the Django style static tag
                attr_value = "{% static '" + attr_value + "' %}"
                el[attribute] = attr_value

def include_header_footer(soup):
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

def process_html_file(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    add_load_static_tag(soup)
    convert_to_django_static(soup, 'src')
    convert_to_django_static(soup, 'href')
    include_header_footer(soup)

    # Pretty-print the modified HTML
    modified_html = soup.prettify()

    # Save the modified HTML to the original file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_html)

if __name__ == "__main__":
    html_file_path = input("Enter the HTML file path: ")

    if os.path.exists(html_file_path):
        process_html_file(html_file_path)
        print("Conversion completed.")
    else:
        print("File not found. Please provide the correct file path.")
