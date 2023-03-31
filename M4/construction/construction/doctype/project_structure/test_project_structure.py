from __future__ import unicode_literals

import frappe
import unittest
def create_eventss():
	if frappe.flags.test_events_created:
		return
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
	"doctype": "Project Structure",
	"project_structure": "Test Basement1"
	}).insert()
	doc = frappe.get_doc({
	"doctype": "Project Structure",
	"project_structure": "Test firstFloor2"
	}).insert()
	doc = frappe.get_doc({
	"doctype": "Project Structure",
	"project_structure": "Test SecondFloor3"
	}).insert()

	frappe.flags.test_events_created = True

class TestProjectStructure(unittest.TestCase):
	def setUp(self):
		create_eventss()
	def tearDown(self):
		frappe.set_user("Administrator")
	def test_event_list(self):
		res = frappe.get_list("Project Structure", filters=[["Project Structure", "project_structure","like", "Test%"]], fields=["name", "project_structure"])
		subjects = [r.project_structure for r in res]
		self.assertTrue("Test SecondFloor3" in subjects)
