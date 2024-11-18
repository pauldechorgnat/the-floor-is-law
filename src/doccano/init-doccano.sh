docker container create \
 --name doccano \
 -p 8000:8000 \
 --env-file .env \
 doccano/doccano
docker container start doccano