"""
Usage: python upload_file_aws_presigned_url.py <galaxy-url> <galaxy-API-key> <pre-signed-url>
"""

import sys

from bioblend.galaxy import GalaxyInstance

if len(sys.argv) != 4:
    print("Usage: python upload_file_aws_presigned_url.py <galaxy-url> <galaxy-API-key> <pre-signed-url>")
    sys.exit(1)
galaxy_url = sys.argv[1]
galaxy_key = sys.argv[2]
url = sys.argv[3]

print("Initiating Galaxy connection")

gi = GalaxyInstance(url=galaxy_url, key=galaxy_key)

print("Retrieving libraries list")

libraries = gi.libraries.get_libraries()

libraryId = libraries[0]['id']
libraryName = libraries[0]['name']

if len(libraries) == 1:
    gi.libraries.upload_file_from_url(libraryId,url)
else:
    print("\nDo nothing!!!")

if len(libraries) == 0:
    print("There are no libraries in your account to upload a file to")
else:
    print("\nupload file successful to library: "+libraryName)
