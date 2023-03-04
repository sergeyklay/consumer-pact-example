#!/usr/bin/env bash

# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

root_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

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

# To get the most out of the Pact Broker, it should either be the git sha
# (or equivalent for your repository), be a git tag name, or it should
# include the git sha or tag name as metadata if you are using semantic
# versioning eg. 1.2.456+405b31ec6.
#
# See https://docs.pact.io/pact_broker/pacticipant_version_numbers for more
# details.
app_version="$(python setup.py --version)"
app_version+="+$(git -C "$root_dir" rev-parse --short HEAD)"

$containerd_cli run \
  --rm \
  -v "$(pwd)"/tests/pacts:/pacts \
  -e PACT_BROKER_BASE_URL="${PACT_BROKER_BASE_URL:-http://broker_app:9292}" \
  -e PACT_BROKER_USERNAME="${PACT_BROKER_USERNAME:-pactbroker}" \
  -e PACT_BROKER_PASSWORD="${PACT_BROKER_USERNAME:-pactbroker}" \
  --network "${BROKER_NETWORK:-broker_default}" \
  pactfoundation/pact-cli:latest \
  publish /pacts \
    --tag release-42 \
    --tag feature-N \
    --tag team-A \
    --consumer-app-version="$app_version" \
    --branch="$(git -C "$root_dir" rev-parse --abbrev-ref HEAD)"
