#!/usr/bin/python

from keystoneclient.v2_0 import client
from keystoneclient import utils
from keystoneclient import base
import six

bootstrap_mode = {
          "token":"token",
          "endpoint":"http://<controller_ip>:35357/v2.0",
         }

# Here is the list of users associated with admin tenant and admin role.
admin_users=['admin','demo']

# Here is the list of users associated with service tenant and service role.
service_users=['ceilometer','cinder','glance','heat','neutron','murano','nova','sahara','swift']


class CreateAccess():
	"""class for creating tenant, user and assign `admin` role to a user-project pair."""
	def __init__(self):
		"""Initialize a new class."""
		self.keystone = ''
		self.admin_t_id = ''
		self.service_t_id = ''
		self.admin_r_id = ''
		self.service_r_id = ''
		self.user_id = ''

	def do_auth(self,**kwargs):
		"""Initialize a new client and does the authentication"""
		self.keystone=client.Client(**kwargs)

	def do_get_tenant_id(self,tenant_name):
		"""Return tenant details """
		return utils.find_resource(self.keystone.tenants,tenant_name)		
	
	def do_get_role_id(self,role_name):
		"""Return role details for the given role."""
		return utils.find_resource(self.keystone.roles,role_name)		

	def do_get_user_id(self,user_name):
		"""Return user details for the given user."""
		return utils.find_resource(self.keystone.users,user_name)		
    
	def do_role_assignment(self,whatrole):
		"""Associates a user with a tenant and a role"""
		if whatrole == 'admin':
			return self.keystone.roles.add_user_role(self.user_id,
                                                     self.admin_r_id,
                                                     self.admin_t_id
                                                    )
		elif whatrole == 'service':
			return self.keystone.roles.add_user_role(self.user_id,
                                                     self.service_r_id,
                                                     self.service_t_id
                                                    )
		else:
			return None
	

	def return_value(self,d):
		"""Return id from List {'values': [ ... ]}"""
		id = ''
		for (prop, value) in six.iteritems(d):
			if prop == 'id':
				id = value
		return id
	
if __name__ == "__main__":
	obj=CreateAccess()
	obj.do_auth(**bootstrap_mode)
	atid = obj.do_get_tenant_id("admin")
	obj.admin_t_id=obj.return_value(atid._info)
	stid = obj.do_get_tenant_id("service")
	obj.service_t_id=obj.return_value(stid._info)
	print "Admin Tenant Id: %s" % obj.admin_t_id
	print "Service Tenant Id: %s" % obj.service_t_id
	arid = obj.do_get_role_id("admin")
	obj.admin_r_id=obj.return_value(arid._info)
	srid = obj.do_get_role_id("service")
	obj.service_r_id=obj.return_value(srid._info)
	print "Admin Role Id: %s" % obj.admin_r_id
	print "Service Role Id: %s" % obj.service_r_id
	
	for item in admin_users:
		uid = obj.do_get_user_id(item)	
		obj.user_id=obj.return_value(uid._info)
		ret=obj.do_role_assignment("admin")
		utils.print_dict(ret._info)

	for item in service_users:
		uid = obj.do_get_user_id(item)	
		obj.user_id=obj.return_value(uid._info)
		ret=obj.do_role_assignment("service")
		utils.print_dict(ret._info)

