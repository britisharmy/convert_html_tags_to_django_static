import os
from bs4 import BeautifulSoup

def custom_prettify(soup):
    # Custom prettify function to preserve PHP tags and insert < and > instead of &lt; and &gt;
    pretty_html = soup.prettify(formatter=lambda s: str(s).replace("&lt;", "<").replace("&gt;", ">"))
    return pretty_html

def convert_absolute_paths_to_base_url(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(file_content, "html.parser")

            # Find all elements with href or src attributes
            elements = soup.find_all(["link", "script", "img"], href=True) + soup.find_all(["script", "img"], src=True)

            # Replace absolute paths with CodeIgniter-style base_url()
            for element in elements:
                attr_name = "href" if element.has_attr("href") else "src"
                absolute_path = element.get(attr_name)

                if not absolute_path.startswith(("http://", "https://")) and "<?php echo base_url(" not in absolute_path:
                    base_url_style = f"<?php echo base_url('{absolute_path.strip()}'); ?>"
                    element[attr_name] = base_url_style

            # Write the modified content back to the file with custom prettify function
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(custom_prettify(soup))

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    convert_absolute_paths_to_base_url(folder_path)
