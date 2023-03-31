from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document



def update_stock_qty_boq_ledger(self,method):
    for i in self.items:
        material_ledger = frappe.db.get_value("BOQ Ledger",{"material_name":i.nx_material_entry_name},["name",'stock_entry_qty'],as_dict=1)
        frappe.db.set_value("BOQ Ledger",material_ledger.name,"stock_entry_qty",(material_ledger.stock_entry_qty + i.qty))



def update_stock_qty_on_cancel(self,method):
   for i in self.items:
        material_ledger = frappe.db.get_value("BOQ Ledger",{"material_name":i.nx_material_entry_name},["name",'stock_entry_qty'],as_dict=1)
        frappe.db.set_value("BOQ Ledger",material_ledger.name,"stock_entry_qty",(material_ledger.stock_entry_qty - i.qty))


def set_expense_account(self,method):
    pass
    '''expense_account = frappe.db.get_value("Construction Settings","construction_settings",'account')
    for i in self.items:
        i.expense_account = expense_account'''
                   
