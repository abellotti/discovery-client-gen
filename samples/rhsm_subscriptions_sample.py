import os
import rhsm_subscriptions_client
from rhsm_subscriptions_client.api import default_api
from pprint import pprint

configuration = rhsm_subscriptions_client.Configuration(
    host="https://console.redhat.com/api/rhsm-subscriptions/v1",
    username=os.environ.get("API_USERNAME", None),
    password=os.environ.get("API_PASSWORD", None),
)

basic_auth = configuration.get_basic_auth_token()

with rhsm_subscriptions_client.ApiClient(configuration) as api_client:
    api_client.set_default_header("Authorization", basic_auth)
    api_instance = default_api.DefaultApi(api_client)
    try:
        api_response = api_instance.get_opt_in_config()
        pprint(api_response)
    except rhsm_subscriptions_client.ApiException as e:
        print("Exception when calling DefaultApi->get_opt_in_config: %s\n" % e)
