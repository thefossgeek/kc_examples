#!/usr/bin/python

from keystoneclient.v2_0 import client
from keystoneclient import utils
from keystoneclient import base
import six

a_args = {
          "username":"admin",
          "password":"admin",
          "tenant_name":"admin",
          "auth_url":"http://10.209.224.53:5000/v2.0"
         }

t_args = {
          "tenant_name":"test",
          "description":"Test Project",
          "enabled":True
         }

u_args = {
          "name":"test",
          "password":"test123",
          "email":"test@example.com",
          "enabled":True
         }

class CreateAccess():
	"""class for creating tenant, user and assign `admin` role to a user-project pair."""
	def __init__(self):
		"""Initialize a new class."""
		self.keystone = ''
		self.t_id = ''
		self.u_id = ''
		self.r_id = ''

	def do_auth(self,**kwargs):
		"""Initialize a new client and does the authentication"""
		self.keystone=client.Client(**kwargs)

	def do_create_t(self,**kwargs):
		"""Create a new tenant."""
		return self.keystone.tenants.create(**kwargs)
	
	def do_create_u(self,**kwargs):
		"""Create a user."""
		return self.keystone.users.create(**kwargs)

	def do_get_role_id(self):
		"""Return role details for admin role."""
		return utils.find_resource(self.keystone.roles,"admin")		
	
	def do_add_user_r(self):
		"""Adds a role to a user."""
		return self.keystone.roles.add_user_role(self.u_id,self.r_id,self.t_id)

	def return_value(self,d):
		"""Return id from List {'values': [ ... ]}"""
		id = ''
		for (prop, value) in six.iteritems(d):
			if prop == 'id':
				id = value
		return id
	
if __name__ == "__main__":
	obj=CreateAccess()
	obj.do_auth(**a_args)
	tenant=obj.do_create_t(**t_args)
	obj.t_id=obj.return_value(tenant._info)
	user=obj.do_create_u(**u_args)
	obj.u_id=obj.return_value(user._info)
	role = obj.do_get_role_id()
	obj.r_id=obj.return_value(role._info)
	ret = obj.do_add_user_r()
	utils.print_dict(ret._info)

