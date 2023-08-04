#!/bin/bash

# initialize app and AWS env vars
. .env

# get ECR token
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# create ECR repository
if [ -z "$(aws ecr describe-repositories --output text | grep $APP_NAME-repository)" ]; then
    aws ecr create-repository --repository-name "$APP_NAME-repository"
fi

# build docker image
tar zc src docker | docker build --rm -t "$APP_NAME:$APP_VERSION" -f docker/Dockerfile -
# docker build --rm -t "$APP_NAME:$APP_VERSION" -f docker/Dockerfile .
# docker build --rm --platform=linux/amd64 -t "$APP_NAME:$APP_VERSION" -f docker/Dockerfile .

# tag docker image
docker tag "$APP_NAME:$APP_VERSION" "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME-repository"

# push docker image to ECR
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME-repository"
