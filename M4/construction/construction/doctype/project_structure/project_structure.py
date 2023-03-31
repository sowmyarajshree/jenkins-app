# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.rename_doc import rename_doc

class ProjectStructure(Document):
	def after_insert(self):
		self.update_project_structure_in_project()

	#def before_save(self):
		#self.validate_structure_level()

	def validate(self):
		self.validate_duplicate_structure_lvl()
		#self.validate_structure_level()
		#self.rename_ps() for future


	def update_project_structure_in_project(self):
		if(frappe.db.count('Project Structure',self.name) == 1):
			project_doc = frappe.get_doc('Project',self.project)
			project_doc.append("project_structure_detail",{
				"project_structure":self.name
			})
			frappe.db.commit()
			project_doc.save(ignore_permissions=True)
			frappe.msgprint(_("Project Structure Added Successfully in Project"))

	def validate_structure_level(self):
		if self.has_level == 1:
			for i in self.structure_level_detail:
				if (frappe.db.exists("BOQ",{"structure_level_name":i.structure_level_name,"project":self.project,"project_structure":self.name,"docstatus":["!=",2]})):
					frappe.throw("Cannot remove the Structure Level")



	def rename_ps(self):
		if(self.project_structure != str(self.name.split('-')[0])):
			new_name = frappe.rename_doc('Project Structure',self.name,(self.project_structure+'-'+self.project),force=True,merge=False,show_alert = True) #rebuild_search=True, This version 13.7 not compatiable for this argument , after update of 13.26  we add this argument
			frappe.db.set_value('Project Structure',new_name,'project_structure',new_name.split('-')[0])
			self.reload()
			#return frappe.msgprint(_(frappe.db.get_value('Project Structure',{'name':new_name},['project_structure'])))

	"""def validate_duplicate_structure_lvl(self):
		if self.has_level ==1:
			structure_lvl = [i.structure_level_name for i in self.structure_level_detail]
			if len(set(structure_lvl)) != len(structure_lvl):
					frappe.throw(" Same Structure Level Name Exists Multiple Times in Structure Level Detail")"""

	def validate_duplicate_structure_lvl(self):
		if self.has_level ==1:
			structure_lvl = []
			for i in self.structure_level_detail:
				if  i.structure_level_name not in structure_lvl:
					structure_lvl.append(i.structure_level_name)
				else :
					frappe.throw(" Same Structure Level Name Exists Multiple Times in Structure Level Detail")





