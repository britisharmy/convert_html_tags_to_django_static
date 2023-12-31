# convert_html_tags_to_django_static
Convert HTML tags to Django static

# Install beautiful soup

`pip install beautifulsoup4`

# Run The Script

`python convert_static.py`

Enter the file you want to convert the tags for. 

# Use Cases

You have purchased a html theme off themeforest for instance and you want to quickly turn the template into a  website fast. The template comes with many absolute paths to the assets and you just want to get the tags for images, scripts or css working ASAP.

You can use the script to save you hours even days.

# Caution

Always back up your files before running the script to avoid accidental data loss.

# Future Plans

- Make it possible to convert all html files in a specific folder

# Untested convert all files inside a specific folder

- [x] Done

# Added Partials Isolation

- I added partials isolation. For now, `partials.py` will isolate `<footer>` into `footer.html` and write an include in your target file. This also happens for `<header>`

# Added ability to generate view methods based on html file names and make urls.py entries. 

- You can now generate view names and have url entries created for you to ensure you move even faster.

# Added script to inject existing partials to your target file

- Supposing you have `header.html` and `footer.html` already created, run `create_partials_includes_without_file_creation.py` to avoid repeating creating fresh html files.
  
Cheers.

