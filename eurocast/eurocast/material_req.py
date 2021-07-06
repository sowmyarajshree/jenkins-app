from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.material_request.material_request import MaterialRequest
from erpnext.controllers.status_updater import validate_status


#update status of Material request based on work order produced_qty
@frappe.whitelist()
def update_status(self,method):
    doc = frappe.get_doc("Material Request",self.name)
    value =frappe.db.get_value("Work Order",{"name":self.work_order_ref_no},["produced_qty"])
    if (value == 1):
        self.status = "Transferred"
    doc.save(ignore_permissions=True)
    frappe.db.commit()


#update request_to field value to source_warehouse field in child table
@frappe.whitelist()
def update_warehouse(self,method):
    if self.request_to:
        for d in self.items:
            d.source_warehouse = self.request_to
