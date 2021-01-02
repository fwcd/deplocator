import json
import urllib.request
import os

def find_possible_maven_dependencies(package_name):
    with urllib.request.urlopen(r"https://search.maven.org/solrsearch/select?q=fc:%22" + package_name + r"%22&rows=20&wt=json") as raw_json:
        results = json.loads(raw_json.read())
        return [dep["id"].split(":") for dep in results["response"]["docs"]]

def matching_prefix_length(xs, ys):
    if xs and ys and xs[0] == ys[0]:
        return 1 + matching_prefix_length(xs[1:], ys[1:])
    return 0

def match_score(package_name, dep):
    # The score relies on lexicographic ordering
    # Longer matching prefixes between package name and group id
    # and higher versions are better.

    if len(dep) == 3:
        [group_id, artifact_id, version] = dep
        return [1, matching_prefix_length(package_name, group_id)] + version.split(".")
    return [0]

def find_maven_dependency(package_name):
    best_dep = None
    best_score = None

    for dep in find_possible_maven_dependencies(package_name):
        score = match_score(package_name, dep)
        if not best_score or score > best_score:
            best_score = score
            best_dep = dep

    return best_dep

