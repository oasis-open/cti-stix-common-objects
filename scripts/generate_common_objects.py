import argparse
import csv
import io
import json
import pathlib
import zipfile

# external
import pycountry
import requests
from stix2 import v21
from stix2validator.v21.enums import INDUSTRY_SECTOR_OV, REGION_OV


_MARKING_DEFINITION_STATEMENT = "This content is subject to \
open source license terms expressed in the BSD-3-Clause License. \
For more information, please see https://github.com/oasis-open/cti-stix-common-objects"


_CANADA_PROVINCE_CODES = [
    ("Alberta", "AB"),
    ("British Columbia", "BC"),
    ("Manitoba", "MB"),
    ("New Brunswick", "NB"),
    ("Newfoundland and Labrador", "NL"),
    ("Northwest Territories", "NT"),
    ("Nova Scotia", "NS"),
    ("Nunavut", "NU"),
    ("Ontario", "ON"),
    ("Prince Edward Island", "PE"),
    ("Quebec", "QC"),
    ("Saskatchewan", "SK"),
    ("Yukon", "YT")
]


_US_STATES_CODES = [
    ("Alabama", "AL"),
    ("Alaska", "AK"),
    ("Arizona", "AZ"),
    ("Arkansas", "AR"),
    ("California", "CA"),
    ("Colorado", "CO"),
    ("Connecticut", "CT"),
    ("Delaware", "DE"),
    ("Florida", "FL"),
    ("Georgia", "GA"),
    ("Hawaii", "HI"),
    ("Idaho", "ID"),
    ("Illinois", "IL"),
    ("Indiana", "IN"),
    ("Iowa", "IA"),
    ("Kansas", "KS"),
    ("Kentucky", "KY"),
    ("Louisiana", "LA"),
    ("Maine", "ME"),
    ("Maryland", "MD"),
    ("Massachusetts", "MA"),
    ("Michigan", "MI"),
    ("Minnesota", "MN"),
    ("Mississippi", "MS"),
    ("Missouri", "MO"),
    ("Montana", "MT"),
    ("Nebraska", "NE"),
    ("Nevada", "NV"),
    ("New Hampshire", "NH"),
    ("New Jersey", "NJ"),
    ("New Mexico", "NM"),
    ("New York", "NY"),
    ("North Carolina", "NC"),
    ("North Dakota", "ND"),
    ("Ohio", "OH"),
    ("Oklahoma", "OK"),
    ("Oregon", "OR"),
    ("Pennsylvania", "PA"),
    ("Rhode Island", "RI"),
    ("South Carolina", "SC"),
    ("South Dakota", "SD"),
    ("Tennessee", "TN"),
    ("Texas", "TX"),
    ("Utah", "UT"),
    ("Vermont", "VT"),
    ("Virginia", "VA"),
    ("Washington", "WA"),
    ("West Virginia", "WV"),
    ("Wisconsin", "WI"),
    ("Wyoming", "WY"),
    ("District of Columbia", "DC"),
    ("American Samoa", "AS"),
    ("Guam", "GU"),
    ("Northern Mariana Islands", "MP"),
    ("Puerto Rico", "PR"),
    ("US Virgin Islands", "VI"),
    ("Marshall Islands", "MH"),
    ("Armed Forces Africa", "AE"),
    ("Armed Forces Americas", "AA"),
    ("Armed Forces Canada", "AE"),
    ("Armed Forces Europe", "AE"),
    ("Armed Forces Middle East", "AE"),
    ("Armed Forces Pacific", "AP")
]

IDENT_ID = "identity--8ce3f695-d5a4-4dc8-9e93-a65af453a31a"
MARKING_ID = "marking-definition--62fd3f9b-15f3-4ebc-802c-91fce9536bcf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create STIX common objects')
    parser.add_argument('stix_dir',
                        help='output directory for generated stix files')
    parser.add_argument('-r', required=False, metavar='id_mapping_file', default=None,
                        help='The file containing the mapping of content to identifiers.')
    parser.add_argument('-m', required=False, metavar='marking_def_id', default=MARKING_ID,
                        help='optional marking definition id')
    parser.add_argument('-i', required=False, metavar='ident_id', default=IDENT_ID,
                        help='optional identity id')
    return parser.parse_args()


def existing_object(stix_type, unique_info, id_map) -> bool:
    return (stix_type, unique_info) in id_map


def write_object(obj, stix_dir, unique_info, id_map) -> None:
    subdirectory_name = stix_dir / obj.type
    if not subdirectory_name.exists():
        subdirectory_name.mkdir()
    file_name = subdirectory_name / (obj.id + ".json")
    id_map[(obj.type, unique_info)] = obj.id
    print(f"Adding {obj.id}")
    with file_name.open("w", encoding="utf-8") as output_file:
        bundle_str = v21.Bundle(objects=[obj]).serialize(pretty=True, encoding="utf-8", ensure_ascii=False)
        output_file.write(bundle_str)


def pretty_print_name(name, delimiter="-") -> str:
    parts = name.split(delimiter)
    capitalized_parts = [p.capitalize() for p in parts]
    return " ".join(capitalized_parts)


def main():
    args = parse_args()
    ident_id = args.i
    marking_def_id = args.m
    mapping_file = pathlib.Path(args.r).resolve() if args.r else ""
    output_dir = pathlib.Path(args.stix_dir).resolve()
    id_map = {}

    if args.r:
        with mapping_file.open('r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                id_map[(row[0], row[1])] = row[2]

    # Create Marking Definition

    if not existing_object("marking-definition", _MARKING_DEFINITION_STATEMENT, id_map):
        marking_definition = v21.MarkingDefinition(
            definition_type="statement",
            created_by_ref=ident_id,
            id=marking_def_id,
            definition={"statement": _MARKING_DEFINITION_STATEMENT},
        )
        write_object(marking_definition, output_dir, _MARKING_DEFINITION_STATEMENT, id_map)

    # Create Identity for the repository

    if not existing_object("identity", "OASIS", id_map):
        identity = v21.Identity(
            name="OASIS",
            description="OASIS is a global community of experts who drive the creation and adoption of open standards promoting interoperability, innovation, and freedom of choice.",
            identity_class="organization",
            id=ident_id,
            object_marking_refs=[marking_def_id],
        )
        write_object(identity, output_dir, "OASIS", id_map)

    # Location objects

    for c in pycountry.countries:
        if not existing_object("location", c.name, id_map):
            location = v21.Location(
                name=c.name,
                country=c.alpha_2,
                created_by_ref=ident_id,
                object_marking_refs=[marking_def_id],
            )
            write_object(location, output_dir, c.name, id_map)

    for reg in REGION_OV:
        if not existing_object("location", reg, id_map):
            location = v21.Location(
                name=pretty_print_name(reg),
                region=reg,
                created_by_ref=ident_id,
                object_marking_refs=[marking_def_id],
            )
            write_object(location, output_dir, reg, id_map)

    for cc in _CANADA_PROVINCE_CODES:
        if not existing_object("location", cc[1], id_map):
            location = v21.Location(
                name=cc[0],
                country="CA",
                administrative_area=cc[1],
                created_by_ref=ident_id,
                object_marking_refs=[marking_def_id],
            )
            write_object(location, output_dir, cc[1], id_map)

    for cc in _US_STATES_CODES:
        if not existing_object("location", cc[1], id_map):
            location = v21.Location(
                name=cc[0],
                country="US",
                administrative_area="US-" + cc[1],
                created_by_ref=ident_id,
                object_marking_refs=[marking_def_id],
            )
            write_object(location, output_dir, cc[1], id_map)

    for sec in INDUSTRY_SECTOR_OV:
        # not an individual
        if not existing_object("identity", sec, id_map):
            identity = v21.Identity(
                name=pretty_print_name(sec) + " sector as a target",
                sectors=[sec],
                created_by_ref=ident_id,
                identity_class="class",
                object_marking_refs=[marking_def_id],
            )
            write_object(identity, output_dir, sec, id_map)

    # Vulnerability objects

    response = requests.get(r"https://github.com/CVEProject/cvelist/archive/refs/heads/master.zip", verify=True)

    with zipfile.ZipFile(io.StringIO(response.text), "r") as cve_zip:
        cve_zip.extractall("cvelist")

    top_level_cve_directory = pathlib.Path("./cvelist/cvelist-master").resolve()
    for cve_entry in top_level_cve_directory.rglob("*.json"):
        with cve_entry.open('r', encoding='utf-8') as cve_file:
            cve_data = json.load(cve_file)
        cve_meta_data = cve_data["CVE_data_meta"]
        cve_id = cve_meta_data["ID"]
        if (not existing_object("vulnerability", cve_id, id_map) and
                cve_meta_data.get("STATE", None) == "PUBLIC"):
            cve_description = cve_data["description"]["description_data"][0]["value"]
            vulnerability = v21.Vulnerability(
                name=cve_id,
                description=cve_description,
                external_references=[v21.ExternalReference(source_name="cve", external_id=cve_id)],
                created_by_ref=ident_id,
                object_marking_refs=[marking_def_id],
            )
            write_object(vulnerability, output_dir, cve_id, id_map)

    top_level_cve_directory.rmdir()  # removes directory

    if args.r:
        with mapping_file.open('w', encoding='utf-8') as csv_file:
            id_map_writer = csv.writer(csv_file, delimiter=',')
            for (stix_type, unique_info), stix_id in id_map.items():
                id_map_writer.writerow([stix_type, unique_info, stix_id])


if __name__ == "__main__":
    main()
