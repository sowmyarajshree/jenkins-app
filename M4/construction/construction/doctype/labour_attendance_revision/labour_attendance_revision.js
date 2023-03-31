//Child Table Function
//function for set hours to 4 or 8 if the revised time is half day or full day
function project_filter() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        };
    });
}

function subcontractor_filter() {
    cur_frm.set_query("subcontractor", function(doc) {
        return {
            "filters": {
                "nx_is_sub_contractor": 1
            }
        }
    })
}

function hrs_set_for_half_full_day(frm, cdt, cdn) {
    var d = frappe.get_doc(cdt, cdn);
    frappe.db.get_doc("Construction Settings", "Construction Settings").then(doc => {
        if (d.revised_timing === "Full Day") {
            frappe.model.set_value(cdt, cdn, "hours", doc.full_day);
        } else if (d.revised_timing === "Half Day") {
            frappe.model.set_value(cdt, cdn, "hours", doc.half_day);
        }
    });
}


function remove_add_row() {
    if (cur_frm.doc.revised_type === "Labour Out" && cur_frm.doc.attendance_type === "Muster Roll") {
        cur_frm.get_field("labour_attendance_revision_item_muster").grid.wrapper.find(".grid-add-row").remove();
    }
    if (cur_frm.doc.revised_type === "Labour In" && cur_frm.doc.attendance_type === "Muster Roll") {
        cur_frm.get_field("labour_attendance_revision_item_muster").grid.wrapper.find(".grid-add-row")
    }
}

function labourer_filter() {
    if (cur_frm.doc.attendance_type === "Subcontractor" && cur_frm.doc.revised_type == "Labour Out") {
        let labourer = []
        frappe.db.get_doc("Labour Attendance", cur_frm.doc.labour_attendance).then(lab_att => {
            lab_att.labour_details.forEach(i => {
                labourer.push(i.labourer)
            })
        })
        cur_frm.fields_dict.labour_attendance_revision_item_sub.grid.get_field('labourer').get_query = function() {
            return {
                filters: [
                    ['Labourer', 'name', 'in', labourer]
                ]
            }
        }
    }

}

function muster_roll_filter() {
    if (cur_frm.doc.attendance_type === "Muster Roll" && cur_frm.doc.revised_type == "Labour Out") {
        let muster_roll = []
        frappe.db.get_doc("Labour Attendance", cur_frm.doc.labour_attendance).then(lab_att => {
            lab_att.muster_roll_detail.forEach(i => {
                muster_roll.push(i.muster_roll)
            })
        })
        cur_frm.fields_dict.labour_attendance_revision_item_muster.grid.get_field('muster_roll').get_query = function() {
            return {
                filters: [
                    ['Muster Roll', 'name', 'in', muster_roll]
                ]
            }
        }
    }
    if (cur_frm.doc.attendance_type === "Muster Roll" && cur_frm.doc.revised_type == "Labour In") {
        let muster_roll = []
        frappe.db.get_doc("Labour Attendance", cur_frm.doc.labour_attendance).then(lab_att => {
            lab_att.muster_roll_detail.forEach(i => {
                muster_roll.push(i.muster_roll)
            })
        })
        cur_frm.fields_dict.labour_attendance_revision_item_muster.grid.get_field('muster_roll').get_query = function() {
            return {
                filters: [
                    ['Muster Roll', 'name', 'not in', muster_roll]
                ]
            }
        }
    }
}




frappe.ui.form.on('Labour Attendance Revision', {
    refresh: function(frm, doc) {
        project_filter();
        //remove_add_row();
        labourer_filter();
        muster_roll_filter();
        subcontractor_filter();
        if (cur_frm.doc.attendance_type === "Subcontractor" && cur_frm.doc.revised_type == "Labour In") {
            cur_frm.fields_dict.labour_attendance_revision_item_sub.grid.get_field('labourer').get_query = null
        }
    },
    revised_type: function(frm, doc) {
        if (cur_frm.doc.revised_type === "Labour In" && cur_frm.doc.attendance_type === "Muster Roll") {
            cur_frm.set_value("labour_attendance_revision_item_muster", null)
        }
        if (cur_frm.doc.revised_type === "Labour In" && cur_frm.doc.attendance_type !== "Muster Roll") {
            cur_frm.set_value("labour_attendance_revision_item_sub", null)
        }
        if (cur_frm.doc.revised_type === "Labour Out" && cur_frm.doc.attendance_type !== "Muster Roll") {
            cur_frm.set_value("labour_attendance_revision_item_sub", null)
        }
        labourer_filter();
        muster_roll_filter();
        if (cur_frm.doc.attendance_type === "Subcontractor" && cur_frm.doc.revised_type == "Labour In") {
            cur_frm.fields_dict.labour_attendance_revision_item_sub.grid.get_field('labourer').get_query = null
        }
    }
});



frappe.ui.form.on('Labour Attendance Revision Item Sub', {

    hours: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "total_hours", (d.no_of_person * d.hours));
    },
    no_of_person: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "total_hours", (d.no_of_person * d.hours));
    },
    labour_attendance_revision_item_sub_add: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.db.get_doc("Construction Settings", "Construction Settings").then(doc => {
            console.log(doc.half_day)
            if (d.revised_timing === "Full Day") {
                frappe.model.set_value(cdt, cdn, "hours", doc.full_day);
            } else if (d.revised_timing === "Half Day") {
                frappe.model.set_value(cdt, cdn, "hours", doc.half_day);
            } else if (d.revised_timing === "Custom Hours") {
                frappe.model.set_value(cdt, cdn, "hours", 0);
            }
        });
        refresh_field("labour_attendance_revision_item_sub");
    },

    revised_timing: function(frm, cdt, cdn) {
        hrs_set_for_half_full_day(frm, cdt, cdn);
    }
});


frappe.ui.form.on('Labour Attendance Revision Item Muster', {
    hours: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "total_hours", (d.no_of_person * d.hours));
    },
    no_of_person: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "total_hours", (d.no_of_person * d.hours));
    },
    labour_attendance_revision_item_muster_add: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (cur_frm.doc.revised_timing) {
            erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "labour_attendance_revision_item_muster", "revised_timing");
            frappe.db.get_doc("Construction Settings", "Construction Settings").then(doc => {
                console.log(doc.half_day)
                if (d.revised_timing === "Full Day") {
                    frappe.model.set_value(cdt, cdn, "hours", doc.full_day);
                } else if (d.revised_timing === "Half Day") {
                    frappe.model.set_value(cdt, cdn, "hours", doc.half_day);
                } else if (d.revised_timing === "Custom Hours") {
                    frappe.model.set_value(cdt, cdn, "hours", 0);
                }
            });
        }
        refresh_field("labour_attendance_revision_item_muster");
    },

    revised_timing: function(frm, cdt, cdn) {
        hrs_set_for_half_full_day(frm, cdt, cdn);
    }

});