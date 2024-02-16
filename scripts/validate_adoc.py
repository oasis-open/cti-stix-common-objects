import argparse
import pathlib
import re
import sys

class Validator():
    def __init__(self, file_path):
        self._errors = []

        with open(file_path, "rt", encoding="utf-8") as input_file:
            self._content = input_file.read()

    def run_jobs(self) -> list:
        self.consistent_type_declaration(self._content)
        self.type_declarations_references(self._content)
        self.external_reference_variables(self._content)
        self.section_ids(self._content)

        return self._errors

    # Verify that all internal references can be resolved and that all anchors for references are used
    def consistent_type_declaration(self, content) -> None:
        find_references = re.compile("<<([a-zA-Z\-_]+),[a-zA-Z\-_]+")
        find_declarations = re.compile("\[\[([a-zA-Z\-_]+)\]\]")
        references = set(find_references.findall(content))
        declarations = set(find_declarations.findall(content))

        for item in references.difference(declarations):
            self._errors.append(f"{item} was referenced but not declared")

        for item in declarations.difference(references):
            self._errors.append(f"{item} was declared but not referenced")

    # Verify all types are references
    def type_declarations_references(self, content) -> None: 
        find_invalid_type = re.compile("\[stixtype\]#([^\{<][^#]+)")
        find_appendix = re.compile("== Appendix [A-Z]\. Revision History")
        
        line_number = 0
        for line in content.split("\n"):
            line_number += 1

            # Type definitions don't need to link to themselves and once we start the revision history we're done
            # since it can reference types that no longer exist meaning we can't have links
            if line.startswith("*Type Name:* "):
                continue
            elif find_appendix.match(line.strip()):
                break

            results = find_invalid_type.findall(line)

            for item in results:
                self._errors.append(f"Line {line_number}: {item} has no reference")

    # Verify all external type definitions use valid variables
    def external_reference_variables(self, content) -> None: 
        variable_declaration = re.compile(":([a-z_]+): https://")
        variable_use = re.compile("\].?\{([^\}]+)") # using a generic character after the type in case * is used instead of #
        
        variables = set(variable_declaration.findall(content))
        
        line_number = 0
        for line in content.split("\n"):
            line_number += 1

            results = variable_use.findall(line)

            for item in results:
                if item not in variables:
                    self._errors.append(f"Line {line_number}: {item} is an external reference that is not declared as a variable")

    # Verify section IDs increase and none are skipped
    def section_ids(self, content) -> None:
        last_id = None
        last_parts = []
        find_formatted_id = re.compile("^(=+ (?:\d+\.?)+)")


        line_number = 0
        for line in content.split("\n"):
            line_number += 1
            results = find_formatted_id.findall(line)


            for item in results:
                id = item.split(" ")[-1][:-1]
                parts = id.split(".")

                if (item.count("=") - 1) != item.count("."):
                    self._errors.append(f"Line {line_number}: {item} has the incorrect list level given its numbering")
                
                if last_id is None:
                    last_id = id
                    last_parts = parts
                    if id != "1":
                        self._errors.append(f"Line {line_number}: {item} should be 1 as the first item")
                    continue

                if item[-1] != ".":
                    self._errors.append(f"Line {line_number}: {item} has no . at the end")
                elif len(parts) == len(last_parts):
                    if int(last_parts[-1]) != int(parts[-1]) - 1:
                        self._errors.append(f"Line {line_number}: {item} should be {'.'.join(last_parts[:-1])}.{int(last_parts[-1]) + 1}")
                elif len(parts) > len(last_parts):
                    if not id.startswith(last_id):
                        self._errors.append(f"Line {line_number}: {item} should be numbered {last_id}.0 or {last_id}.1")
                    elif parts[-1] != "1":
                        self._errors.append(f"Line {line_number}: {item} should be numbered {last_id}.0 or {last_id}.1")
                else:
                    last_parts = last_parts[:len(parts)]
                    expected = f"{'.'.join(last_parts[:-1])}.{int(last_parts[-1]) + 1}".strip(".")
                    if id != expected:
                        self._errors.append(f"Line {line_number}: {item} should be numbered {expected}")

                last_id = id
                last_parts = parts



if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        prog="Validate STIX ASCII Doc",
        description="Validates an ASCII Doc input file meets STIX 2.1 format standards"
    )

    arguments.add_argument("-i", "--input", dest="input_path", action="store", required=True, help="The input file")
    args = arguments.parse_args()

    validator = Validator(args.input_path)
    errors = validator.run_jobs()

    if len(errors) > 0:
        print(f"Error Validating: {args.input_path}", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        exit(1)
    else:
        print(f"No errors found: {args.input_path}")

    exit(0)