def format_simple(group_id, artifact_id, version):
    return f"{group_id}:{artifact_id}:{version}"

def format_maven(group_id, artifact_id, version):
    return "\n".join([
        "<dependency>",
        f"  <groupId>{group_id}</groupId>",
        f"  <artifactId>{artifact_id}</artifactId>",
        f"  <version>{version}</version>",
        "</dependency>"
    ])

def format_gradle(group_id, artifact_id, version):
    return f"implementation '{group_id}:{artifact_id}:{version}'"
