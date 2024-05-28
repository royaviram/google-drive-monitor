# google-drive-monitor
This script monitors your Google Drive for new files and ensures that files are not publicly accessible by changing their permissions if necessary. It also checks the default sharing settings of newly created files.

Prerequisites:
1. Python Environment: Ensure you have Python 3.x installed on your system.
2. Google Cloud Project: You need to have a Google Cloud project with the Google Drive API enabled.
3. Service Account: Create a service account in your Google Cloud project with sufficient permissions to access and modify files in your Google Drive.

Setup:
1. Place the Service Account Credentials File: Save the downloaded JSON file in the project folder and name it secret.json.
2. Install Required Python Packages:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

How to run the script:

python main.py


Scopes and Tokens:
Scope: 'https://www.googleapis.com/auth/drive' - This scope allows full access to all files in the user's Google Drive, including read, write and delete files. By using this scope, the script can perform comprehensive management of the files' permissions.
Service Account: The script uses a service account private key defined in the secret.json file for authentication and API access.

Example Output:
File test_file1 - file_id has been checked for overly permissive permissions. It has been found that the file was public and changed to private
File test_file2 - file_id has been checked for overly permissive permissions. The file is currently not public
The default sharing settings in this account are publicly accessible. The settings are as follows: [list of permissions]

Potential Attack Surfaces
1. Publicly Accessible Files: Files with permissions set to 'anyone' can be accessed by anyone who holds the link. This makes the link sensitive data that, if leaked, can lead to data exfiltration and unauthorized access..
2. Overly Permissive Default Sharing Settings: If the default sharing settings for newly created files are too permissive, it can result in all newly created files being publicly accessible by default.
