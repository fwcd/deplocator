import argparse

from deplocator.parse import find_external_packages
from deplocator.locate import find_maven_dependency

def main():
    parser = argparse.ArgumentParser(description="Parses Java source file and maps external imports to Maven dependencies.")
    parser.add_argument("project_path", help="Path to the folder of the project to be analyzed.")
    parser.add_argument("pkg_prefix", help="The package prefix of the project to be analyzed (imports from this package or subpackages not be considered external).")

    args = parser.parse_args()
    project_path = args.project_path
    pkg_prefix = args.pkg_prefix

    print("Packages:")
    pkgs = find_external_packages(project_path, pkg_prefix)
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
