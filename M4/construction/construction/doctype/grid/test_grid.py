# Copyright (c) 2022, Nxweb and Contributors
# See license.txt

from __future__ import unicode_literals

import frappe
import unittest

def create_grid():
	if frappe.flags.test_events_created:
		return
	doc = frappe.get_doc({
		"doctype":"Grid",
		"grid_name":"D3-F5",
		"project":"Nxweb"
		})
	doc.save()
	frappe.flags.test_events_created = True



class TestGrid(unittest.TestCase):
	def setUp(self):
		create_grid()
	def tearDown(self):
		frappe.set_user("Administrator")
	def test_event_list(self):
		res = frappe.get_list("BOQ", filters=[["Grid", "project", "like", "Nxweb%"]], fields=["name", "project"])
		subjects = [r.project for r in res]
		self.assertTrue("Nxweb" in subjects)


		

	



