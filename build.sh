#!/bin/bash

docker build -t webapp:latest .
docker tag webapp:latest us-east1-docker.pkg.dev/project-name/blogsite/webapp:latest
docker push us-east1-docker.pkg.dev/project-name/blogsite/webapp:latest
