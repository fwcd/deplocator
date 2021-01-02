import argparse

from deplocator.parse import find_external_packages
from deplocator.format import format_simple, format_maven, format_gradle
from deplocator.locate import find_maven_dependency

def main():
    parser = argparse.ArgumentParser(description="Parses Java source file and maps external imports to Maven dependencies.")
    parser.add_argument("project_path", help="Path to the folder of the project to be analyzed.")
    parser.add_argument("pkg_prefix", help="The package prefix of the project to be analyzed (imports from this package or subpackages not be considered external).")
    parser.add_argument("--maven", action="store_true", help="Outputs the dependencies in a Maven-formatted way.")
    parser.add_argument("--gradle", action="store_true", help="Outputs the dependencies in a Gradle-formatted way.")

    args = parser.parse_args()

    print("Packages:")
    pkgs = find_external_packages(args.project_path, args.pkg_prefix)
    print(pkgs)

    print("=============================")

    found = set()
    for pkg in pkgs:
        deps = find_maven_dependency(pkg)
        if len(deps) > 0:
            dep = deps[0].split(":")
            if len(dep) == 3:
                [group_id, artifact_id, version] = dep
                group_artifact = (group_id, artifact_id)
                if group_artifact not in found:
                    found.add(group_artifact)
                    if args.maven:
                        print(format_maven(group_id, artifact_id, version))
                    elif args.gradle:
                        print(format_gradle(group_id, artifact_id, version))
                    else:
                        print(pkg, "->", format_simple(group_id, artifact_id, version))

