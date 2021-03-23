import stix2
from stix2validator.v21.enums import INDUSTRY_SECTOR_OV, REGION_OV

import argparse
import csv
import json
import os
import pycountry

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
    parser = argparse.ArgumentParser(
        description='Create STIX common objects')
    parser.add_argument(
        'cve_dir', help='directory holding CVE entries')
    parser.add_argument(
        'stix_dir', help='output directory for generated stix files')
    parser.add_argument('-r', required=False, metavar='id_mapping_file', default=None,
                         help='The file containing the mapping of content to identifiers.')
    parser.add_argument('-m', required=False, metavar='marking_def_id', default=MARKING_ID,
                        help='optional marking definition id')
    parser.add_argument('-i', required=False, metavar='ident_id', default=IDENT_ID,
                        help='optional identity id')
    return parser.parse_args()


def existing_object(type, unique_info, id_map):
    return (type, unique_info) in id_map


def write_object(obj, stix_dir, unique_info, id_map):
    subdirectory_name = os.path.join(stix_dir, obj.type)
    if not os.path.exists(subdirectory_name):
        os.mkdir(subdirectory_name)
    file_name = os.path.join(stix_dir, obj.type, obj.id + ".json")
    id_map[(obj.type, unique_info)] = obj.id
    print("Adding " + obj.id)
    with open(file_name, "w") as output_file:
        output_file.write(str(stix2.Bundle(objects=[obj])))


def pretty_print_name(name, delimiter="-"):
    parts = name.split(delimiter)
    captialized_parts = [p.capitalize() for p in parts]
    return " ".join(captialized_parts)


def main():
    args = parse_args()
    ident_id = args.i
    marking_def_id = args.m
    mapping_file_name = args.r
    id_map = {}

    if args.r:
        with open(mapping_file_name, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                id_map[(row[0], row[1])] = row[2]

    # Create Marking Definition

    if not existing_object("marking-definition", _MARKING_DEFINITION_STATEMENT, id_map):
        marking_def = stix2.MarkingDefinition(definition_type="statement",
                                              id=marking_def_id,
                                              definition={
                                                    "statement": _MARKING_DEFINITION_STATEMENT
                                                })
        write_object(marking_def, args.stix_dir, _MARKING_DEFINITION_STATEMENT, id_map)

    # Create Identity for the repository

    if not existing_object("identity", "OASIS", id_map):
        ident = stix2.Identity(name="OASIS",
                               description="OASIS is a global community of experts who drive the creation and adoption of open standards promoting interoperability, innovation, and freedom of choice.",
                               identity_class="organization",
                               id=args.i)

        write_object(ident, args.stix_dir, "OASIS", id_map)

    # Location objects

    for c in pycountry.countries:
        if not existing_object("location", c.name, id_map):
            write_object(stix2.Location(name=c.name,
                                        country=c.alpha_2,
                                        created_by_ref=ident_id,
                                        object_marking_refs=[marking_def_id]),
                         args.stix_dir,
                         c.name,
                         id_map)

    for reg in REGION_OV:
        if not existing_object("location", reg, id_map):
            write_object(stix2.Location(name=pretty_print_name(reg),
                                        region=reg,
                                        created_by_ref=ident_id,
                                        object_marking_refs=[marking_def_id]),
                         args.stix_dir,
                         reg,
                         id_map)

    for cc in _CANADA_PROVINCE_CODES:
        if not existing_object("location", cc[1], id_map):
            write_object(stix2.Location(name=cc[0],
                                        country="CA",
                                        administrative_area=cc[1],
                                        created_by_ref=ident_id,
                                        object_marking_refs=[marking_def_id]),
                         args.stix_dir,
                         cc[1],
                         id_map)

    for cc in _US_STATES_CODES:
        if not existing_object("location", cc[1], id_map):
            write_object(stix2.Location(name=cc[0], country="US",
                                        administrative_area="US-" + cc[1],
                                        created_by_ref=ident_id,
                                        object_marking_refs=[marking_def_id]),
                         args.stix_dir,
                         cc[1],
                         id_map)

    for sec in INDUSTRY_SECTOR_OV:
        # not an individual
        if not existing_object("identity", sec, id_map):
            write_object(stix2.Identity(name=pretty_print_name(sec) + " sector as a target",
                                        sectors=[sec],
                                        created_by_ref=ident_id,
                                        identity_class="class",
                                        object_marking_refs=[marking_def_id]),
                         args.stix_dir,
                         sec,
                         id_map)

    # Vulnerability objects

    top_level_cve_directory = args.cve_dir
    for year_dir in os.listdir(top_level_cve_directory):
        year_dir_full_path = os.path.join(top_level_cve_directory, year_dir)
        if os.path.isdir(year_dir_full_path) and not year_dir_full_path.endswith(".git"):
            for sub_dir in os.listdir(year_dir_full_path):
                sub_dir_full_path = os.path.join(year_dir_full_path, sub_dir)
                for f in os.listdir(sub_dir_full_path):
                    file_full_path = os.path.join(sub_dir_full_path, f)
                    with open(file_full_path, 'r', encoding='utf-8') as cve_file:
                        cve_data = json.load(cve_file)
                        cve_meta_data = cve_data["CVE_data_meta"]
                        cve_id = cve_meta_data["ID"]
                        if not existing_object("vulnerability", cve_id, id_map):
                            if "STATE" in cve_meta_data and cve_meta_data["STATE"] == "PUBLIC":
                                write_object(stix2.Vulnerability(name=cve_id,
                                                                 description=cve_data["description"]["description_data"][0]["value"],
                                                                 external_references=[stix2.ExternalReference(source_name="cve",
                                                                                                              external_id=cve_id)],
                                                                 created_by_ref=ident_id,
                                                                 object_marking_refs=[marking_def_id]),
                                             args.stix_dir,
                                             cve_id,
                                             id_map)

    if args.r:
        with open(mapping_file_name, 'w', encoding='utf-8') as csv_file:
            id_map_writer = csv.writer(csv_file, delimiter=',')
            for (type, unique_info), id in id_map.items():
                id_map_writer.writerow([type, unique_info, id])


if __name__ == "__main__":
    main()