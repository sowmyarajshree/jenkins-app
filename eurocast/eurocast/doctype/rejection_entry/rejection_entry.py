# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _
from frappe import utils
from frappe.utils import flt
from frappe.model.document import Document

class RejectionEntry(Document):
	def validate(self):
		self.status = self.get_status()

	def before_save(self):
		self.qty_calculation()

	def before_update_after_submit(self):
		self.get_status_on_update()

#update status based on docstatus
	def get_status(self):
		if self.docstatus == 0:
			status = "Draft"
		elif self.docstatus == 1:
			status = "Submitted"
		elif self.docstatus == 2:
			status = "Cancelled"
		return status

#update status based stock_entry value
	def get_status_on_update(self):
		if self.stock_entry != None:
			self.status = "Completed"
		else:
			self.status = "Submitted"

#calculate item_value and item_weight based on qty
	def qty_calculation(self):
		for d in self.rejection_detail:
			if d.qty:
				d.item_value = flt(d.qty) * flt(d.value)
				d.item_weight = flt(d.qty) * flt(d.weight)


#return rejection entry items as a list and take sum of qty for same item_code
@frappe.whitelist()
def update_items(docname,rejection_entry,nx_source_warehouse):
	if rejection_entry:
		rejection_entry_doc = frappe.get_doc("Rejection Entry",rejection_entry)
		items = []
	for d in rejection_entry_doc.rejection_detail:
		qty = frappe.db.sql("""select sum(qty) as qty, item_code as item_code, parent, sum(item_value) as item_value, sum(item_weight) as item_weight
				from `tabRejection Detail`
				where parent = %s and docstatus = 1 group by item_code""",(rejection_entry_doc.name),as_dict=1)
	for q in qty:
		stock_uom = frappe.get_value("Item",{"item_code":q.item_code},["stock_uom"])
		uom = frappe.get_value("UOM Conversion Detail",{"parent":q.item_code},["uom"])
		conversion_factor = frappe.get_value("UOM Conversion Detail",{"parent":q.item_code},["conversion_factor"])
		items.append({
						"qty": q.qty,
						"item_code": q.item_code,
						"stock_uom": stock_uom,
						"uom": stock_uom,
						"conversion_factor": 1,
						"transfer_qty":q.qty,
						"item_value": q.item_value,
						"item_weight": q.item_weight,
						"source_or_raw_material_": "Source",
						"s_warehouse":nx_source_warehouse
						})
	return items
