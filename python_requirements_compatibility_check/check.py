import requests
import requirements
import argparse
import csv

## Args parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "--requirements", help="check this requirements file", required=True
)
args = parser.parse_args()

if args.requirements:
    print("Check file " + args.requirements)

def csv_writer(name):
## CSV
    csv_path = name
    try:
        file = open(csv_path, "w", newline="")
        writer = csv.writer(file)
        writer.writerow(
            [
                "Package",
                "Version",
                "Python 3.8",
                "Python 3.9",
                "Python 3.10",
                "Django 3.0",
                "Django 3.2",
                "Django 4.0",
                "vulnerabilities",
            ]
        )
    except:
        print("error opening or writing to the CSV file!")
        raise
    return writer    

def check_classifiers(input,classifier):
    if classifier in input:
        return True
    else:
        return False

current_version = csv_writer('current_version.csv')
latest_version = csv_writer('latest_version.csv')

def get_pypi(package, version):
    r = requests.get("https://pypi.org/pypi/" + package + "/" + version + "/json")
    resulta = r.json()

    current_version.writerow(
        [
            package,
            str(version),
            check_classifiers(resulta['info']['classifiers'],"Programming Language :: Python :: 3.8"),
            check_classifiers(resulta['info']['classifiers'],"Programming Language :: Python :: 3.9"),
            check_classifiers(resulta['info']['classifiers'],"Programming Language :: Python :: 3.10"),
            check_classifiers(resulta['info']['classifiers'],"Framework :: Django :: 3.0"),
            check_classifiers(resulta['info']['classifiers'],"Framework :: Django :: 3.2"),
            check_classifiers(resulta['info']['classifiers'],"Framework :: Django :: 4.0"),
            resulta["vulnerabilities"],
        ]
    )

    r = requests.get("https://pypi.org/pypi/" + package + "/json")
    resultl = r.json()

    latest_version.writerow(
        [
            package,
            resultl['info']['version'],
            check_classifiers(resultl['info']['classifiers'],"Programming Language :: Python :: 3.8"),
            check_classifiers(resultl['info']['classifiers'],"Programming Language :: Python :: 3.9"),
            check_classifiers(resultl['info']['classifiers'],"Programming Language :: Python :: 3.10"),
            check_classifiers(resultl['info']['classifiers'],"Framework :: Django :: 3.0"),
            check_classifiers(resultl['info']['classifiers'],"Framework :: Django :: 3.2"),
            check_classifiers(resultl['info']['classifiers'],"Framework :: Django :: 4.0"),
            resultl["vulnerabilities"],
        ]
    )

with open(args.requirements, "r") as fd:
    for req in requirements.parse(fd):
        print(req.name, req.specs)
        if not req.line.startswith("git+") and "==" in req.specs[0]:
            get_pypi(req.name, req.specs[0][1])

