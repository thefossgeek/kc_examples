#!/usr/bin/python

from keystoneclient.v2_0 import client
from keystoneclient import utils

keystone = client.Client(username="admin",
                         password="admin",
                         tenant_name="admin",
                         auth_url="http://<controller_ip>:5000/v2.0"
                        )
roles = keystone.roles.list()
utils.print_list(roles, ['id', 'name'], order_by='name')
