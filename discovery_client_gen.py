#
# generate the rest client for the host based inventory api
#
# OpenAPI Schema Json:
#     https://console.redhat.com/api/inventory/v1/openapi.json
#
# Reference Implementation:
#     https://github.com/RedHatInsights/sources-api/blob/master/lib/tasks/client_generate.rake
#

from pathlib import Path
import os
import json
import requests
import sys

OPENAPI_SOURCE = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli"
OPENAPI_VERSION = "5.4.0"
CLIENT_LANG = "python"


def gen_client(base_dir, client_name, openapi_url):
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    print("------------------------------------------")
    print("Base directory: ", base_dir)

    source_url = f"{OPENAPI_SOURCE}/{OPENAPI_VERSION}/openapi-generator-cli-{OPENAPI_VERSION}.jar"

    jar_path = f"{base_dir}/openapi-generator-cli-{OPENAPI_VERSION}.jar"
    if not Path(jar_path).exists():
        resp = requests.get(source_url)
        if resp.status_code != 200:
            raise Exception("Failed to download " + source_url)
        with open(jar_path, "wb") as jf:
            jf.write(resp.content)
        print("Downloaded ", source_url)

    client_dir = f"{base_dir}/{client_name}"
    Path(client_dir).mkdir(parents=True, exist_ok=False)
    print("Client directory: ", client_dir)

    resp = requests.get(openapi_url)
    if resp.status_code != 200:
        raise Exception("Failed to download " + openapi_url)
    openapi_file = f"{client_dir}/openapi.json"
    with open(openapi_file, "w") as of:
        of.write(json.dumps(json.loads(resp.content), indent=4))
    print("Downloaded ", openapi_url)

    print("")
    print("Using OpenAPI Generator CLI Jar: ", jar_path)
    print("OpenAPI 3.0 Specification File:  ", openapi_file)

    print("")
    print(f"Generating API {CLIENT_LANG} Client")

    python_client_dir = f"{client_dir}/Client"
    Path(python_client_dir).mkdir(parents=True, exist_ok=False)
    cmd = f"java -jar {jar_path} generate -i {openapi_file} -g {CLIENT_LANG} -o {python_client_dir}"
    rc = os.system(cmd)
    print("java exit code: ", rc)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: discovery_client_gen.py target_directory")
    client_dir = sys.argv[1]
    gen_client(client_dir, "ingress", "https://console.redhat.com/api/ingress/v1/openapi.json")
    gen_client(client_dir, "rhsm", "https://console.redhat.com/api/rhsm/v2/openapi.json")
    gen_client(client_dir, "inventory", "https://console.redhat.com/api/inventory/v1/openapi.json")
