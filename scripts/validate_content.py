import argparse
import pathlib
import re
import shlex
import subprocess

# external
from stix2validator import ValidationError, codes, output, validate_string
from stix2validator.scripts import stix2_validator
from stix2validator.validator import FileValidationResults, ValidationOptions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate STIX common objects')
    parser.add_argument('-repo_dir',
                        help='directory with common objects content.'
                             'If not provided it will attempt `git status` on current directory')
    parser.add_argument('-v', required=False, metavar='validator_options', default=None,
                        help='validator arguments')
    return parser.parse_args()


def validate_stix2_string(json_string, validator_options, file_path=None) -> FileValidationResults:
    results = validate_string(json_string, validator_options)
    fvr = FileValidationResults(results.is_valid, file_path, results)
    return fvr


def get_validator_options(validator_args) -> ValidationOptions:
    """Return a stix2validator.validators.ValidationOptions instance."""
    return stix2_validator.parse_args(shlex.split(validator_args))


def main():
    args = parse_args()
    return_value = 0
    top_level_repo_directory = pathlib.Path(args.repo_dir).resolve().rglob("*.json") if args.repo_dir else ""
    modified_files = []
    new_files = []

    if not args.repo_dir:
        sub_proc = subprocess.run(["git", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if sub_proc.returncode != 0:
            print("Error executing Git...")
            print(sub_proc.stderr)
            return -1

        str_stdout = sub_proc.stdout.decode("utf-8")
        modified_files = re.findall(r'modified:\s{3}(.*\.json)', str_stdout, re.MULTILINE)
        new_files = re.findall(r'new file:\s{3}(.*\.json)', str_stdout, re.MULTILINE)

    search_criteria = top_level_repo_directory or (modified_files + new_files)

    for json_filename in search_criteria:
        if not isinstance(json_filename, pathlib.Path):
            json_filename_path = pathlib.Path(json_filename).resolve()
        else:
            json_filename_path = json_filename
        json_filename_str = str(json_filename_path)
        try:
            with json_filename_path.open('r', encoding='utf-8') as stix_file:
                json_string = stix_file.read()
                validation_results = validate_stix2_string(json_string, get_validator_options(args.v), json_filename_str)
                if not validation_results.is_valid:
                    output.print_results([validation_results])
                    return_value = -1
                else:
                    print(f"{json_filename_str} is valid")
        except ValidationError as ex:
            output.error("Validation error occurred: '{}'".format(ex))
            output.error("Error Code: {}".format(codes.EXIT_VALIDATION_ERROR))
            return_value = -1
        except Exception:
            print(f"Failed with uncaught exception: {json_filename_str}")
            return_value = -1
    if return_value != -1:
        print("All content is valid")
    return return_value


if __name__ == "__main__":
    main()
