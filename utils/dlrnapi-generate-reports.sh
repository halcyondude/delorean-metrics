#!/usr/bin/env bash

#
# Copyright (C) 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
# upstream:  tripleo-ci-testing
# rdophase1: current-tripleo-rdo
# rdophase2: current-tripleo-rdo-internal


dest=/tmp/dlrnapi-reports
rm -rf $dest
mkdir -p $dest

function print_promotion_report()
{
    set -x

    release=$1
    ./dlrnapi-get-promotions.py -r $release                                 > $dest/$release-combined.txt
    ./dlrnapi-get-promotions.py -r $release -n tripleo-ci-testing           > $dest/$release-tripleo-ci-testing.txt
    ./dlrnapi-get-promotions.py -r $release -n current-tripleo-rdo          > $dest/$release-current-tripleo-rdo.txt
    ./dlrnapi-get-promotions.py -r $release -n current-tripleo-rdo-internal > $dest/$release-current-tripleo-rdo-internal.txt

    set +x

}

rm -rf .venv-dlrnapi
virtualenv .venv-dlrnapi
source .venv-dlrnapi/bin/activate
pip install git+https://github.com/javierpena/dlrnapi_client.git

echo ""

echo "=================="
echo "promotions: master"
echo "=================="
print_promotion_report master

echo "=================="
echo "promotions: pike"
echo "=================="
print_promotion_report pike

echo "================="
echo "promotions: ocata"
echo "================="
print_promotion_report ocata

echo "=================="
echo "promotions: newton"
echo "=================="
print_promotion_report newton

echo ""
echo "Reports are here: $dest"
ls -laF $dest