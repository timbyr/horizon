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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import forms
from horizon import tabs

from openstack_dashboard import api
from .tables import DomainsTable
from .forms import DomainCreate
from .tabs import DomainDetailTabs


class IndexView(tables.DataTableView):
    table_class = DomainsTable
    template_name = 'dns/domains/index.html'

    def get_data(self):
        try:
            return api.moniker.domain_list(self.request)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve domain list.'))


class DetailView(tabs.TabView):
    tab_group_class = DomainDetailTabs
    template_name = 'project/volumes/detail.html'


class CreateView(forms.ModalFormView):
    form_class = DomainCreate
    template_name = 'dns/domains/create.html'
    success_url = reverse_lazy('horizon:dns:domains:index')

    def get_object_display(self, obj):
        return obj.ip

    # def get_context_data(self, **kwargs):
    #     context = super(CreateView, self).get_context_data(**kwargs)
    #     try:
    #         context['usages'] = quotas.tenant_quota_usages(self.request)
    #     except:
    #         exceptions.handle(self.request)
    #     return context

    # def get_initial(self):
    #     try:
    #         pools = api.moniker.floating_ip_pools_list(self.request)
    #     except:
    #         pools = []
    #         exceptions.handle(self.request,
    #                           _("Unable to retrieve floating IP pools."))
    #     pool_list = [(pool.id, pool.name) for pool in pools]
    #     if not pool_list:
    #         pool_list = [(None, _("No floating IP pools available."))]
    #     return {'pool_list': pool_list}
