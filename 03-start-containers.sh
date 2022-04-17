#!/bin/bash

if ! command -v docker &> /dev/null
then
    echo "Docker is not available on this system!"
    exit
fi

if command -v docker-compose &> /dev/null
then
    echo "Stopping and removing old containers"
    docker-compose rm -sf &> /dev/null
    echo "Starting new containers"
    docker-compose up --force-recreate -d &> /dev/null
    exit
fi

if command -v docker compose &> /dev/null
then
    echo "Stopping and removing old containers"
    docker compose rm -sf &> /dev/null
    echo "Starting new containers"
    docker compose up --force-recreate -d &> /dev/null
    exit
fi

echo "Docker compose is not installed!"
exit