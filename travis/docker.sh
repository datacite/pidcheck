#!/bin/bash

set -e

# Login
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD";

# We want to tag builds as appropriate
if [ "${TRAVIS_TAG?}" ]; then
    TAG=$TRAVIS_TAG;
elif [ "${TRAVIS_BRANCH?}" ]; then
    TAG=$TRAVIS_BRANCH;
else
    # Generic fallback
    # Remember that latest in docker land means latest build which is not
    # nescessarily the latest release version
    TAG="latest"
fi

echo "Tagging builds with ":$TAG

docker build --rm -f docker/crawler/Dockerfile -t 'datacite/crawler':$TAG .

# Run tests within the docker builds
# TODO

# Push master and tagged releases
# Don't push other branches by default

if [ "$TRAVIS_BRANCH" = "master" ] || [ "$TRAVIS_TAG" ]; then
    docker push 'datacite/crawler':$TAG;
    echo "Pushed docker image to" 'datacite/crawler':$TAG;
fi