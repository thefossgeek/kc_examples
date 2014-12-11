#!/usr/bin/python

from keystoneclient.v2_0 import client
from keystoneclient import utils

keystone = client.Client(token="token",
                         endpoint="http://<controller_ip>:35357/v2.0"
						)
tenants = keystone.tenants.list()
utils.print_list(tenants, ['id', 'name', 'enabled'], order_by='name')
