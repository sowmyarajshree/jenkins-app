# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
'''def create_events():
	#if frappe.flags.test_events_created:
		#return
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
	      "doctype":"Basic Rate",
	      "project":"FACTORY BUILDING",
		  "project_name":"FACTORY BUILDING",
		  "item_code":"M7.5 RMC",
		  "default_uom":"Nos",
		  "rate":100,
		  "has_tax":1,
		  "item_for":"Material"
		  #"gst":10
	     }).insert()
	doc.submit()
	frappe.flags.test_events_created = True'''

class TestBasicRate(unittest.TestCase):
	pass
	


	'''def setUp(self):
		create_events()

	def tearDown(self):
		frappe.set_user("Administrator")
	def test_event_list(self):
		basic_rate = frappe.get_list("Basic Rate",filters=[["Basic Rate","project","like","FACTORY BUILDING%"]],fields=["name","item_code"])
		sub = [i.item_code for i in basic_rate]
		self.assertTrue("M7.5 RMC" in sub)'''
