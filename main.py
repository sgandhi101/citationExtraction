import os
import tempfile
from docx2python import docx2python
import re

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def extract_footnotes():
    if request.method == 'POST':
        # Get the file from the POST request
        file = request.files['file']

        # Save the file to a temporary directory
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        # Extract the footnotes from the file
        footnotes = extract_footnotes_from_doc(file_path)

        # Delete the file
        os.remove(file_path)

        # Render the result template
        return render_template('result.html', footnotes=footnotes)
    else:
        # Render the file upload form
        return render_template('form.html')


def extract_footnotes_from_doc(doc_path):
    # Use the docx2python library to convert the .docx file at the given path to HTML
    doc = docx2python(doc_path, html=True)

    # Create an empty list to store the footnotes
    footnote_list = []

    # Iterate over the footnotes in the document
    for footnote in doc.footnotes_runs[0][0]:
        # Iterate over the lines in the footnote
        for specific in footnote:
            for line in specific:
                # Split the line by the tab character
                split_lines = line.split("\t")
                # If the line starts with "footnote", extract the footnote number
                if "footnote" in split_lines[0]:
                    footnote_list.append(re.sub(r'\D', '', split_lines[0]))
                # Otherwise, append the line as is
                else:
                    footnote_list.append(split_lines[0])

    # Return the list of footnotes
    return footnote_list


if __name__ == '__main__':
    app.run()
