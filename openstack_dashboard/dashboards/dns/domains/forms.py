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
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api


class DomainCreate(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Domain Name"))
    email = forms.CharField(max_length="255", label=_("Email"))

    # def __init__(self, *args, **kwargs):
    #     super(FloatingIpAllocate, self).__init__(*args, **kwargs)
    #     floating_pool_list = kwargs.get('initial', {}).get('pool_list', [])
    #     self.fields['pool'].choices = floating_pool_list

    def handle(self, request, data):
        try:
            domain = api.moniker.domain_create(request, name=data['name'],
                                               email=data['email'])
            messages.success(request,
                             _('Domain created %(name)s.')
                             % {"name": domain.name})
            return domain
        except:
            exceptions.handle(request, _('Unable to create domain.'))
