import re
import argparse

# CSS should be pulled from the original file so we don't need to redo it
adoc_header = """[width="100%",cols="1,1,1"]
|===
^|*Source*
^|*Type* 
^|*Target* 

"""

arguments = argparse.ArgumentParser(
    prog="Relationship Summary Builder",
    description="Creates a summary of relationships in an adoc file by reading section marked with relationships:start and relationships:end comments"
)

arguments.add_argument("-i", "--input", dest="input_path", action="store", required=True, help="The input file")
arguments.add_argument("-o", "--output", dest="output_path", action="store", required=True, help="The output file")
args = arguments.parse_args()

# find tables
parse_tables = re.compile('// relationships:start.+?// relationships:end', re.DOTALL)

# read each table and just extract the content
parse_rows = re.compile('(\|(\[stixtype\]#[^#]+#)\s*\|(\[stixrelationship\]#[^#]+#)\s*\|(\[stixtype\]#[^#]+#))')
results = []
mapping = {}

with open(args.input_path, 'rt') as input_file:
    content = input_file.read()
    
    for table in parse_tables.findall(content):
        for row in parse_rows.findall(table):
            # Using a dictionary with lists to convert to a comma separated values for targets so it matches with the spec
            key = f"|{row[1]}\n|{row[2]}\n|"
            if key not in mapping:
                mapping[key] = [row[3]]
            else:
                if row[3] not in mapping[key]:
                    mapping[key].append(row[3])
                
results = list(mapping.keys())
results.sort()
with open(args.output_path, "wt") as output_file:
    output_file.write(adoc_header)
    for key in results:
        output_file.write(key)
        mapping[key].sort()
        output_file.write(", ".join(mapping[key]))
        output_file.write("\n\n")
    
    output_file.write("|===")