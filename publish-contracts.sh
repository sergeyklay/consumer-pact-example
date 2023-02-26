#!/usr/bin/env bash

# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.


rdctl="${RANCHERCTL:-$(command -v rdctl 2>/dev/null)}"
containerd_cli=""

# Try to get a suitable container engine (if available)
if [ -n "${rdctl}" ]; then
  if $rdctl list-settings | grep -q '"containerEngine": "moby"'; then
    containerd_cli="${DOCKER:-$(command -v docker 2>/dev/null)}"
  else
    containerd_cli="${NERDCTL:-$(command -v nerdctl 2>/dev/null)}"
  fi
else
  containerd_cli="${DOCKER:-$(command -v docker 2>/dev/null)}"
fi

# In order for docker to allocate a TTY (the -t option) you already need
# to be in a TTY when docker run is called.
# GitHub Actions executes its jobs not in a TTY.
options='-i'
test -t 1 && options="-ti"

$containerd_cli run $options \
  --rm \
  -v "$(pwd)"/tests/pacts:/pacts \
  -e PACT_BROKER_BASE_URL="${PACT_BROKER_BASE_URL:-http://broker_app:9292}" \
  -e PACT_BROKER_USERNAME="${PACT_BROKER_USERNAME:-pactbroker}" \
  -e PACT_BROKER_PASSWORD="${PACT_BROKER_USERNAME:-pactbroker}" \
  --network "${BROKER_NETWORK:-broker_default}" \
  pactfoundation/pact-cli:latest \
  publish /pacts \
    --consumer-app-version="${CONSUMER_VERSION:-$(python setup.py --version)}" \
    --branch="$(git rev-parse --abbrev-ref HEAD)"
