#!/usr/bin/env python

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

#
# REQUIRED: pip install -r requirements-dlrnapi-get-promotions.txt
#
# https://github.com/softwarefactory-project/dlrnapi_client#getting-started
#
from __future__ import print_function
import argparse
import os
from datetime import datetime
import time
import dlrnapi_client
from dlrnapi_client.rest import ApiException
from pprint import pprint

#
# TODO: Propose API change.  This should not be something clients of dlrnapi need to codify in script.  It's fragile.
#
def get_url_from_commit_distro(commit, distro, base_uri):
    if base_uri[-1] != '/':
        base_uri += '/'
    return (base_uri + commit[0:2] + '/' + commit[2:4] + '/' + commit + '_' + distro[:8])


#
# handle args
#
parser = argparse.ArgumentParser(description="display promotion status for RDO releases.  Pike is the default release.",
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=25,width=180))

parser.add_argument("-r", "--release", choices=['master', 'queens', 'pike', 'ocata', 'newton'])
parser.add_argument("-n", "--name",    choices=['tripleo-ci-testing', 'current-tripleo', 'current-tripleo-rdo', 'current-tripleo-rdo-internal'])
args = parser.parse_args()

map_version_to_endpoint = {'master'  : 'https://trunk.rdoproject.org/api-centos-master-uc',
                           'queens'  : 'https://trunk.rdoproject.org/api-centos-queens',
                           'pike'    : 'https://trunk.rdoproject.org/api-centos-pike',
                           'ocata'   : 'https://trunk.rdoproject.org/api-centos-ocata',
                           'newton'  : 'https://trunk.rdoproject.org/api-centos-newton'}

if not args.release:
    args.release = "pike"

# upstream:  tripleo-ci-testing
# rdophase1: current-tripleo-rdo
# rdophase2: current-tripleo-rdo-internal

# TODO: Propose API change.  This is also needlessly forcing clients of the API to understand RDO infra.  These should just be returned
base_uri = "https://trunk.rdoproject.org/centos7-%s" % args.release

host = map_version_to_endpoint[args.release]

api_client = dlrnapi_client.ApiClient(host=host)
api_instance = dlrnapi_client.DefaultApi(api_client=api_client)

params = dlrnapi_client.PromotionQuery()

# it not specified will just list all promotions
if args.name:
    params.promote_name = args.name

try:
    api_response = api_instance.api_promotions_get(params)

    for promo in api_response:
        t = datetime.fromtimestamp(promo.timestamp)
        delorean_url = get_url_from_commit_distro(promo.commit_hash, promo.distro_hash, base_uri)
        print("%s, %s, %s" % (t, delorean_url, promo.promote_name))

except ApiException as e:
    print("Exception when calling DefaultApi->api_promotions_get: %s\n" % e)

