import os
import re

def remove_django_tags_from_file(file_path):
    # Regular expression to find Django tags {% ... %}
    django_tag_pattern = r"{%\s*([^%]+)\s*%}"

    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Remove all occurrences of Django tags from the file
    file_content = re.sub(django_tag_pattern, "", file_content)

    # Write the modified content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)

def convert_static_tags_to_base_url(folder_path):
    # Regular expression to find the Django-style static tag
    static_tag_pattern = r"{%\s*static\s*'([^']+?)'\s*%}"

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            # Remove Django tags from the file
            remove_django_tags_from_file(file_path)

            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            # Find all occurrences of the Django-style static tag in the file
            matches = re.findall(static_tag_pattern, file_content)

            if matches:
                # Replace each occurrence with CodeIgniter-style PHP code, skipping URLs starting with https or http
                for match in matches:
                    codeigniter_style = "<?php echo base_url('%s'); ?>" % match
                    static_tag = "{%% static '%s' %%}" % match

                    # Check if the URL starts with http or https
                    if static_tag.startswith("https") or static_tag.startswith("http"):
                        continue

                    file_content = file_content.replace(static_tag, codeigniter_style)

                # Write the modified content back to the file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_content)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    convert_static_tags_to_base_url(folder_path)
