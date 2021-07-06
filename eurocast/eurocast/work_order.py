from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils
from frappe.model.mapper import get_mapped_doc
import erpnext.manufacturing.doctype.work_order.work_order

'''@frappe.whitelist()
def create_material_request(source_name, target_doc=None,for_qty=None):
	for_qty = for_qty or json.loads(target_doc).get('for_qty')
	doc = get_mapped_doc('Work Order', source_name, {
		'Work Order': {
			'doctype': 'Material Request',
			'validation': {
				'docstatus': ['=', 1]
			}
		},
		'Work Order Item': {
			'doctype': 'Material Request Item'
		},
	}, target_doc)

	doc.for_qty = for_qty

	return doc'''

#update warehouse from BOM
@frappe.whitelist()
def warehouse(self,method):
	warehouse = frappe.db.get_value("BOM",{"name": self.bom_no},["wip_warehouse"])
	target = frappe.db.get_value("BOM",{"name": self.bom_no},["fg_warehouse"])
	if target != None:
		self.fg_warehouse = target
	if warehouse != None:
		self.wip_warehouse = warehouse

#create Material Request from work_order
@frappe.whitelist()
def create_material_request(docname):
	doc = frappe.get_doc("Work Order", docname)
	doc_item = frappe.get_value("Work Order Item",{"parent":doc.name},["item_code"])
	uom =  frappe.get_value("Item",{"item_code":doc_item},["stock_uom"])
	source_warehouse = frappe.db.get_value("Item Default",{"parent":doc_item},["default_warehouse"])
	for d in doc.required_items:
		docm = frappe.new_doc("Material Request")
		docm.update({
                    "material_request_type" : "Material Transfer",
                    #"production_item"         : doc.production_item,
                    #"work_order_ref_no": docname,
                    #"bom_no": doc.bom_no,
                    "docstatus": 0,
                    #"wip_warehouse": doc.wip_warehouse,
                    "fg_warehouse": doc.fg_warehouse,
					"from_warehouse": source_warehouse
                    #"qty": doc.qty
		})
		docm.append("items",{
                                "item_code"         : d.item_code,
                                "qty"               : d.required_qty,
                                "uom"               : uom,
                                "item_name"         : d.item_name,
                                "stock_uom"         : uom,
                                "description"       : d.description,
								"warehouse"			: doc.fg_warehouse,
								"source_warehouse"	: source_warehouse
		})
		return docm.as_dict()
