#!/bin/bash

# IFS set to a newline lets it actually get the proper paths
IFS='
'
for path in $(find */ -name "*.adoc"); do
    base_path=$(echo $path | sed 's/\.[^\.]\+$//')
    base_name=$(echo $base_path | sed 's/^[^\/]\+\//\.\.\/temp\//')

    asciidoctor  -v --failure-level INFO -a stylesheet=../asciidoc-shared/stix.css -D ../temp $path
    asciidoctor  -b docbook -v --failure-level INFO -a stylesheet=../asciidoc-shared/stix.css -D ../temp $path
    pandoc -r docbook -t docx -o $base_name.docx $base_name.xml
    # wkhtmltopdf --enable-local-file-access $base_name.html $base_name.pdf
done