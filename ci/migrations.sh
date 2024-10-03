#!/usr/bin/env bash

# Run migrations printing before the plan and after the status

set -e
flask db upgrade
