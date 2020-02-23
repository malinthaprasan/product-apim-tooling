# Copyright (c) 2020, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
#
# WSO2 Inc. licenses this file to you under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import yaml
import base64
import csv
from utils import request_methods, util_methods


# variables
abs_path = ""
token_registration_endpoint = ""
token_endpoint = ""
publisher_api_endpoint = ""
store_application_endpoint = ""
delete_user_soap_endpoint = ""

gateway_protocol = ""
gateway_host = ""
gateway_servelet_port_https = ""
nio_pt_transport_port = ""


def loadConfig():
    """
    This function will load and set the configuration data
    :return: None
    """
    global abs_path, token_registration_endpoint, token_endpoint, publisher_api_endpoint, store_application_endpoint, delete_user_soap_endpoint
    global gateway_protocol, gateway_host, gateway_servelet_port_https, nio_pt_transport_port
    
    abs_path = os.path.abspath(os.path.dirname(__file__))

    with open(abs_path + '/../../../../config/apim.yaml', 'r') as config_file:
        apim_config = yaml.load(config_file, Loader=yaml.FullLoader)

    token_registration_endpoint = str(apim_config['apim_endpoints']['token_registration_endpoint'])
    token_endpoint = str(apim_config['apim_endpoints']['token_endpoint'])
    publisher_api_endpoint = str(apim_config['apim_endpoints']['publisher_api'])
    store_application_endpoint = str(apim_config['apim_endpoints']['store_application'])
    delete_user_soap_endpoint = str(apim_config['apim_endpoints']['delete_user'])
    
    gateway_protocol = str(apim_config['management_console']['protocol'])
    gateway_host = str(apim_config['management_console']['host'])
    gateway_servelet_port_https = str(apim_config['management_console']['servlet_transport_port_https'])
    nio_pt_transport_port = str(apim_config['api_manager']['nio_pt_transport_port'])


def removeApplications():
    """
    This function will remove all created applications from API Manager
    :return: None
    """

    remove_count = 0
    
    # get id and secret
    client_id, client_secret = request_methods.getIDSecret(gateway_protocol, gateway_host, gateway_servelet_port_https, token_registration_endpoint)
    
    if client_id == None or client_secret == None:
        util_methods.log("traffic-tool.log", "ERROR", "Fetching client id, client secret unsuccessful!. Aborting task...")
        print('[ERROR] Fetching client id, client secret unsuccessful!. Aborting task...')
        return
    util_methods.log("traffic-tool.log", "INFO", "Successfully fetched client id, client secret")

    concat_value = client_id + ":" + client_secret
    b64_encoded = base64.b64encode(concat_value.encode('utf-8')).decode('utf-8')

    # get access token
    access_token = request_methods.getAccessToken(gateway_protocol, gateway_host, nio_pt_transport_port, token_endpoint, b64_encoded, 'apim:subscribe apim:api_view')[0]

    if access_token == None:
        util_methods.log("traffic-tool.log", "ERROR", "Getting access token failed!. Aborting task...")
        print('[ERROR] Getting access token failed!. Aborting task...')
        return
    util_methods.log("traffic-tool.log", "INFO", "Successfully received access token")

    # iterate for each application
    with open(abs_path + '/../../data/runtime_data/app_ids.csv', 'r') as f:
        reader = csv.reader(f)

        for app_id in reader:
            deleted = request_methods.deleteAppAPI(gateway_protocol, gateway_host, gateway_servelet_port_https, store_application_endpoint, access_token,app_id[0])

            if not deleted:
                util_methods.log("traffic-tool.log", "ERROR", "Application removing Failed!. App id: {}. Retrying...".format(app_id[0]))
                deleted = request_methods.deleteAppAPI(gateway_protocol, gateway_host, gateway_servelet_port_https, store_application_endpoint, access_token,app_id[0])
                if not deleted:
                    util_methods.log("traffic-tool.log", "ERROR", "Application removing Failed!. App id: {}".format(app_id[0]))
                else:
                    util_methods.log("traffic-tool.log", "INFO", "Application removed successfully!. App id: {}".format(app_id[0]))
                    remove_count += 1
            else:
                util_methods.log("traffic-tool.log", "INFO", "Application removed successfully!. App id: {}".format(app_id[0]))
                remove_count += 1
            
        util_methods.log("traffic-tool.log", "INFO", "Application deletion process completed. Total {} applications removed".format(str(remove_count)))
        print("[INFO] Application deletion process completed. Total {} applications removed".format(str(remove_count)))


def removeAPIs():
    """
    This function will remove all created APIs from API Manager
    :return: None
    """

    remove_count = 0
    
    # get id and secret
    client_id, client_secret = request_methods.getIDSecret(gateway_protocol, gateway_host, gateway_servelet_port_https, token_registration_endpoint)
    
    if client_id == None or client_secret == None:
        util_methods.log("traffic-tool.log", "ERROR", "Fetching client id, client secret unsuccessful!. Aborting task...")
        print('[ERROR] Fetching client id, client secret unsuccessful!. Aborting task...')
        return
    util_methods.log("traffic-tool.log", "INFO", "Successfully fetched client id, client secret")

    concat_value = client_id + ":" + client_secret
    b64_encoded = base64.b64encode(concat_value.encode('utf-8')).decode('utf-8')

    # get access token
    access_token = request_methods.getAccessToken(gateway_protocol, gateway_host, nio_pt_transport_port, token_endpoint, b64_encoded, 'apim:api_create apim:api_view')[0]

    if access_token == None:
        util_methods.log("traffic-tool.log", "ERROR", "Getting access token failed!. Aborting task...")
        print('[ERROR] Getting access token failed!. Aborting task...')
        return
    util_methods.log("traffic-tool.log", "INFO", "Successfully received access token")

    # iterate for each API
    with open(abs_path + '/../../data/runtime_data/api_ids.csv', 'r') as f:
        reader = csv.reader(f)

        for api_id in reader:
            deleted = request_methods.deleteAppAPI(gateway_protocol, gateway_host, gateway_servelet_port_https, publisher_api_endpoint, access_token,api_id[0])

            if not deleted:
                util_methods.log("traffic-tool.log", "ERROR", "API removing Failed!. API id: {}. Retrying...".format(api_id[0]))
                deleted = request_methods.deleteAppAPI(gateway_protocol, gateway_host, gateway_servelet_port_https, publisher_api_endpoint, access_token,api_id[0])
                if not deleted:
                    util_methods.log("traffic-tool.log", "ERROR", "API removing Failed!. API id: {}".format(api_id[0]))
                else:
                    util_methods.log("traffic-tool.log", "INFO", "API removed successfully!. API id: {}".format(api_id[0]))
                    remove_count += 1
            else:
                util_methods.log("traffic-tool.log", "INFO", "API removed successfully!. API id: {}".format(api_id[0]))
                remove_count += 1
            
        util_methods.log("traffic-tool.log", "INFO", "API deletion process completed. Total {} APIs removed".format(str(remove_count)))
        print("[INFO] API deletion process completed. Total {} APIs removed".format(str(remove_count)))


def removeUsers():
    """
    This function will remove all created user accounts from carbon
    :return: None
    """

    remove_count = 0

    with open(abs_path + '/../../data/scenario/user_details.yaml', 'r') as user_file:
        user_data = yaml.load(user_file, Loader=yaml.FullLoader)

    for user in user_data['users']:
        removed = request_methods.removeUserSOAP(gateway_protocol, gateway_host, gateway_servelet_port_https, delete_user_soap_endpoint, user['username'])

        if not removed:
            util_methods.log("traffic-tool.log", "ERROR", "User deletion Failed!. username: {}. Retrying...".format(user['username']))
            removed = request_methods.removeUserSOAP(gateway_protocol, gateway_host, gateway_servelet_port_https, delete_user_soap_endpoint, user['username'])
            if not removed:
                util_methods.log("traffic-tool.log", "ERROR", "User deletion Failed!. username: {}".format(user['username']))
            else:
                util_methods.log("traffic-tool.log", "INFO", "User removed successfully!. username: {}".format(user['username']))
                remove_count += 1
        else:
            remove_count += 1
    
    util_methods.log("traffic-tool.log", "INFO", "User deletion process completed. Total {} user accounts removed".format(str(remove_count)))
    print("[INFO] User deletion process completed. Total {} user accounts removed".format(str(remove_count)))


if __name__ == "__main__":
    loadConfig()
    removeApplications()
    removeAPIs()
    removeUsers()
