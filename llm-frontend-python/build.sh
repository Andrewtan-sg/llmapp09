#!/usr/bin/env sh
set -eu
: "${DOCKERHUB_USERNAME:?Set DOCKERHUB_USERNAME to your Docker Hub username}"
docker build -t "${DOCKERHUB_USERNAME}/llm-frontend-python:latest" .
docker push "${DOCKERHUB_USERNAME}/llm-frontend-python:latest"
