import rhsm_client
from rhsm_client.api import manifest_api
# from rhsm_client.model.inline_response2002 import InLineResponse2002

# from rhsm_client.model.inline_response401 import InLineResponse401
from pprint import pprint
configuration = rhsm_client.Configuration(
    host="https://console.redhat.com/api/rhsm/v2",
    username="<<USERNAME>>",
    password="<<PASSWORD>>"
)

with rhsm_client.ApiClient(
        configuration,
        header_name="Authorization",
        header_value=configuration.get_basic_auth_token()) as api_client:
    api_instance = manifest_api.ManifestApi(api_client)
    try:
        api_response = api_instance.list_manifests(limit=10, offset=1)
        pprint(api_response)
        for manifest in api_response["body"]:
            print("name=%s, uuid=%s" % (manifest["name"], manifest["uuid"]))
    except rhsm_client.ApiException as e:
        print("Exception when calling ManifestApi->list_manifests: %s\n" % e)
