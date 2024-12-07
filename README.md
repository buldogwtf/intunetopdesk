# intunetopdesk
Upload intune devices through graph api to topdesk by api

You need the following:

1. Get card Type id from topdesk ( i made a card type named: device), retrieved the id through postman api call, and update line 69 with it:

https://yourtopdeskurl.topdesk.net/tas/api/assetmgmt/cardTypes

2. Get your graphapi details and update # Microsoft Graph API Configuration

client_id = 'your-client-id'
tenant_id = 'your-tenant-id'
client_secret = 'your-client-secret'

make sure it has permission on: DeviceManagementManagedDevices.ReadWrite.All

3. Get your Topdesk api details and update # TOPdesk Configuration

topdesk_url = 'https://yourtopdeskurl.topdesk.net/tas/api/assetmgmt/assets'
topdesk_username = 'your-topdesk-username'
topdesk_api_key = 'your-topdesk-api-key'

put the pyton script somewhere.

You have to have from msal import ConfidentialClientApplication installed.

