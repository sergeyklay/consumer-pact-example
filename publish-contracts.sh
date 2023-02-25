#!/usr/bin/env bash

docker run -ti \
  --rm \
  -v "$(pwd)"/tests/pacts:/pacts \
  -e PACT_BROKER_BASE_URL="${PACT_BROKER_BASE_URL:-http://broker_app:9292}" \
  -e PACT_BROKER_USERNAME="${PACT_BROKER_USERNAME:-pactbroker}" \
  -e PACT_BROKER_PASSWORD="${PACT_BROKER_USERNAME:-pactbroker}" \
  --network broker_backend \
  pactfoundation/pact-cli:latest \
  publish /pacts \
    --consumer-app-version="${CONSUMER_VERSION:-1}" \
    --branch="$(git rev-parse --abbrev-ref HEAD)" \
    --verbose
