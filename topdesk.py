import datetime
import requests
from msal import ConfidentialClientApplication

# Microsoft Graph API Configuration
client_id = 'your-client-id'
tenant_id = 'your-tenant-id'
client_secret = 'your-client-secret'
graph_endpoint = 'https://graph.microsoft.com/v1.0/deviceManagement/managedDevices'

# TOPdesk Configuration
topdesk_url = 'https://yourtopdeskurl.topdesk.net/tas/api/assetmgmt/assets'
topdesk_username = 'your-topdesk-username'
topdesk_api_key = 'your-topdesk-api-key'

# Helper function to get a token for Microsoft Graph API
def get_graph_api_token():
    app = ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret
    )
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception("Failed to acquire token for Microsoft Graph API")

# Fetch new computers from Microsoft Graph API
def get_new_computers_from_graph_api():
    access_token = get_graph_api_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    one_day_ago_iso = one_day_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    print("Fetching managed devices from Microsoft Graph API...")
    response = requests.get(graph_endpoint, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching devices: {response.text}")

    devices = response.json().get('value', [])
    new_devices = []
    for device in devices:
        last_enrollment_date = device.get('enrolledDateTime')
        if last_enrollment_date and last_enrollment_date > one_day_ago_iso:
            new_devices.append({
                'name': device.get('deviceName', 'Unknown Device'),
                'id': device.get('id'),
                'serialNumber': device.get('serialNumber'),
				'model': device.get('model'),
				'manufacturer': device.get('manufacturer'),
				'userDisplayName': device.get('userDisplayName')
            })

    print(f"Found {len(new_devices)} new devices.")
    return new_devices


# Add computers to TOPdesk Asset Management
def add_computers_to_topdesk(computers):
    for computer in computers:
        asset_data = {
            "name": computer['name'],
			's-n': computer['serialNumber'],
			'model': computer['model'],
			'vendor': computer['manufacturer'],
			'clientname': computer['userDisplayName'],
            "type_id": "yourcardTypeid"   # Get the card type id and put it here
        }

        print(f"Adding computer {computer['name']} to TOPdesk...")
        response = requests.post(
            topdesk_url,
            auth=(topdesk_username, topdesk_api_key),  # Basic authentication
            headers={'Content-Type': 'application/json'},
            json=asset_data
        )

        if response.status_code == 201:
            print(f"Successfully added {computer['name']} to TOPdesk.")
        else:
            print(f"Failed to add {computer['name']} to TOPdesk. Error: {response.text}")

if __name__ == '__main__':
    try:
        # Step 1: Get new computers from Microsoft Graph API
        new_computers = get_new_computers_from_graph_api()

        # Step 2: Add them to TOPdesk
        if new_computers:
            add_computers_to_topdesk(new_computers)
        else:
            print("No new computers found.")
    except Exception as e:
        print(f"An error occurred: {e}")
