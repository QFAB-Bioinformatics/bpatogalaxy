"""
Usage: python poc_bpa_cloudstor.py <couldstor-url> <couldstor-user> <couldstor-key> <couldstor-dir>
<bpa-url> <bpa-API-key> <file-type> <file-name> <list-files-only> <upload-from-local>
"""

import sys
import requests
import ckanapi
from webdav3.client import Client

if len(sys.argv) != 11:
    print('Usage: python poc_bpa_cloudstor.py <couldstor-url> <couldstor-user> <couldstor-key> <couldstor-dir> '+
          '<bpa-url> <bpa-API-key> <file-type> <file-name> <list-files-only> <upload-from-local> '+
          len(sys.argv))
    sys.exit(1)
couldstor_url = sys.argv[1]
couldstor_user = sys.argv[2]
couldstor_key = sys.argv[3]
couldstor_dir = sys.argv[4]
bpa_url = sys.argv[5]
bpa_key = sys.argv[6]
bpa_file_type = sys.argv[7]
bpa_file = sys.argv[8]
list_only = sys.argv[9]
use_local = sys.argv[10]

remote = ckanapi.RemoteCKAN(bpa_url, apikey=bpa_key)
result = remote.action.package_search(
    q='type:'+bpa_file_type,
    rows=50000,
    include_private=True)

print('{} matches found.'.format(result['count']))

listAll = False
if list_only == 'yes':
    listAll = True
else:
    print('\nlist_only '+list_only)

listCount = 20
if listAll == True:
    indexCount = 0
    for package in result['results']:
        for resource in package['resources']:
            if indexCount < listCount:
                indexCount = indexCount + 1
                print(resource['name']) 

uploadFromLocal = False
if use_local == 'yes':
    uploadFromLocal = True
else:
    print('use_local '+use_local)

downloadCount =  0
resource_name = ''
if listAll == False:
    for package in result['results']:
        for resource in package['resources']:
            if resource['name'] == bpa_file and downloadCount == 0:
                resource_name = resource['name']
                print(resource_name) 
                resource_url = resource['url']
                print(str(resource_url)) 
                resp = requests.get(resource_url, headers={'Authorization': remote.apikey})
                if uploadFromLocal == False:
                    with open(resource_name, 'wb') as fd:
                        fd.write(resp.content)
                downloadCount = 1

print('\nInitiating couldstor connection')
options = {
 'webdav_hostname': couldstor_url,
 'webdav_login':    couldstor_user,
 'webdav_password': couldstor_key
}
client = Client(options)
client.verify = False # To not check SSL certificates (Default = True)
# client.session.proxies(...) # To set proxy directly into the session (Optional)
# client.session.auth(...) # To set proxy auth directly into the session (Optional)
free_size = client.free()
print('free_size '+str(free_size))
files1 = client.list()
print('files '+str(files1))
couldstor_dir_exists = client.check(couldstor_dir)
print('check dir: "'+couldstor_dir+'" exists: '+str(couldstor_dir_exists))
if not couldstor_dir_exists:
    client.execute_request('mkdir', '/'+couldstor_dir)
client.upload_sync(remote_path='/'+couldstor_dir+'/'+bpa_file, local_path=bpa_file)
print('Upload successful!!!')