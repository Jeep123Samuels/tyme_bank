#!/bin/bash

export ENVIRONMENT="testing"
flask db init
flask db migrate
flask db upgrade
pytest
unset ENVIRONMENT
rm -Rf ../instance