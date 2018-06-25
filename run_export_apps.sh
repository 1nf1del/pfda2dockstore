#!/usr/bin/env bash

ORG=pfda2dockstore

docker login

prompt() {
    echo -n "$1: " && read $2 $1 && echo
}

if [[ -z $ORG ]]; then
    echo "Please enter your github org"
    prompt "ORG"
fi
if [[ -z $PFDA_TOKEN ]]; then
    echo "Please enter your PFDA token"
    prompt "PFDA_TOKEN"
fi
if [[ -z $GITHUB_TOKEN ]]; then
    echo "Please enter your github token"
    prompt "GITHUB_TOKEN"
fi
if [[ -z $DS_TOKEN ]]; then
    echo "Please enter your Dockstore token"
    prompt "DS_TOKEN"
fi

APP_LIST_PATH=$1
if [[ -z $APP_LIST_PATH ]]; then
    option="--export-all-apps"
else
    option="--export-apps $APP_LIST_PATH" 
fi

python3 pfda2dockstore \
  $option \
  --pfda-token $PFDA_TOKEN \
  --github-org $ORG \
  --github-token $GITHUB_TOKEN \
  --dockerhub-org $ORG \
  --dockstore-token $DS_TOKEN \
  --dockstore-org $ORG
