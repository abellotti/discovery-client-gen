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
import json
import os
import yaml
import requests
import sys

OPENAPI_SOURCE = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli"
OPENAPI_VERSION = "5.4.0"
CLIENT_LANG = "python"


def gen_client(client_dir, openapi_url):
    Path(client_dir).mkdir(parents=True, exist_ok=False)
    print("------------------------------------------")
    print("Client directory: ", client_dir)

    source_url = f"{OPENAPI_SOURCE}/{OPENAPI_VERSION}/openapi-generator-cli-{OPENAPI_VERSION}.jar"

    jar_path = f"{client_dir}/openapi-generator-cli-{OPENAPI_VERSION}.jar"
    resp = requests.get(source_url)
    if resp.status_code != 200:
        raise Exception("Failed to download " + source_url)
    with open(jar_path, "wb") as jf:
        jf.write(resp.content)
    print("Downloaded ", source_url)

    resp = requests.get(openapi_url)
    if resp.status_code != 200:
        raise Exception("Failed to download " + openapi_url)
    openapi_file = f"{client_dir}/openapi.json"
    with open(openapi_file, "wb") as of:
        of.write(resp.content)
    print("Downloaded ", openapi_url)

    with open(openapi_file) as jf:
        openapi_json = json.load(jf)

    openapi_yaml_file = f"{client_dir}/openapi.yaml"
    with open(openapi_yaml_file, "w") as yf:
        yaml.safe_dump(openapi_json, yf, default_flow_style=False)

    print("")
    print("Using OpenAPI Generator CLI Jar: ", jar_path)
    print("OpenAPI 3.0 Specification File:  ", openapi_file)
    print("OpenAPI 3.0 Yaml File:           ", openapi_yaml_file)

    print("")
    print(f"Generating API {CLIENT_LANG} Client")

    python_client_dir = f"{client_dir}/Client"
    Path(python_client_dir).mkdir(parents=True, exist_ok=False)
    # cmd = f"java -jar {jar_path} generate -i {openapi_yaml_file} -c {generator_config} -g {CLIENT_LANG} -o {python_client_dir}"
    cmd = f"java -jar {jar_path} generate -i {openapi_yaml_file} -g {CLIENT_LANG} -o {python_client_dir}"
    rc = os.system(cmd)
    print("java exit code: ", rc)
  

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: hbi_client_gen.py target_directory")
    client_dirs = sys.argv[1]
    gen_client(f"{client_dirs}/ingress", "https://console.redhat.com/api/ingress/v1/openapi.json")
    gen_client(f"{client_dirs}/rhsm", "https://console.redhat.com/api/rhsm/v2/openapi.json")
    gen_client(f"{client_dirs}/inventory", "https://console.redhat.com/api/inventory/v1/openapi.json")
