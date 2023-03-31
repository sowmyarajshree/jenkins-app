# Copyright (c) 2022, Nxweb and Contributors
# See license.txt

#import frappe
import unittest

import frappe
import unittest
import random
import datetime

class TestDoctype(unittest.TestCase):
    def test_create_and_submit_document(self):
        # get a list of all projects
        projects = frappe.get_all("Project")
        subcontractors =  frappe.get_list("Supplier", {"nx_is_sub_contractor":1})
        labourers = frappe.get_all("Labourer")
        Musters = frappe.get_all("Muster Roll")
         # select a project at random
        project = random.choice(projects)
        subcontractor = random.choice(subcontractors)
        labourer = random.choice(labourers)
        muster = random.choice(Musters)
    # generate a random date
        random_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 365))
        random_time = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(1, 86400))
    # generate a random integer
        random_integer = random.randint(1, 100)
        
        # select the value of the select field at random
        select_field_value = random.choice(["Subcontractor", "Muster Roll"])
        
        # create a new document
        doc = frappe.get_doc({
            "doctype": "Labour Attendance",
            "project": project.name,
            "company": "Nxweb",
            "attendance_type": select_field_value,
            "posting_date": random_date,
            "posting_time": random_time,
            "subcontractor":subcontractor if select_field_value == "Subcontractor" else None,
          
        })
        if select_field_value == 'Subcontractor':
            doc.append("labour_details",{
                "labourer":labourer,
                "qty": random.randint(1, 20)
                })
        '''elif select_field_value == 'Muster Roll':
            doc.append('muster_roll_detail',{
                "muster_roll":muster,
                })'''
        doc.insert()

        # check if the document is created
        self.assertTrue(frappe.db.exists("Labour Attendance", doc.name))

        # submit the document
        doc.submit()

        # check if the document is submitted
        self.assertEqual(frappe.db.get_value("Labour Attendance", doc.name, "docstatus"), 1)

