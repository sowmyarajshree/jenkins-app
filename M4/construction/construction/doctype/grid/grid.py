# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re

class Grid(Document):
	def before_insert(self):
		self.validate_duplicate_entry()

	def validate(self):
		self.validate_grid_name()

#validation for duplicate entry not to create multiple times
	def validate_duplicate_entry(self):
		if frappe.db.exists("Grid",{"project":self.project,"grid_name":self.grid_name,"docstatus":0}):
			frappe.throw(_("Grid is Already exists"))

#validation for grid name to restrict special characters
	def validate_grid_name(self):
		if not (bool(re.match("^[A-Za-z0-9-]*$",self.grid_name))):
			frappe.throw(_("Grid name is not valid"))

#renaming the grid name 
	def rename_grid(self):
		if(self.grid_name != str(self.name.split('-')[0])):
			new_name = frappe.rename_doc('Grid',self.name,(self.grid_name+'-'+self.boq),force=True,merge=False,show_alert = True) #rebuild_search=True, This version 13.7 not compatiable for this argument , after update of 13.26  we add this argument
			frappe.db.set_value('Grid',new_name,'grid_name',new_name.split('-')[0])
















