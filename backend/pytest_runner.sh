#!/bin/bash

export ENVIRONMENT="testing"
flask db upgrade
pytest
unset ENVIRONMENT
rm -Rf ../instance
