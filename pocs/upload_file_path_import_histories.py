"""
Usage: python upload_file_aws_presigned_url.py <galaxy-url> <galaxy-API-key> <file-path>
"""

import sys

from bioblend.galaxy import GalaxyInstance

if len(sys.argv) != 4:
    print("Usage: python upload_file_aws_presigned_url.py <galaxy-url> <galaxy-API-key> <file-path>")
    sys.exit(1)
galaxy_url = sys.argv[1]
galaxy_key = sys.argv[2]
hist_arch_file_path = sys.argv[3]

print("Initiating Galaxy connection")

gi = GalaxyInstance(url=galaxy_url, key=galaxy_key)

print("Retrieving histories list")

histories = gi.histories.get_histories()

if len(histories) == 0:
    print("There are no Histories in your account.")
else:
    print("\nHistories:")
    for hist_dict in histories:
        # As an example, we retrieve a piece of metadata (the size) using show_history
        hist_details = gi.histories.show_history(hist_dict['id'])
        print(f"{hist_dict['name']} ({hist_details['size']}) : {hist_dict['id']}")

print("Uploading from local path to histories")

gi.histories.import_history(file_path=hist_arch_file_path,url=None)

