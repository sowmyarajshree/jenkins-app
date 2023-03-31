# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and Contributors
# See license.txt
from __future__ import unicode_literals
import frappe
import unittest
def create_eventss():
	if frappe.flags.test_events_created:
		return
	frappe.set_user("Administrator")
	doc = frappe.get_doc({
	"doctype": "Quantity Request",
	"project":"PROJ-0020",
	"project_structure": "Second Floor",
	"item_of_work":"44286-00002",
	"qty":"100",
	"boq":"BOQ00024",
	"request":"Tender Qty",
	"reason":"Test Reason",
	"client_approval":"Yes"
	}).insert()
	doc = frappe.get_doc({
	"doctype": "Quantity Request",
	"project":"PROJ-0020",
	"project_structure": "Second Floor",
	"item_of_work":"1235-00001",
	"qty":"200",
	"boq":"BOQ00021",
	"request":"Tender Qty",
	"reason":"Test Reason1",
	"client_approval":"Yes"
	}).insert()
	doc = frappe.get_doc({
	"doctype": "Quantity Request",
	"project":"PROJ-0022",
	"project_structure": "Second Floor",
	"item_of_work":"23445-00017",
	"qty":"300",
	"boq":"BOQ00023",
	"request":"Tender Qty",
	"reason":"Test Reason2",
	"client_approval":"Yes"
	}).insert()

	frappe.flags.test_events_created = True


class TestQuantityRequest(unittest.TestCase):
	def setUp(self):
		create_eventss()
	def tearDown(self):
		frappe.set_user("Administrator")
	def test_event_list(self):
		res = frappe.get_list("Quantity Request", filters=[["Quantity Request", "project_structure","like", "Second Floor%"]], fields=["name", "project_structure"])
		subjects = [r.project_structure for r in res]
		self.assertTrue("Second Floor" in subjects)
