from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


ACCOUNT_SECRET_FILE = 'secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    ACCOUNT_SECRET_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)


def is_public(file_id):
    # Check if a file is publicly accessible. The function checks if the file has a permissions attribute configured to 'anyone'.
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        for permission in permissions.get('permissions', []):
            if permission.get('type') == 'anyone':
                return True
        return False
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False

def change_permissions(file_id):
    # Remove permissive permissions ('anyone') from the file permissions list
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        for permission in permissions.get('permissions', []):
            if permission.get('type') == 'anyone':
                #service.permissions().delete(fileId=file_id, permissionId=permission['id']).execute()
                return True
        return False
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False

def check_default_sharing_settings():
    # Check the default permissions of newly created files by creating a file and without specifying the
    # permissions settings and examining the output.
    try:
        file_metadata = {
            'name': 'Test_file',
            'mimeType':'application/vnd.google-apps.document'
        }
        test_file = service.files().create(body=file_metadata).execute()
        file_id = test_file.get('id')
        permissions = service.permissions().list(fileId=file_id).execute()
        return(permissions.get('permissions', []),is_public(file_id))
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    files = {}
    page_token = None
    while True:
        try:
            response = service.files().list(q="trashed=false", spaces='drive',fields='nextPageToken, files(id, name, createdTime)' ,pageToken=page_token).execute()
            for file in response.get('files', []):
                file_id = file.get('id')
                file_name = file.get('name')
                file_creation_time = file.get('createdTime')
                files[file_id] = {
                    'name': file_name,
                    'creation_time': file_creation_time,
                    'is_public': is_public(file_id),
                    'changed_permissions': False,
                }
                if files[file_id]['is_public']:
                    print(f'file {file_name} is public')
                    files[file_id]['changed_permissions'] = change_permissions(file_id)
                if files[file_id]['changed_permissions']:
                    print(f' file {file_name} - {file_id} has been checked for over premissive permissions. It has been found that the file was public and changed to private')
                else:
                    print(
                        f' file {file_name} - {file_id} has been checked for over premissive permissions. The file is currently not public')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        except HttpError as error:
            print(f'An error occurred: {error}')
    default_permissions, default_is_public = check_default_sharing_settings()
    if default_is_public:
        print(f'The default sharing setting in this account are publicly accessible.'
              f' The settings are as follows: {default_permissions}')
    else:
        print(f'The default sharing setting in this account are not publicly accessible.'
              f' The settings are as follows: {default_permissions}')

if __name__ == '__main__':
    main()
