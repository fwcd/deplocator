import sys
import os
import re
import urllib.request
import json

PACKAGE_REGEX = re.compile(r"import\s*(?:static)*\s*(.+)")

def extract_package(import_line):
    return PACKAGE_REGEX.match(import_line).group(1).rsplit(".", 1)[0]

def is_external_package(line):
    matched = PACKAGE_REGEX.match(line)
    if matched:
        pkg = matched.group(1)
        return not pkg.startswith("java") and not pkg.startswith("javax") and not pkg.startswith("com.antelmann")
    return False

def extract_imports(src_file_path):
    try:
        with open(src_file_path, "r") as src_file:
            return {extract_package(line) for line in src_file if is_external_package(line)}
    except UnicodeDecodeError:
        return set()

def find_external_packages(base_path):
    return {pkg for root, _, files in os.walk(base_path) for filename in files if filename.endswith(".java") for pkg in extract_imports(os.path.join(root, filename))}

def find_maven_dependency(package_name):
    with urllib.request.urlopen(r"http://search.maven.org/solrsearch/select?q=fc:%22" + package_name + r"%22&rows=20&wt=json") as raw_json:
        results = json.loads(raw_json.read())
        return [dep["id"] for dep in results["response"]["docs"]]

def main():
    if len(sys.argv) < 2:
        print("Pass a project folder as argument!")
    else:
        print("Packages:")
        pkgs = find_external_packages(sys.argv[1])
        print(pkgs)
        print("=============================")
        found = set()
        for pkg in pkgs:
            deps = find_maven_dependency(pkg)
            if len(deps) > 0:
                dep = deps[0]
                group_artifact = dep.rsplit(":", 1)[0]
                if group_artifact not in found:
                    found.add(group_artifact)
                    print(pkg, "->", dep)

if __name__ == "__main__":
    main()
