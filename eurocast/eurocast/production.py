from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils
import erpnext.manufacturing.doctype.production_plan.production_plan

#update warehouse and wip warehouse in production_plan child table from BOM
@frappe.whitelist()
def prod_plan_item(self,method):
	for d in self.po_items:
		warehouse = frappe.db.get_value("BOM",{"name": d.bom_no},["wip_warehouse"])
		target = frappe.db.get_value("BOM",{"name": d.bom_no},["fg_warehouse"])
		d.warehouse = warehouse
		d.wip_warehouse = target
