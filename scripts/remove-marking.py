import argparse
import datetime
import json
import os
import pathlib

def strftime_with_appropriate_fractional_seconds(timestamp, milliseconds_only):
    if isinstance(timestamp, (str, bytes)):
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    if milliseconds_only:
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate STIX common objects')
    parser.add_argument('-repo_dir',
                        help='directory with common objects content.'
                             'If not provided it will attempt `git status` on current directory')
    return parser.parse_args()


def main():
    args = parse_args()
    current_datetime = strftime_with_appropriate_fractional_seconds(datetime.datetime.now(), False)
    top_level_repo_directory = args.repo_dir
    for type_dir in os.listdir(top_level_repo_directory):
        dir_path_name = os.path.join(top_level_repo_directory, type_dir)
        for f in os.listdir(dir_path_name):
            json_filename = os.path.join(dir_path_name, f)
            json_filename_path = pathlib.Path(json_filename)
            stix_file_r = json_filename_path.open('r', encoding='utf-8')
            try:
                bundle = json.load(stix_file_r)
            except Exception as exc:
                print("Bad: " + json_filename)
                raise exc
            obj = bundle["objects"][0]
            if "object_marking_refs" in obj:
                obj.pop("object_marking_refs")
                obj["modified"] = current_datetime
                stix_file_r.close()
                with json_filename_path.open('w', encoding='utf-8') as stix_file_w:
                    json.dump(
                        bundle,
                        stix_file_w,
                        ensure_ascii=False,
                        indent=4,
                        separators=(',', ': '),
                        sort_keys=True
                    )

            else:
                print(json_filename)



if __name__ == "__main__":
    main()