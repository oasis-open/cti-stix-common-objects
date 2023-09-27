#!/bin/bash

# IFS set to a newline lets it actually get the proper paths
IFS='
'
for path in $(find */ -maxdepth 1 -name "*.adoc"); do
    base_path=$(echo $path | sed 's/\.[^\.]\+$//')
    base_name=$(echo $base_path | sed 's/^[^\/]\+\//\.\.\/temp\//')

    asciidoctor  -v --failure-level INFO -a stylesheet=../asciidoc-shared/stix.css -D ../temp $path
    asciidoctor  -b docbook -v --failure-level INFO -a stylesheet=../asciidoc-shared/stix.css -D ../temp $path
    pandoc -r docbook -t docx -o $base_name.docx $base_name.xml
    # wkhtmltopdf --enable-local-file-access $base_name.html $base_name.pdf
done

mkdir ../_site 

echo "<html><head><title>Common Extensions</title></head><body><ul>" > ../_site/index.html
for path in $(find ../temp -name "*.html"); do
    friendly_name=$(echo $path | sed 's/^.\{8\}//' | sed 's/.\{5\}$//')
    filename=$(echo $path | sed s'/^.\{8\}//' | sed 's/ /_/g')
    echo "Added: "$friendly_name
    echo '<li><a href="' $filename '">' ${friendly_name} "</a></li>" >> ../_site/index.html
    cp "$path" "../_site/$filename"
done
echo "</ul></body></html>" >> ../_site/index.html