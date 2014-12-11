#!/usr/bin/python

from keystoneclient.v2_0 import client
from keystoneclient import utils

keystone = client.Client(username="admin",
                         password="admin",
                         tenant_name="admin",
                         auth_url="http://<controller_ip>:5000/v2.0"
                        )
users = keystone.users.list()
utils.print_list(users, ['id', 'name', 'enabled','email'], order_by='name')
