import sys

from deplocator.parse import find_external_packages
from deplocator.locate import find_maven_dependency

def main():
    if len(sys.argv) < 3:
        print("Usage: deplocator [project folder] [project package prefix]")
    else:
        print("Packages:")
        pkgs = find_external_packages(sys.argv[1], sys.argv[2])
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
