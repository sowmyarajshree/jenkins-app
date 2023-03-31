# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ItemofWork(Document):
	pass
'''	def validate(self):
		pass
		#self.rename_iow()

	def rename_iow(self):
		if(self.item_of_work != str(self.name.split('-')[1])):
			new_name = frappe.rename_doc('Item of Work',self.name,(self.project+'-'+self.item_of_work),force=True,merge=False,show_alert = True) #rebuild_search=True, This version 13.7 not compatiable for this argument , after update of 13.26  we add this argument
			frappe.db.set_value('Item of Work',new_name,'item_of_work',new_name.split('-')[1])
			#return frappe.msgprint(_(frappe.db.get_value('Item of Work',{'name':new_name},['item_of_work'])))
'''
