import json
import urllib.request
import os

def find_maven_dependency(package_name):
    with urllib.request.urlopen(r"http://search.maven.org/solrsearch/select?q=fc:%22" + package_name + r"%22&rows=20&wt=json") as raw_json:
        results = json.loads(raw_json.read())
        return [dep["id"] for dep in results["response"]["docs"]]


