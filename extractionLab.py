import re

from docx2python import docx2python

# extract docx content with basic font styles converted to html
doc = docx2python('Final_Project copy.docx', html=True)
footnote_list = []

for footnote in doc.footnotes_runs[0][0]:
    for specific in footnote:
        for line in specific:
            split_lines = line.split("\t")
            if "footnote" in split_lines[0]:
                footnote_list.append(re.sub(r'\D', '', split_lines[0]))
            else:
                footnote_list.append(split_lines[0])

print(footnote_list)