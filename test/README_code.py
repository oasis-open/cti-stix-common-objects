from stix2 import FileSystemSource, Filter

def get_location_for_country(store, country_name):
    filt = [
        Filter('type', '=', 'location'),
        Filter('name', '=', country_name),
    ]
    return store.query(filt)


def get_new_vulnerabilties(store, added_after_date):
    filt = [
        Filter('type', '=', 'vulnerability'),
        Filter("created", ">=", added_after_date)
    ]
    return store.query(filt)


def main():
    fs = FileSystemSource("/Users/rpiazza/git/stix/common-object-repository-prototype")
    print("Initialized File System Source")
    filt = Filter('type', '=', 'vulnerability')
    vulnerabilities = fs.query([filt])
    print("number of vulnerabilities: " + str(len(vulnerabilities)))

    france = get_location_for_country(fs, "France")
    print(str(france))

    vulnerabilities = get_new_vulnerabilties(fs, "2021-02-28T00:00:00.000Z")
    print("number of new vulnerabilities: " + str(len(vulnerabilities)))


if __name__ == "__main__":
    main()