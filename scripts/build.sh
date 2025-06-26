#!/bin/bash

set -e

source .env
TAR_PATH=./build/${IMAGE_NAME}.tar

echo "Removing old tar if it exists..."
[ -f "$TAR_PATH" ] && rm "$TAR_PATH"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Saving Docker image to tar..."
docker save -o $TAR_PATH $IMAGE_NAME

echo "Copying image to remote machine..."
scp $TAR_PATH ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}

echo "Loading image on remote machine and restarting container..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << EOF
  docker load -i ${REMOTE_DIR}/${IMAGE_NAME}.tar
  docker stop $IMAGE_NAME || true
  docker rm $IMAGE_NAME || true
  docker run -d --network host --name $IMAGE_NAME $IMAGE_NAME
  docker image prune -f
EOF
