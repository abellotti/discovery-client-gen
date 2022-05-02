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
import shutil
import sys

OPENAPI_SOURCE = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli"
OPENAPI_VERSION = "5.4.0"
CLIENT_LANG = "python"


def gen_client(
    base_dir, client_name, package_name, openapi_url=None, openapi_schema_dir=None
):
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    print("--------------------------------------------------------------")
    print("Base directory:                  ", base_dir)

    source_url = (
        f"{OPENAPI_SOURCE}/{OPENAPI_VERSION}/"
        f"openapi-generator-cli-{OPENAPI_VERSION}.jar"
    )

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
    print("Client directory:                ", client_dir)

    openapi_file = f"{client_dir}/openapi.json"
    if openapi_schema_dir:
        schema_override = f"{openapi_schema_dir}/{client_name}_openapi.json"
        if Path(client_dir).exists():
            shutil.copy(schema_override, openapi_file)
            print("Using ", schema_override)

    if not Path(openapi_file).exists():
        if not openapi_url:
            raise Exception("Must specify a url to download " + openapi_file)

        resp = requests.get(openapi_url)
        if resp.status_code != 200:
            raise Exception("Failed to download " + openapi_url)
        with open(openapi_file, "w") as of:
            of.write(json.dumps(json.loads(resp.content), indent=4))
        print("Downloaded ", openapi_url)

    print("")
    print("Using OpenAPI Generator CLI Jar: ", jar_path)
    print("OpenAPI 3.0 Specification File:  ", openapi_file)
    print("OpenAPI Client Package Name:     ", package_name)

    print("")
    print(f"Generating API {CLIENT_LANG} Client")

    python_client_dir = f"{client_dir}/openapi_client"
    Path(python_client_dir).mkdir(parents=True, exist_ok=False)
    cmd = (
        f"java -jar {jar_path} generate -i {openapi_file} -g {CLIENT_LANG}"
        f" --package-name {package_name} -o {python_client_dir}"
    )
    rc = os.system(cmd)
    if rc != 0:
        raise Exception("OpenAPI Client Generate exited with ", rc)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: discovery_client_gen.py target_directory")
    client_dir = sys.argv[1]
    script_dir = os.path.dirname(__file__)
    openapi_schema_dir = f"{script_dir}/openapi_schemas"
    # Ingress for uploading & registering new device
    gen_client(
        base_dir=client_dir,
        client_name="ingress",
        package_name="ingress_client",
        openapi_url="https://console.redhat.com/api/ingress/v1/openapi.json",
    )
    # Swatch, RHSM Subscriptions, pulling model analog, etc.
    gen_client(
        base_dir=client_dir,
        client_name="rhsm_subscriptions",
        package_name="rhsm_subscriptions_client",
        openapi_url=(
            "https://console.redhat.com/api/rhsm-subscriptions/v1/openapi.json"
        ),
    )
    # HBI, Host Based Inventory
    # Commenting out for now, even though the openapiseveral openapi validator
    # passes fine on the openapi schema, the generator fails with a null pointer
    # exception. Seems to be related to nested object and deepObject serialization
    # with the Python client.
    #
    # gen_client(
    #    base_dir=client_dir,
    #    client_name="inventory",
    #    package_name="inventory_client",
    #    openapi_schema_dir=openapi_schema_dir,
    #    openapi_url="https://console.redhat.com/api/inventory/v1/openapi.json",
    # )
