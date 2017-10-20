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
from pprint import pprint
import json
import requests

import dlrnapi_client
from dlrnapi_client.rest import ApiException

##################################################

parser = argparse.ArgumentParser(description="display promotion status for RDO releases.  Pike is the default release.",
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=25,width=180))

parser.add_argument("-r", "--release", choices=['master', 'pike', 'ocata', 'newton'])
parser.add_argument("-d", "--dashboard", help='default to http://localhost:3030, useful for testing')
parser.add_argument("-v", "--verbose")

args = parser.parse_args()

if not args.dashboard:
    args.dashboard = 'http://localhost:3030'

# TODO: this can probably go away?  really we should update all releases...for now leave it as we're prototyping with pike
if not args.release:
    args.release = "pike"

##################################################


#
# TODO: Propose API change.  This should not be something clients of dlrnapi need to codify.  It's beyond fragile.
#
def get_url_from_commit_distro(commit, distro, base_url):
    if base_url[-1] != '/':
        base_url += '/'
    return (base_url + commit[0:2] + '/' + commit[2:4] + '/' + commit + '_' + distro[:8])

def get_shorthash_from_commit_distro(commit, distro):
    return (commit + '_' + distro[:8])

# TODO: does python have a static specifier?
map_version_to_endpoint = {'master'  : 'https://trunk.rdoproject.org/api-centos-master-uc',
                           'pike'    : 'https://trunk.rdoproject.org/api-centos-pike',
                           'ocata'   : 'https://trunk.rdoproject.org/api-centos-ocata',
                           'newton'  : 'https://trunk.rdoproject.org/api-centos-newton'}

def get_endpoint(release):
    return map_version_to_endpoint[release]

# name used for Text widgets that contain the most recent promoted url
def get_promo_widget_url(dashurl, release, promote_name):
    # TODO: parameter validation
    map_name_to_widget = {'current-tripleo'              : 'promo_%s_ooo'  % release,
                          'current-tripleo-rdo'          : 'promo_%s_rdo1' % release,
                          'current-tripleo-rdo-internal' : 'promo_%s_rdo2' % release}

    widget = map_name_to_widget[promote_name]
    url = "%s/widgets/%s" % (dashurl, widget)

    return url

def update_dashboard_promotion_tile(dashurl, release, promote_name):

    host = get_endpoint(release)
 
    api_client = dlrnapi_client.ApiClient(host=host)
    api_instance = dlrnapi_client.DefaultApi(api_client=api_client)
    params = dlrnapi_client.PromotionQuery()
    
    if promote_name:
        params.promote_name = promote_name

    try:
        api_response = api_instance.api_promotions_get(params)

        # TODO: how does scoping in python work?  can i end exception block here?

        if api_response:
            # first in the list is most recent
            promo = api_response[0]

            ts = datetime.fromtimestamp(promo.timestamp)

            # RFE: Propose API change.  This is also needlessly forcing clients of the API to understand RDO infra.  
            dlrn_base_url = "https://trunk.rdoproject.org/centos7-%s" % args.release
            delorean_url = get_url_from_commit_distro(promo.commit_hash, promo.distro_hash, dlrn_base_url)
            hash_id = get_shorthash_from_commit_distro(promo.commit_hash, promo.distro_hash)

            widget_url = get_promo_widget_url(dashurl, release, promote_name)

            # TODO: pull out auth token in a better way
            postdata = { "auth_token": "YOUR_AUTH_TOKEN", 
                         "text": hash_id, 
                         "moreinfo": delorean_url,
                         "updatedAtMessage": ts.isoformat() }

            json_payload = json.dumps(postdata)

            r = requests.post(widget_url, data = json_payload)

            pprint(vars(r))

    except ApiException as e:
        print("Exception when calling DefaultApi->api_promotions_get: %s\n" % e)

###

update_dashboard_promotion_tile(args.dashboard, args.release, 'current-tripleo')
update_dashboard_promotion_tile(args.dashboard, args.release, 'current-tripleo-rdo')
update_dashboard_promotion_tile(args.dashboard, args.release, 'current-tripleo-rdo-internal')

# TODO: add combined view (name is None)