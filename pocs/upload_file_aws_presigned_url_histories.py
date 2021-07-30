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
galaxy_s3_url_file = sys.argv[3]

print("Initiating Galaxy connection")

gi = GalaxyInstance(url=galaxy_url, key=galaxy_key)

print("Retrieving histories list")

histories = gi.histories.get_histories()

print("Uploading from history to url")
token_name="Authorization"
token_key="5157c8ad-9aa6-425c-9feb-e62d2089c601"
# gi.histories.import_history(None,url=galaxy_s3_url_file)
gi.histories.upload_history_from_url(url=galaxy_s3_url_file,token_name=token_name,token_key=token_key)

