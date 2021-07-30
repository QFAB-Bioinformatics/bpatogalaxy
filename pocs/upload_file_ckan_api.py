"""
Usage: python upload_file_ckan_api.py
"""
import sys
import requests
import ckanapi

from bioblend.galaxy import GalaxyInstance

if len(sys.argv) != 9:
    print("Usage: python upload_file_ckan_api.py <galaxy-url> <galaxy-API-key> "+
          "<bpa-url> <bpa-API-key> <file-type> <file-name> <list-files-only> <upload-from-local> "+
          len(sys.argv))
    sys.exit(1)
galaxy_url = sys.argv[1]
galaxy_key = sys.argv[2]
bpa_url = sys.argv[3]
bpa_key = sys.argv[4]
bpa_file_type = sys.argv[5]
bpa_file = sys.argv[6]
list_only = sys.argv[7]
use_local = sys.argv[8]

remote = ckanapi.RemoteCKAN(bpa_url, apikey=bpa_key)
result = remote.action.package_search(
    q='type:'+bpa_file_type,
    rows=50000,
    include_private=True)

print("{} matches found.".format(result['count']))

listAll = False
if list_only == 'yes':
    listAll = True
else:
    print("\nlist_only "+list_only)

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
    print("\nuse_local "+use_local)

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

    print("Initiating Galaxy connection")

    gi = GalaxyInstance(url=galaxy_url, key=galaxy_key)

    print("Retrieving libraries list")

    libraries = gi.libraries.get_libraries()

    libraryId = libraries[0]['id']
    libraryName = libraries[0]['name']

    if len(libraries) == 1:
        print("\n start upload of file "+resource_name)
        gi.libraries.upload_file_from_local_path(libraryId,resource_name)
    else:
        print("\nDo nothing!!!")

    if len(libraries) == 0:
        print("There are no libraries in your account to upload a file to")
    else:
        print("\nupload file successful to library: "+libraryName)
