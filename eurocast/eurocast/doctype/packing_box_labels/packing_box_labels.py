# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import utils
from frappe.model.document import Document

class PackingBoxLabels(Document):
	def validate(self):
		self.update_qty()
		self.update_cus_name()

	def before_submit(self):
		self.update_box_no()

#updating conversion factor in quantity field from Item
	def update_qty(self):
		if self.item:
			doc = frappe.get_doc("Item",self.item)
			for q in doc.uoms:
				for d in self.packing_box_label_item:
					if q.uom == "Box":
						d.quantity = q.conversion_factor


#updating customer name in quantity field from Item
	def update_cus_name(self):
		if self.item:
			doc = frappe.get_doc("Item",self.item)
			for q in doc.customer_items:
				for d in self.packing_box_label_item:
					d.customer_name = q.customer_name

#creating naming series for box no field using autoname
	def update_box_no(self):
		from frappe.model.naming import make_autoname
		for d in self.packing_box_label_item:
			#d.box_no = self.name + "/" + str(d.idx)
			d.box_no = make_autoname(self.box_series)



#retuns customer items as a list
@frappe.whitelist()
def update_items(docname,item):
	items = []
	if item:
		doc = frappe.get_doc("Item",item)
		for i in doc.customer_items:
			items.append({
				"item_code": item,
				"part_no": i.part_no,
				"part_name": i.part_name,
				"material": i.material,
				"drawing_no": i.drawing_no,
				"weight": i.box_gross_weight,
				"customer_name": i.customer_name
			})
		return items


#retuns customer items as a list by getting total_no of boxes
@frappe.whitelist()
def update_items_nos(docname,item,no_of_boxes):
	items = []
	if item:
		doc = frappe.get_doc("Item",item)
		no_of_boxes_ct = int(no_of_boxes)
	for i in doc.customer_items:
		for d in range(no_of_boxes_ct):
			items.append({
				"item_code": item,
				"part_no": i.part_no,
				"part_name": i.part_name,
				"material": i.material,
				"drawing_no": i.drawing_no,
				"weight": i.box_gross_weight,
				"customer_name": i.customer_name
			})
		return items
