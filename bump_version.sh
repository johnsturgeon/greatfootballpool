#!/bin/bash
# usage: [major, minor, patch]
poetry version $1
git add .
git commit -m "bumped version"
NEW_VERSION=`poetry version -s`
git tag v${NEW_VERSION}
git push origin v${NEW_VERSION}