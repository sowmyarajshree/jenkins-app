# Copyright (c) 2021, Nxweb and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


def create_boq():
	if frappe.flags.test_events_created:
		return
	doc = frappe.get_doc({
		"doctype":"BOQ",
		"project":"Toyota Showroom",
		"project_name":"Toyota Showroom",
		"project_structure":"Toyota Showroom-service centre",
		"quantity":1,
		"item_of_work":"Toyota Showroom-Plastering work",
		#"item_of_work_name":"Test Brick Work",
		#"iow_type":"Labour Bill",
		"to_uom":"Cubic Foot",
		"from_uom":"Cubic Meter",
		"estimate_quantity":1000,
				#self.grand_total = (self.net_total +self.total_taxes_and_other_cost)
		"items":[
		     {
		         "item_code":"cement",
		         "item_name":"cement",
		         "qty":10,
		         "rate":200
		     }
		     ],
		"labour":[
		     {
		         "labour":"Machinery&curing",
		         "qty":2,
		         "rate":10
		      }     
		      ]
		})
	doc.save()
	frappe.flags.test_events_created = True



class TestBOQ(unittest.TestCase):
	def setUp(self):
		create_boq()
	def tearDown(self):
		frappe.set_user("Administrator")
	def test_event_list(self):
		res = frappe.get_list("BOQ", filters=[["BOQ", "project", "like", "Toyota Showroom%"]], fields=["name", "project"])
		subjects = [r.project for r in res]
		self.assertTrue("Toyota Showroom" in subjects)


		

	



