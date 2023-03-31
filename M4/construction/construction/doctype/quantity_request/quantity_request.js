// Copyright (c) 2021, Nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quantity Request', {
    refresh: function(frm, doc) {
        apply_project_filter();
        apply_project_structure_filter();
        apply_item_of_work_filter();
        apply_boq_filter();
    }
});

function apply_project_filter() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        }
    })
}

function apply_project_structure_filter() {
    cur_frm.set_query("project_structure", function() {
        return {
            "filters": [
                ["Project Structure", "project", "=", cur_frm.doc.project]
            ]
        }
    })
}

function apply_item_of_work_filter() {
    cur_frm.set_query("item_of_work", function() {
        return {
            "filters": [
                ["Item of Work", "project", "=", cur_frm.doc.project],
                ["Item of Work", "status", "=", "Active"]
            ]
        }
    })
}

function apply_boq_filter() {
    cur_frm.set_query("boq", function() {
        return {
            "filters": [
                ["BOQ", "project", "=", cur_frm.doc.project],
                ["BOQ", "project_structure", "=", cur_frm.doc.project_structure],
                ["BOQ", "item_of_work", "=", cur_frm.doc.item_of_work]
            ]
        }
    })
}