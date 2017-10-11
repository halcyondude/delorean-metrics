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
from datetime import date, datetime
import dlrnapi_client
from dlrnapi_client.rest import ApiException

def get_url_from_commit_distro(commit, distro, base_uri):
    if base_uri[-1] != '/':
        base_uri += '/'
    return (base_uri + commit[0:2] + '/' + commit[2:4] + '/' + commit + '_' + distro[:8])

release="master-uc"
base_uri="https://trunk.rdoproject.org/centos7-%s" % release
host="https://trunk.rdoproject.org/api-centos-%s" % release

api_client = dlrnapi_client.ApiClient(host=host)
api_instance = dlrnapi_client.DefaultApi(api_client=api_client)

params = dlrnapi_client.PromotionQuery()
# params.promote_name = "current-tripleo-rdo-internal"

try: 
    api_response = api_instance.api_promotions_get(params)

    for promo in api_response:
        t = datetime.fromtimestamp(promo.timestamp)
        delorean_url = get_url_from_commit_distro(promo.commit_hash, promo.distro_hash, base_uri)
        print("Date %s, link: %s, uri: %s" % (t, promo.promote_name, delorean_url))

except ApiException as e:
    print("Exception when calling DefaultApi->api_promotions_get: %s\n" % e)

