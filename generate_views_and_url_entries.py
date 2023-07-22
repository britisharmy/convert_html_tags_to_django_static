import os
import re
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.shortcuts import render

def create_view_methods(folder_path):
    view_methods = []

    # Get all HTML files in the folder
    html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

    for html_file in html_files:
        # Generate the method name from the HTML file name
        method_name = re.sub(r'[^a-zA-Z0-9_]', '', os.path.splitext(html_file)[0])
        method_name = method_name.replace('-', '_')  # Replace hyphens with underscores

        # Define the view method
        def view_method(request):
            # Your logic for the view method goes here
            return render(request, f'frontend/{html_file}')

        view_methods.append((method_name, view_method))

    return view_methods

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing HTML files: ")

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        view_methods = create_view_methods(folder_path)

        # Write the view methods to a views.py file
        with open("views.py", "w", encoding="utf-8") as views_file:
            for method_name, view_method in view_methods:
                views_file.write(f"def {method_name}(request):\n")
                views_file.write(f"    # Your logic for the {method_name} method goes here\n")
                views_file.write(f"    return render(request, 'frontend/{method_name}.html')\n")

        # Update urls.py with the urlpatterns
        with open("urls.py", "w", encoding="utf-8") as urls_file:
            urls_file.write("from django.contrib import admin\n")
            urls_file.write("from django.urls import path, include, re_path\n")
            urls_file.write("from django.views.generic import TemplateView\n")
            urls_file.write("from django.shortcuts import render\n\n")
            urls_file.write("urlpatterns = [\n")
            urls_file.write("    path('admin/', admin.site.urls),\n")
            for method_name, _ in view_methods:
                urls_file.write(f"    path('{method_name}/', {method_name}, name='{method_name}'),\n")
            urls_file.write("    re_path(r'^.*$', TemplateView.as_view(template_name='404.html')),\n")
            urls_file.write("]")

        print("View methods and URLs created successfully.")
    else:
        print("Folder not found. Please provide the correct folder path.")
