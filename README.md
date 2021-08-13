# bpatogalaxy
BPA to Galaxy repo to store early POCs and other relevant documents

# Instructions for running POCs
1. If already installed skip step 1 
```
sudo apt install python3-venv
```
2. Run python3 command to create virtual environment  
```
python3 -m venv my-anyname-env
```
3. Modify env files as required then source each one
```
source bpatogalaxy.env
source bpatogalaxy_settings.env
```
4. Activate your python virtual env
```
source my-anyname-env/bin/activate
```
5. Install python libraries inside your virtual as required
```
pip install bioblend
pip install ckanapi
pip install webdavclient3
```
6. Run POCs passing the right parameters
```
python3 upload_file_aws_presigned_url_libraries.py $BIOBLEND_GALAXY_URL $BIOBLEND_GALAXY_API_KEY $AWS_PRESIGNED_URL
python3 upload_file_aws_presigned_url_histories.py $BIOBLEND_GALAXY_URL $BIOBLEND_GALAXY_API_KEY $AWS_PRESIGNED_URL
python3 upload_file_ckan_api.py $BIOBLEND_GALAXY_URL $BIOBLEND_GALAXY_API_KEY $BPA_PORTAL_URL $BPA_PORTAL_KEY $BPA_PORTAL_FYLE_TYPE $BPA_PORTAL_FILE_NAME 
python3 poc_bpa_cloudstor.py $CLOUDSTOR_URL $CLOUDSTOR_USER $CLOUDSTOR_KEY $CLOUSTOR_DIR $BPA_PORTAL_URL $BPA_PORTAL_KEY $BPA_PORTAL_FYLE_TYPE $BPA_PORTAL_FILE_NAME $LIST_FILES_ONLY $UPLOAD_FROM_LOCAL $LIST_FILES_ONLY $UPLOAD_FROM_LOCAL
```
7. Deactivate your virtual env using below command
```
deactivate
```
