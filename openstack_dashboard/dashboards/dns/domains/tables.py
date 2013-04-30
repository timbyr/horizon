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
import logging

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class CreateDomain(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Domain")
    url = "horizon:dns:domains:create"
    classes = ("ajax-modal", "btn-create")


class DeleteDomain(tables.BatchAction):
    name = "delete"
    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Domain")
    data_type_plural = _("Domains")
    classes = ('btn-danger', 'btn-delete')

    def allowed(self, request, instance=None):
        return True

    def action(self, request, domain_id):
        api.moniker.domain_delete(request, domain_id)


class DomainsTable(tables.DataTable):
    name = tables.Column("name",
                         link=("horizon:dns:domains:detail"),
                         verbose_name=_("Name"))
    email = tables.Column("email",
                          verbose_name=_("Email"))
    serial = tables.Column("serial",
                           verbose_name=_("Serial"))

    class Meta:
        name = "domains"
        verbose_name = _("Domains")
        # status_columns = ["status", "task"]
        # row_class = UpdateRow
        table_actions = (CreateDomain, DeleteDomain,)
        row_actions = (DeleteDomain,)


class RecordsTable(tables.DataTable):
    name = tables.Column("name",
                         link=("horizon:dns:domains:detail"),
                         verbose_name=_("Name"))
    # type = tables.Column("type",
    #                      verbose_name=_("Type"))
    # date = tables.Column("serial",
    #                      verbose_name=_("Data"))

    class Meta:
        name = "records"
        verbose_name = _("Records")
        # table_actions = (CreateDomain, DeleteDomain,)
        # row_actions = (DeleteDomain,)
