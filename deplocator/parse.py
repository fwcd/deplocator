import os
import re

IMPORT_REGEX = re.compile(r"import\s*(?:static)*\s*(.+)")

def extract_package(import_line):
    return IMPORT_REGEX.match(import_line).group(1).rsplit(".", 1)[0]

def is_external_package(line, project_pkg_prefix):
    matched = IMPORT_REGEX.match(line)
    if matched:
        pkg = matched.group(1)
        return not pkg.startswith("java") and not pkg.startswith("javax") and not pkg.startswith(project_pkg_prefix)
    return False

def extract_imports(src_file_path, project_pkg_prefix):
    try:
        with open(src_file_path, "r") as src_file:
            return {extract_package(line) for line in src_file if is_external_package(line, project_pkg_prefix)}
    except UnicodeDecodeError:
        return set()

def find_external_packages(base_path, project_pkg_prefix):
    return {pkg for root, _, files in os.walk(base_path) for filename in files if filename.endswith(".java") for pkg in extract_imports(os.path.join(root, filename), project_pkg_prefix)}

