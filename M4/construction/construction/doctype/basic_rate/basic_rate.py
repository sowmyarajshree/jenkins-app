# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class BasicRate(Document):
    
	#def validate(self):
		#self.update_gst_rate() for future enhancement
	def before_save(self):
		self.duplicate_basic_rate()

	def update_gst_rate(self):
		if self.rate != None and self.gst != None:
			gst_rate = (int(self.rate) * int(self.gst)) / 100
			self.gst_rate = int(gst_rate) + int(self.rate)
			if self.rate == 0:
				frappe.throw("Rate Cannot Be Zero")

	def duplicate_basic_rate(self):
		if frappe.db.exists("Basic Rate",{"item_code":self.item_code,"project":self.project,"docstatus":0}):
			frappe.throw(_("Basic Rate {0} Is Already Exist").format(self.item_code))

@frappe.whitelist()
def update_gst_rate(docname,rate,gst):
	gst_rate = (int(rate) * int(gst)) / 100
	gst_rate_actual = int(gst_rate) + int(rate)
	return gst_rate_actual

