// Copyright (c) 2021, Nxweb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Basic Rate', {
    //for future enhancement
    /*gst: function(frm,doc) {
    	frappe.call({
    		method: "construction.construction.doctype.basic_rate.basic_rate.update_gst_rate",
    		args: {
    			"docname": frm.doc.name,
    			"rate": cur_frm.doc.rate,
    			"gst": cur_frm.doc.gst
    			},
    		freeze: true,
    		callback: function(r){
    			if(r.message) {
    		    frm.set_value("gst_rate", r.message);
    		}
    		refresh_field('gst_rate');
    	}
    });
    },*/
    refresh: function(frm) {
        apply_project_filter();
        apply_item_code_filter();

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

function apply_item_code_filter() {
    cur_frm.set_query("item_code", function() {
        return {
            filters: [
                ["Item", "disabled", "=", "0"],
                ["Item", "nx_item_type", "!=", "BOQ"]
            ]
        }
    })
}