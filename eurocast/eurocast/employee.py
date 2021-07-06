from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils
from frappe.utils import (get_first_day,nowdate)


#function to update operation based on department selected
@frappe.whitelist()
def update_department(self,method):
    if(self.department == "PRODUCTION - ECE"):
        self.operation = "PDC"
    if(self.department == "MACHINING - ECE"):
        self.operation = "MACHINING"

#function to set date of joining
@frappe.whitelist()
def validate_doj(self,method):
    date = get_first_day(self.nx_date_of_joining)
    self.date_of_joining = date 