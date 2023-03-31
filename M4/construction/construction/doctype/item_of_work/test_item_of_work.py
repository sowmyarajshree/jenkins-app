from __future__ import unicode_literals
import frappe
import unittest
def create_eventss():
	if frappe.flags.test_events_created:
		return
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
	"doctype":"Item of Work",
	"item_of_work":"Test Brick Work",
	"iow_type":"STEEL WORK",
	"uom":"Nos",
	"project":"FACTORY BUILDING",
	"project_structure":"Fourth Floor"
	}).insert()
	doc.save()
	frappe.flags.test_events_created = True

	

class TestItemOfWork(unittest.TestCase):
	def setUp(self):
		create_eventss()
	def test_event_list(self):
		res = frappe.get_list("Item of Work", filters=[["Item of Work", "project", "like", "FACTORY BUILDING%"]], fields=["name", "project"])
		subjects = [r.project for r in res]
		self.assertTrue("FACTORY BUILDING" in subjects)

