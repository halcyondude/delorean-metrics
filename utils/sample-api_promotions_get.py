#!/usr/bin/env python

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

release="pike"
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

