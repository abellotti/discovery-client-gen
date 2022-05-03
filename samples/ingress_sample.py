import ingress_client
from ingress_client.api import default_api
from pprint import pprint

configuration = ingress_client.Configuration(
    host="https://console.redhat.com/api/ingress/v1",
    username="<<USERNAME>>",
    password="<<PASSWORD>>",
)

basic_auth = configuration.get_basic_auth_token()
upload_host_file = open("./sample_host.info", "rb")

with ingress_client.ApiClient(configuration) as api_client:
    api_client.set_default_header("Authorization", basic_auth)
    api_instance = default_api.DefaultApi(api_client)
    try:
        api_response = api_instance.version_get()
        print("Version: ", api_response)
    except ingress_client.ApiException as e:
        print("Exception when calling DefaultApi->version_get: %s\n" % e)

    try:
        api_response = api_instance.upload_post(file=upload_host_file)
        pprint(api_response)
    except ingress_client.ApiException as e:
        print("Exception when calling DefaultApi->upload_post: %s\n" % e)
