// Copyright (c) 2022, Nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Material Request', {
    refresh: function(frm) {
        apply_project_filter();
        apply_warehouse_filter();
        apply_material_request_detail_filter();

    },
    date: function(frm, doc) {
        if (frm.doc.date) {
            frappe.db.get_value('Accounting Period', {
                'start_date': ['<=', cur_frm.doc.date],
                'end_date': ['>=', cur_frm.doc.date]
            }, ['name']).then(r => cur_frm.set_value('accounting_period', r.message.name));
        }
    }

});

function apply_project_filter() {
    cur_frm.set_query("project", function() {
        return {
            filters: [
                ["Project", "status", "=", "Open"]
            ]
        }
    })
}

function apply_warehouse_filter() {
    cur_frm.set_query("warehouse", function() {
        return {
            filters: [
                ["Warehouse", "disabled", "=", "0"]
            ]
        }
    })
}

function apply_material_request_detail_filter() {
    cur_frm.fields_dict.material_request_details.grid.get_field('item_code').get_query = function() {
        return {
            filters: [
                ["nx_item_type", "!=", "BOQ"]
            ]
        }
    }
}

	

