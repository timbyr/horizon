# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Author: Kiall Mac Innes <kiall@hp.com>
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
from __future__ import absolute_import

import logging

from designateclient.v1 import Client
from designateclient.v1.domains import Domain

from openstack_dashboard.api.base import url_for
from horizon import exceptions

LOG = logging.getLogger(__name__)


def designateclient(request):
    designate_url = ""
    try:
        designate_url = url_for(request, 'dns')
    except exceptions.ServiceCatalogException:
        LOG.debug('no dns service configured.')
        return None
        
    LOG.debug('designateclient connection created using token "%s" and url "%s"' %
              (request.user.token.id, designate_url))

    return Client(endpoint=designate_url,
                  token=request.user.token.id,
                  username=request.user.username,
                  tenant_id=request.user.project_id)


def domain_get(request, domain_id):
    d_client = designateclient(request)
    if d_client is None:
        return []
    return d_client.domains.get(domain_id)


def domain_list(request):
    d_client = designateclient(request)
    if d_client is None:
        return []
    return d_client.domains.list()


def domain_create(request, name, email):
    d_client = designateclient(request)
    if d_client is None:
        return None

    domain = Domain(name=name, email=email)

    return d_client.domains.create(domain)


def domain_delete(request, domain_id):
    d_client = designateclient(request)
    if d_client is None:
        return []
    return d_client.domains.delete(domain_id)


def record_list(request, domain_id):
    d_client = designateclient(request)
    if d_client is None:
        return []
    return d_client.records.list(domain_id)
