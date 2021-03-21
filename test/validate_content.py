import argparse
import os
import shlex

# external
from stix2validator import ValidationError, codes, output, validate_string
from stix2validator.scripts import stix2_validator
from stix2validator.validator import FileValidationResults

import stix2

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Validate STIX common objects')
    parser.add_argument(
        'repo_dir', help='directory with common objects content')
    parser.add_argument('-v', required=False, metavar='validator_options', default=None,
                        help='validator arguments')
    return parser.parse_args()

def validate_stix2_string(json_string, validator_options, file_path=None):
    results = validate_string(json_string, validator_options)
    fvr = FileValidationResults(results.is_valid, file_path, results)
    return fvr

def get_validator_options(validator_args):
    """Return a stix2validator.validators.ValidationOptions instance."""
    return stix2_validator.parse_args(shlex.split(validator_args))

def main():
    args = parse_args()
    return_value = 0
    top_level_repo_directory = args.repo_dir
    for type_dir in os.listdir(top_level_repo_directory):
        type_dir_full_path = os.path.join(top_level_repo_directory, type_dir)
        if os.path.isdir(type_dir_full_path):
            for f in os.listdir(type_dir_full_path):
                if f.endswith(".json"):
                    try:
                        file_full_path = os.path.join(type_dir_full_path, f)
                        with open(file_full_path, 'r', encoding='utf-8') as stix_file:
                                json_string = stix_file.read()
                                validation_results = validate_stix2_string(json_string, get_validator_options(args.v), file_full_path)
                                if not validation_results.is_valid:
                                    output.print_results([validation_results])
                                    return_value = -1
                    except ValidationError as ex:
                        output.error("Validation error occurred: '{}'".format(ex))
                        output.error("Error Code: {}".format(codes.EXIT_VALIDATION_ERROR))
                        return_value = -1
                    except Exception:
                        print("Failed with uncaught exception: " + file_full_path)
                        return_value = -1
    return return_value

if __name__ == "__main__":
    main()