#!/usr/bin/python

from keystoneclient.v2_0 import client
import json
from keystoneclient import utils

keystone = client.Client(username="admin",
                         password="admin",
                         tenant_name="admin",
                         auth_url="http://<controller_ip>:5000/v2.0"
						)
tenants_list=keystone.tenants.list()
print tenants_list
utils.print_list(tenants_list, ['id', 'name', 'enabled'], order_by='name')
