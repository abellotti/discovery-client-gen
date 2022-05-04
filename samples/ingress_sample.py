import ingress_client
import os
from ingress_client.api import default_api
from pathlib import Path
from pprint import pprint

configuration = ingress_client.Configuration(
    host="https://console.redhat.com/api/ingress/v1",
    username=os.environ.get("API_USERNAME", None),
    password=os.environ.get("API_PASSWORD", None),
)

basic_auth = configuration.get_basic_auth_token()

insights_client_content_type = "application/vnd.redhat.advisor.example+tgz"
insights_client_archive_file = "./example.tar.gz"

with ingress_client.ApiClient(configuration) as api_client:
    api_client.set_default_header("Authorization", basic_auth)
    api_instance = default_api.DefaultApi(api_client)
    try:
        api_response = api_instance.version_get()
        print("Version: ", api_response)
    except ingress_client.ApiException as e:
        print("Exception when calling DefaultApi->version_get: %s\n" % e)
    try:
        if Path(insights_client_archive_file).exists():
            print("Uploading ", insights_client_archive_file, " to ingress/upload ...")
            upload_host_file = open(insights_client_archive_file, "rb")
            # The metadata is not supported as per the openapi json so we're not
            # effectively setting the content-type on this multipart/form-data.
            #
            # api_response = api_instance.upload_post(
            #                    file=upload_host_file,
            #                    metadata={"type": insights_client_content_type}
            #                )
            #
            #
            # working curl would be:
            # curl --verbose --user $API_USER
            #  -F "file=@example.tar.gz;type=application/vnd.redhat.advisor.example+tgz"
            #  https://console.redhat.com/api/ingress/v1/upload
            api_response = api_instance.upload_post(file=upload_host_file)
            pprint(api_response)
        else:
            print("Missing insights client archive file ", insights_client_archive_file)
    except ingress_client.ApiException as e:
        print("Exception when calling DefaultApi->upload_post: %s\n" % e)
