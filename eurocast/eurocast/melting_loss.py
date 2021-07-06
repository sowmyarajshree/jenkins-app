from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils
from frappe.model.mapper import get_mapped_doc
import erpnext.stock.doctype.stock_entry.stock_entry


#update melting_loss value based on bom_no
@frappe.whitelist()
def calculate_melting_loss(self,method):
     val = frappe.db.get_value("Melting Loss",{"bom_no": self.bom_no},["melting_loss"])
     if val:
         self.melting_loss = val
