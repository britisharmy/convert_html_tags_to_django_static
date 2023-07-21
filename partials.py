from bs4 import BeautifulSoup
import os
import shutil

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

def create_header_footer_files(html_path, header_file, footer_file):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    header_tag = soup.find('header')
    if header_tag:
        with open(header_file, 'w', encoding='utf-8') as header_file:
            header_file.write(header_tag.prettify())
        header_tag.decompose()

    footer_tag = soup.find('footer')
    if footer_tag:
        with open(footer_file, 'w', encoding='utf-8') as footer_file:
            footer_file.write(footer_tag.prettify())
        footer_tag.decompose()

def include_header_footer(soup, header_file, footer_file):
    header_include = soup.new_tag('div')
    header_include.string = "{% include '" + os.path.basename(header_file) + "' %}"

    footer_include = soup.new_tag('div')
    footer_include.string = "{% include '" + os.path.basename(footer_file) + "' %}"

    # Place header include at the beginning of the body
    body_tag = soup.find('body')
    if body_tag:
        body_tag.insert(0, header_include)

    # Place footer include at the end of the body
    if body_tag:
        body_tag.append(footer_include)

if __name__ == "__main__":
    html_file_path = input("Enter the HTML file path: ")
    header_file = "header.html"
    footer_file = "footer.html"

    if os.path.exists(html_file_path):
        # Create a backup of the original HTML file
        shutil.copy(html_file_path, html_file_path + ".bak")

        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        add_load_static_tag(soup)
        convert_to_django_static(soup, 'src')
        convert_to_django_static(soup, 'href')

        create_header_footer_files(html_file_path, header_file, footer_file)
        include_header_footer(soup, header_file, footer_file)

        # Pretty-print the modified HTML
        modified_html = soup.prettify()

        # Save the modified HTML to the original file
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_html)

        print("Conversion completed.")
    else:
        print("File not found. Please provide the correct file path.")
