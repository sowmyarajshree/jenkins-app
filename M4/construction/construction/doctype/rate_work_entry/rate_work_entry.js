/*
#Parent Trigger
1.refresh:
2.get_items:
3.update_rate:
4.has_lwo:

#Child Trigger (labour progress Work detail)
1.labour_progress_work_details_remove:
2.amount:
3.rate:
4.lifting_charges:
5.lifting_type:

#Parent Function
1.trigger_on_posting_date()
2.get_lwo(subcontractor, labour_type)
3.apply_project_filter()
4.glow()
5.get_item_glow()
6.apply_subcontractor_filter()
7.apply_accounting_period()

#Child Function 
1.apply_labour_work_filter()

*/
frappe.ui.form.on('Rate Work Entry', {
    has_lwo: function(frm, doc) {
        if (cur_frm.doc.has_lwo === "Yes") {
            cur_frm.fields_dict["labour_progress_work_details"].grid.update_docfield_property("rate", "read_only", 1);

        }
        if (cur_frm.doc.has_lwo === "No") {
            cur_frm.fields_dict["labour_progress_work_details"].grid.update_docfield_property("rate", "read_only", 0);
        }

    },

    refresh: function(frm, doc) {
        if (cur_frm.doc.has_lwo === "Yes") {
            cur_frm.fields_dict["labour_progress_work_details"].grid.update_docfield_property("rate", "read_only", 1);

        }
        if (cur_frm.doc.has_lwo === "No") {
            cur_frm.fields_dict["labour_progress_work_details"].grid.update_docfield_property("rate", "read_only", 0);
        }


        apply_accounting_period();

        if (cur_frm.doc.docstatus === 1) {
            setTimeout(() => {
                cur_frm.remove_custom_button("Labour Progress Entry", "Get Items From")


            }, 10)
        }

        //cur_frm.refresh_field("rate_work_details");
        //cur_frm.refresh_field("labour_progress_work_details");
        if (cur_frm.doc.docstatus !== 1) {
            cur_frm.add_custom_button(__('Labour Progress Entry'),
                function() {
                    if (cur_frm.doc.project === undefined) {
                        get_item_glow();
                        frappe.throw("Enter the Project");
                    }
                    if (cur_frm.doc.subcontractor === undefined) {
                        get_item_glow(frm);
                        frappe.throw("Enter the Subcontractor")
                    }
                    new frappe.ui.form.MultiSelectDialog({
                        doctype: "Labour Progress Entry",
                        target: cur_frm,
                        setters: {
                            project_name: cur_frm.doc.project,
                            subcontractor: cur_frm.doc.subcontractor,
                            posting_date: null,
                            project_structure: null

                        },
                        add_filters_group: 1,

                        get_query() {
                            return {
                                filters: {
                                    docstatus: ["=", 1],
                                    status: ["=", "To Prepared and Bill"],
                                    labour_type: ["=", "Rate Work"],
                                    project_name: ["=", cur_frm.doc.project]




                                }
                            };
                        },
                        action(selections) {
                            for (let b in selections) {
                                frappe.db.get_doc("Labour Progress Entry", selections[b]).then(doc => {
                                    
                                    var subcontractor = doc.subcontractor
                                    var labour_type = doc.labour_type

                                    cur_frm.set_value("is_primary_labour", doc.is_primary_labour)
                                    cur_frm.set_value("project", doc.project_name)

                                    var child = cur_frm.add_child("labour_progress_work_details")
                                    child.labour_progress_entry = doc.name
                                    child.labour_work = doc.labour
                                    if (doc.steel_reinforcement === 1) {
                                        child.qty = doc.total_quantity
                                    } else if (doc.steel_reinforcement === 0) {
                                        child.qty = doc.total_qty
                                    }

                                    child.is_primary_labour = doc.is_primary_labour
                                    child.dates = doc.posting_date
                                    child.project_structure = doc.project_structure
                                    labour_progress_work_details_date_sort();
                                    frappe.ui.hide_open_dialog();
                                    cur_frm.refresh_field("labour_progress_work_details")

                                    
                                    get_lwo(subcontractor, labour_type)


                                });
                            }
                            //cur_frm.clear_table("labour_progress_work_details")
                            /*if (cur_frm.doc.labour_progress_work_details[0].labour_progress_entry === undefined) {
                                cur_frm.get_field("labour_progress_work_details").grid.grid_rows[0].remove()

                            }*/
                            cur_frm.refresh_field("labour_progress_work_details")

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


                }, __("Get From"))
                                       
        };



        if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Bill") {
            cur_frm.add_custom_button("Purchase Invoice", () => {
                frappe.call({
                    method: "construction.construction.doctype.rate_work_entry.rate_work_entry.create_purchase_invoice",
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




                });
            });
        }


        cur_frm.set_query("labour_work_order", function() {
            return {
                filters: [
                    ["Labour Work Order", "project", "=", cur_frm.doc.project],
                    ["Labour Work Order", "status", "=", "Active"],
                    ["Labour Work Order", "labour_type", "=", cur_frm.doc.labour_type],
                    ["Labour Work Order", "subcontractor", "=", cur_frm.doc.subcontractor]
                ]
            };
        });


        if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Bill") {
            cur_frm.add_custom_button("Purchase Invoice", () => {
                frappe.call({
                    method: "construction.construction.doctype.rate_work_entry.rate_work_entry.create_purchase_invoice",
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
                });
            });
        }



        cur_frm.fields_dict["labour_progress_work_details"].grid.get_field("labour_progress_entry").get_query = function() {
            return {
                filters: [
                    ["Labour Progress Entry", "status", "=", "To Prepared and Bill"],
                    ["Labour Progress Entry", "docstatus", "=", 1],
                    ["Labour Progress Entry", "has_measurement_sheet", "=", "Yes"],
                    ["Labour Progress Entry", "labour_type", "=", "Rate Work"],
                    ["Labour Progress Entry", "project_name", "=", cur_frm.doc.project]
                ]
            }
        }

        apply_labour_work_filter();
        apply_project_filter();
        apply_subcontractor_filter();
    },
    posting_date: function(frm, doc) {
        apply_accounting_period();
    },


    update_rate: function(frm, doc) {
        if (cur_frm.doc.docstatus !== 1) {
            //if (cur_frm.doc.total_amount === 0) {
            cur_frm.doc.total_amount = 0;
            cur_frm.doc.labour_progress_work_details.forEach(i => {

                frappe.xcall("construction.construction.doctype.rate_work_entry.rate_work_entry.fetch_labour_work_order_price", {
                    "lwo": cur_frm.doc.labour_work_order,
                    "labourer": i.labour_work,
                    "status": "Active"
                }).then(r => {

                    i.rate = r;
                    i.amount = i.rate * i.qty;
                    cur_frm.doc.total_amount += i.amount

                    cur_frm.refresh_field('labour_progress_work_details');
                    cur_frm.refresh_field('total_amount');


                });

            });
        }
    },
    /*labour_progress_work_details: function(frm, doc){
        labour_progress_work_details_date_sort(frm);
    }*/



    // For future enhancement
    /* get_items: function(frm, doc) {


         if (cur_frm.doc.labour_work_order === " " || cur_frm.doc.labour_work_order === undefined) {
             frappe.throw("Enter the Labour Work Order to fetch the rate");
         }
         cur_frm.set_value('rate_work_details', null);
         cur_frm.doc.labour_progress_work_details.uniqBy(i => i.labour_work).forEach(j => {
             var row = cur_frm.add_child("rate_work_details");
             row.labour_work = j.labour_work;
             row.qty = j.qty;


         });

         cur_frm.doc.total_amount = 0;
         cur_frm.doc.rate_work_details.forEach(i => {
             i.qty = cur_frm.doc.labour_progress_work_details.filter(j => j.labour_work === i.labour_work).reduce((sum, q) => {
                 return sum + q.qty
             }, 0);
             frappe.xcall("construction.construction.doctype.rate_work_entry.rate_work_entry.get_lwo_rate", {
                 "lwo_doc": cur_frm.doc.labour_work_order,
                 "labour_work": i.labour_work,
                 "status": "Active"
             }).then(r => {
                 i.rate = r;
                 i.amount = i.qty * r;
                 cur_frm.doc.total_amount += i.amount


                 cur_frm.refresh_field('rate_work_details');
                 cur_frm.refresh_field('total_amount');

             });
         });
         cur_frm.refresh_field('rate_work_details');
         cur_frm.refresh_field('labour_work_details');

         glow();


     }*/

});

function apply_accounting_period() {
    frappe.db.get_value('Accounting Period', {
        'start_date': ['<=', cur_frm.doc.posting_date],
        'end_date': ['>=', cur_frm.doc.posting_date]
    }, ['name']).then(doc => cur_frm.set_value('accounting_period', doc.message.name));
}

function apply_labour_work_filter() {
    cur_frm.fields_dict["labour_progress_work_details"].grid.get_field("labour_work").get_query = function() {
        return {
            filters: [
                ["Labour", "is_disabled", "=", "0"]
            ]
        }
    }

}

function apply_project_filter() {
    cur_frm.set_query("project", function() {
        return {
            filters: [
                ["Project", "status", "=", "Open"]
            ]
        }
    })
}

function apply_subcontractor_filter() {
    cur_frm.set_query("subcontractor", function(doc) {
        return {
            filters: {
                "nx_is_sub_contractor": 1
            }
        }
    })
}

function get_lwo(subcontractor, labour_type) {
    if (cur_frm.doc.labour_work_order === undefined) {
        frappe.db.get_value("Labour Work Order", {
            "subcontractor": subcontractor,
            "labour_type": labour_type
        }, ["name"]).then(r => {
            cur_frm.set_value("labour_work_order", r.message.name);
            cur_frm.set_value("subcontractor", subcontractor);
            cur_frm.set_value("labour_type", labour_type);
        });

    }
}



frappe.ui.form.on('Labour Progress Work Detail', {
    lifting_type: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.lifting_type === "Percentage") {

            frappe.db.get_doc("Labour Work Order", cur_frm.doc.labour_work_order).then(lwo_doc => {
                lwo_doc.labour_rate_details.forEach(i => {
                    if (i.labour_item === d.labour_work) {
                        let rate_percentage = i.rate / 100
                        frappe.model.set_value(cdt, cdn, "rate", i.rate + rate_percentage)
                    }

                })


            })

        } else {
            frappe.db.get_doc("Labour Work Order", cur_frm.doc.labour_work_order).then(lwo_doc => {
                lwo_doc.labour_rate_details.forEach(i => {
                    if (i.labour_item === d.labour_work) {
                        frappe.model.set_value(cdt, cdn, "rate", i.rate + d.lifting_charges)
                    }
                })
            })
        }

    },
    lifting_charges: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.lifting_type === "Percentage") {
            frappe.db.get_doc("Labour Work Order", cur_frm.doc.labour_work_order).then(lwo_doc => {
                lwo_doc.labour_rate_details.forEach(i => {
                    if (i.labour_item === d.labour_work) {
                        let rate_percentage = (d.lifting_charges / 100) * i.rate
                        console.log(rate_percentage)
                        frappe.model.set_value(cdt, cdn, "rate", i.rate + rate_percentage)
                    }

                })


            })

        } else if (d.lifting_type === "Amount") {
            frappe.db.get_doc("Labour Work Order", cur_frm.doc.labour_work_order).then(lwo_doc => {
                lwo_doc.labour_rate_details.forEach(i => {
                    if (i.labour_item === d.labour_work) {
                        frappe.model.set_value(cdt, cdn, "rate", i.rate + d.lifting_charges)
                    }
                })
            })

        }
    },
    rate: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", d.qty * d.rate)
    },

    amount: function(frm, cdt, cdn) {
        validate_total_amt(frm, cdt, cdn);
    },


    labour_progress_work_details_remove: function(frm, cdt, cdn) {
        validate_total_amt(frm, cdt, cdn);
    }


});


function validate_total_amt(frm, cdt, cdn) {
    cur_frm.doc.total_amount = 0;
    cur_frm.doc.labour_progress_work_details.forEach(i => {
        cur_frm.doc.total_amount += i.amount;
    });
    cur_frm.refresh_field("total_amount")
}

function glow(frm) {
    if (cur_frm.doc.total_amount !== null) {
        cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').addClass('btn btn-primary');
        cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').addClass('btn btn-primary');

        frappe.utils.play_sound('chat-notification');
    }
}

//input-with-feedback form-control bold
function get_item_glow(frm) {

    cur_frm.fields_dict.get_items.$input_wrapper.find('.dropdown-item').addClass('btn btn-primary');

    frappe.utils.play_sound('alert');


}

//Labour Progress Work Details sort by date
function labour_progress_work_details_date_sort(frm){
    cur_frm.doc.labour_progress_work_details = cur_frm.doc.labour_progress_work_details
    .sort((a,b) => (moment(a.dates, "YYYY-MM-DD")-moment(b.dates, "YYYY-MM-DD")));
    cur_frm.refresh_field('labour_progress_work_details');
    console.log("date sorted successfully")
}