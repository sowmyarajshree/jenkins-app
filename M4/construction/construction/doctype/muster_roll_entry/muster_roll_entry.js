/* 
#Parent Filter
1.project_filter()

#Parent Function
1.dates()
2.labour_progress_entries()
3.get_item_glow(frm)
4.button_LPE()
5.remove_rounding_adjustment()
6.rm_lpe_get_item_button()
7.button_journal_entry()
8.muster_roll_validation()
9.update_attendance()
10.rm_lpe_get_lpe_from()
11.rm_journal_entry_button()

#child Filter Labour Progress Detail
1.lpe_filters()

#child Function F and F Item
1.get_item_glow(frm)
2.amount_calculation()
3.total_amt()
4.total_hrs()

#child Function Labour Progress Detail
1.function labour_progress_entries()
2.function dates()
3.tot_lpe_hrs()
*/

//Parent Function
function remove_rounding_adjustment() {
    if (cur_frm.doc.manual_rounding === 0) {
        cur_frm.set_value("rounding_adjustment", 0)
    }
}

function tds_validation() {
    let tax_val = cur_frm.doc.total_amount * cur_frm.doc.tax_percentage / 100;
    cur_frm.set_value("tax_amount", tax_val)
    cur_frm.set_value("grand_total", cur_frm.doc.total_amount - tax_val)
    cur_frm.set_value("rounded_total", cur_frm.doc.grand_total)
}

function set_accounting_period() {
    frappe.db.get_value('Accounting Period', {
        'start_date': ['<=', cur_frm.doc.posting_date],
        'end_date': ['>=', cur_frm.doc.posting_date]
    }, ['name']).then(doc => cur_frm.set_value('accounting_period', doc.message.name))
}

function project_filter() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        }
    })
}

function rm_journal_entry_button() {
    if (cur_frm.doc.status === "Completed") {
        cur_frm.remove_custom_button("Journal Entry", "Create")
    }
}

function rm_lpe_get_lpe_from() {
    if (cur_frm.doc.docstatus === 1) {
        cur_frm.remove_custom_button("Labour Progress Entry", "Get LPE From")
    }
}

function button_LPE() {
    if (cur_frm.doc.docstatus !== 1 && cur_frm.doc.status === "Draft") {
        cur_frm.add_custom_button(__('Labour Progress Entry'),
            function() {
                if (cur_frm.doc.project === undefined) {

                    frappe.throw("Enter the project")
                }
                if (cur_frm.doc.muster_roll === undefined) {

                    frappe.throw("Enter the Muster Roll")
                }
                new frappe.ui.form.MultiSelectDialog({
                    doctype: "Labour Progress Entry",
                    target: cur_frm,
                    fields: [{
                       'fieldname': 'muster_roll',
                       'fieldtype': 'Link'
                    }],
                    setters: {
                        project_name: cur_frm.doc.project,
                        posting_date: null               
                    },
                    allow_child_item_selection:1,
                    add_filters_group: 1,
                    child_fieldname:"working_details",
                    child_columns:["muster_roll"],
                    


                    get_query() {
                        return {
                            filters: {
                                docstatus: ["=", 1],
                                status: ["=", "To Prepared and Bill"],
                                labour_type: ["=", "Muster Roll"],
                                muster_roll:["=",cur_frm.doc.muster_roll]


                            }
                        };
                    },
            
                    action(selections) {
                        cur_frm.set_value("labour_progress_details", [])
                        for (let b in selections) {
                            cur_frm.doc.total_lpe_hours = 0
                            frappe.db.get_doc("Labour Progress Entry", selections[b]).then(doc => {
                                cur_frm.set_value("labour_type", doc.labour_type)


                                var child = cur_frm.add_child("labour_progress_details")
                                child.labour_progress_entry = doc.name
                                child.dates = doc.posting_date
                                child.item_code = doc.labour
                                child.project = doc.project
                                child.project_structure = doc.project_structure
                                for (let i of doc.working_details) {
                                    if (i.muster_roll === cur_frm.doc.muster_roll) {
                                        child.working_details_name = i.name
                                        child.total_hrs = i.total_working_hours
                                        cur_frm.doc.total_lpe_hours += child.total_hrs
                                        cur_frm.refresh_field("total_lpe_hours")
                                    }

                                }

                                child.is_primary_labour = doc.is_primary_labour
                                frappe.ui.hide_open_dialog();
                                cur_frm.refresh_field("labour_progress_details")
                            });
                        }

                        if (cur_frm.doc.labour_progress_details[0].labour_progress_entry === undefined) {
                            cur_frm.get_field("labour_progress_details").grid.grid_rows[0].remove
                        }
                        cur_frm.refresh_field("labour_progress_details")


                    }
                });


                setTimeout(() => {
                    if (cur_dialog && frappe.is_mobile() === false) {
                        if (cur_dialog.title === "Select Labour Progress Entries") {
                            console.log("test")
                            cur_dialog.$wrapper.find('.modal-dialog').css("max-width", "70%");
                        }
                    }
                }, 900)
            }, __("Get LPE From"));
    }

}

function lpe_filters() {
    cur_frm.fields_dict["labour_progress_details"].grid.get_field("labour_progress_entry").get_query = function() {
        return {
            filters: [
                ["Labour Progress Entry", "status", "=", "To Prepared and Bill"],
                ["Labour Progress Entry", "docstatus", "=", 1],
                ["Labour Progress Entry", "has_measurement_sheet", "=", "Yes"],
                ["Labour Progress Entry", "labour_type", "=", "Muster Roll"],
                ["Labour Progress Entry", "project_name", "=", cur_frm.doc.project]




            ]
        }
    }
}

function button_journal_entry() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status !== "Completed") {
        cur_frm.add_custom_button("Journal Entry", () => {
            frappe.call({
                method: "construction.construction.doctype.muster_roll_entry.muster_roll_entry.create_journal_entry",
                args: {
                    "docname": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name);

                    }
                }
            })
        }, "Create")
    }

}

function muster_roll_validation() {
    //cur_frm.set_value("labour_progress_details",null)
    cur_frm.set_value("total_lpe_hours", null)
    cur_frm.set_value("f_and_f_details_update", null)
    cur_frm.set_value("total_hours", null)
    cur_frm.set_value("total_amount", null)
}

function update_attendance() {
    const att_field = ["labour_attendance", "date", "labour_attendance", "amount", "labourer", "hours_worked", "rate", "total_person"]

    frappe.call({
        method: "construction.construction.doctype.muster_roll_entry.muster_roll_entry.get_labour_attendance",
        args: {
            "dates": dates(),
            "muster_roll": cur_frm.doc.muster_roll,
            "project": cur_frm.doc.project
        },
        freeze: true,
        callback: function(r) {
            if (r.message) {
                cur_frm.clear_table("f_and_f_details_update")
                $.each(r.message, function(i, d) {
                    var f_and_f_tab = cur_frm.add_child("f_and_f_details_update")
                    for (let i in d) {
                        if (d[i] && in_list(att_field, i)) {
                            f_and_f_tab[i] = d[i]
                        }
                    }
                });
                cur_frm.doc.total_amount = 0
                cur_frm.doc.f_and_f_details_update.forEach(i => {
                    cur_frm.doc.total_amount += i.amount
                })
                cur_frm.refresh_field("total_amount")

                cur_frm.doc.total_hours = 0
                cur_frm.doc.f_and_f_details_update.forEach(i => {
                    cur_frm.doc.total_hours += i.hours_worked
                })
                cur_frm.refresh_field("total_hours")
            }
            cur_frm.refresh_field("f_and_f_details_update")

        }
    })

}
function dates() {
    let dates = []
    cur_frm.doc.labour_progress_details.forEach(i => dates.push(i.dates))
    return dates
}

function amount_calculation() {
    var d = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "amount", ((d.rate / 8) * d.hours_worked))
}

function total_amt_and_total_hrs() {
    cur_frm.doc.total_amount = 0
    cur_frm.doc.total_hours = 0
    cur_frm.doc.f_and_f_details_update.forEach(i => {
        cur_frm.doc.total_amount += i.amount
        cur_frm.doc.total_hours += i.total_hours
    })
    cur_frm.refresh_field("total_amount")
    cur_frm.refresh_field("total_hours")
}

function get_item_glow() {

    cur_frm.fields_dict.update_attendance.$input_wrapper.find('.btn btn-xs btn-default').addClass('btn-xs');
    cur_frm.fields_dict.update_attendance.$input_wrapper.find('.btn btn-xs btn-default').addClass('btn btn-primary');
    frappe.utils.play_sound('chat-notification');

}


frappe.ui.form.on('Muster Roll Entry', {
    manual_rounding: function(frm, doc) {
        remove_rounding_adjustment();
    },
    rounding_adjustment: function(frm, doc) {
        cur_frm.set_value("rounded_total", cur_frm.doc.grand_total + cur_frm.doc.rounding_adjustment)
    },
    tax_percentage: function(frm, doc) {
        tds_validation();
    },

    refresh: function(frm, doc) {
        set_accounting_period();
        project_filter();
        button_LPE();
        lpe_filters();
        button_journal_entry();
        rm_lpe_get_lpe_from();
        rm_journal_entry_button();
        cur_frm.get_field("labour_progress_details").grid.wrapper.find(".grid-add-row").remove();

    },
    muster_roll: function(frm, doc) {
        muster_roll_validation();

    },
    posting_date: function(frm, doc) {
        set_accounting_period();
    },
    update_attendance: function(frm, doc) {
        update_attendance();
        get_item_glow();
    }
});


frappe.ui.form.on('F and F Item', {
    rate: function(frm, cdt, cdn) {
        amount_calculation();
    },
    hours_worked: function(frm, cdt, cdn) {
        amount_calculation();
    },
    amount: function(frm, cdt, cdn) {
        total_amt_and_total_hrs();
    }

});

frappe.ui.form.on('Labour Progress Detail', {
    labour_progress_details_remove: function(frm, cdt, cdn) {
        cur_frm.doc.total_lpe_hours = 0
        cur_frm.doc.labour_progress_details.forEach(i => {
            cur_frm.doc.total_lpe_hours += i.total_hrs
        });
        cur_frm.refresh_field("total_lpe_hours")


    }
})