/*
#Parent Filter
1.Project Filter
2.Item Of Work Filter
3.Structure level Name Filter
4.UOM
5.Client UOM
6.Thickness UOM
7.Length/Breadth/Width UOM
8.Project Structure

#child Table Filter (Material Detail)
1.Item Filter

#child Table Filter (labour Detail)
1.Labour 
2.UOM

child Table Filter (Other Charges)
1.Item Filter
*/
/* 
#Parent Function
1.apply_filters()
2.create_quantity_request()
3.create_task()
4.uom_con_factor()
5.add_empty_row()
6.calculate_total_material_and_labour_cost()
7.create_quotation()
8.make_multi_grid()
9.glow_for_button_for_rate(frm)
10.glow_for_button(frm)

#Child Table Function
1.child_table_refresh_bug_fix()
*/

/* 
#Parent Triger
1.to_uom:
2.before_submit
3.setup
4.lifting_percentage
5.is_lifting_percentage
6.total_taxes_and_other_cost
7.net_total
8.total_material_and_labour_cost
9.total_other_taxes_and_charges
10.total_labour_cost
11.total_material_cost 
12.item_of_work
13.project_structure
14.project
15.refresh
16.converted_qty
17.has_conversion
18.rounding_adjustment 
19.additional_discount_percentage 
20.converted_rate 
21.grand_total 
22.lifting_amount
23.callback
24.from_uom
25.estimate_quantity
26.rate_conversion
27.qty_conversion
28.disable_rounded_total
29.uom_conversion_type

#Child Table Triger BOQ Material Detail
1.uom_conversion_factor
2.uom
3.amount
4.rate
5.item_code
6.items_remove
7.item_code

#Child Table Triger BOQ Material Detail
1.uom_con_factor
2.amount
3.rate
4.qty
5.labour
6.uom
7.labour_detail_remove

#Child Table Triger Other Taxes and Charges
1.charges_based_on
2.rate
3.amount
4.total
5.other_taxes_and_charges_remove
*/

// Copyright (c) 2021, Nxweb and contributors
// For license information, please see license.txt
//Filter Functions
function structure_level_filter() {

    var level_list = [];
    frappe.db.get_doc('Project Structure', cur_frm.doc.project_structure).then(doc => {
        doc.structure_level_detail.forEach(i => level_list.push(i.structure_level_name));
    });
    cur_frm.set_query("structure_level_name", function() {
        return {
            filters: [
                ["name", "in", level_list]
            ]
        };
    });
}

function item_of_work_filter() {
    cur_frm.set_query("item_of_work", function(doc) {
        return {
            "filters": {
                "project": cur_frm.doc.project,
                'status': 'Active'
            }
        };
    });
}

function project_structure_filter() {
    cur_frm.set_query("project_structure", function(doc) {
        return {
            "filters": {
                "project": cur_frm.doc.project,
            }
        };
    });
}

function item_filter() {
    cur_frm.fields_dict.items.grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
        var d = locals[cdt][cdn];
        return {
            filters: [
                ['Item', 'nx_item_type', '=', "Material"],
                ['Item', 'disabled', '=', 0]
            ]
        };
    };
}

function labour_filter() {
    cur_frm.fields_dict.labour_detail.grid.get_field('labour').get_query = function(doc, cdt, cdn) {
        var d = locals[cdt][cdn];
        return {
            filters: [
                ['Item', 'nx_item_type', '=', "Labour"],
                ['Item', 'nx_labour_applicable_for', '=', "BOQ"],
                ['Item', 'disabled', '=', 0],
                ['Item', 'nx_project', '=', cur_frm.doc.project]
            ]
        };
    };
}

function project_filter() {
    cur_frm.set_query("project", function(doc) {
        return {
            "filters": {
                "status": 'Open',
            }
        };
    });
}

function child_table_refresh_bug_fix() {
    console.log('child_table_refresh_bug_fix test');
    cur_frm.refresh_field("items");
    cur_frm.refresh_field("labour_detail");
    cur_frm.refresh_field("other_taxes_and_charges");
}

function apply_filters() {
    console.log('apply_filter test');
    project_filter();
    item_of_work_filter();
    project_structure_filter();
    item_filter();
    //labour_filter();
}
//adding Custom Buttons and it's functions
function create_quantity_request() {
    cur_frm.add_custom_button(__("Quantity Request"), function() {
        frappe.route_options = {
            "boq": cur_frm.doc.name,
            "project": cur_frm.doc.project,
            "project_name": cur_frm.doc.project_name,
            "project_structure": cur_frm.doc.project_structure,
            "item_of_work": cur_frm.doc.item_of_work,
            "uom": cur_frm.doc.from_uom
        };
        frappe.new_doc("Quantity Request");
    }, __("Create"));
    cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
}


function create_task() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.work_status === "Not Scheduled") {
        cur_frm.add_custom_button("Task", () => {
            frappe.call({
                method: "construction.construction.doctype.boq.boq.update_task",
                args: {
                    "boq_name": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    }
                }
            });
        }, "Create");
    }
}

function create_quotation() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.boq_type === 'Tender' && cur_frm.doc.billing_status === 'To Quotation') {
        cur_frm.add_custom_button("Quotation", () => {
            frappe.call({
                method: "construction.construction.doctype.boq.boq.create_quotation",
                args: {
                    "boq_name": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    }
                }
            });
        }, "Create");
    }
}
//total calculations
function calculate_total_material_and_labour_cost() {
    cur_frm.set_value('total_material_and_labour_cost', (cur_frm.doc.total_labour_cost + cur_frm.doc.total_material_cost));
}
//add empty first row if child is undefined
function add_empty_row() {
    if (cur_frm.doc.items === undefined) {
        cur_frm.add_child('items');
        cur_frm.refresh_field('items');
    }
    if (cur_frm.doc.labour_detail === undefined) {
        cur_frm.add_child('labour_detail');
        cur_frm.refresh_field('labour_detail');
    }
    if (cur_frm.doc.other_taxes_and_charges === undefined) {
        cur_frm.add_child('other_taxes_and_charges');
        cur_frm.refresh_field('other_taxes_and_charges');
    }
}

function uom_con_factor() {
    cur_frm.set_query("conversion_factor", function(doc) {
        return {
            "filters": {
                "from_uom": cur_frm.doc.uom,
                "to_uom": cur_frm.doc.to_uom
            }
        };
    });
}

function make_multi_grid() {
    const fields = [{
        label: 'Grid',
        fieldtype: 'Table',
        fieldname: 'items',
        fields: [{
            fieldtype: 'Data',
            fieldname: 'grid_name',
            reqd: 1,
            label: __('Grid Name'),
            in_list_view: 1
        }],
    }]
    var d = new frappe.ui.Dialog({
        title: __('Grid Table'),
        fields: fields,
        primary_action: function() {
            var data = d.get_values("items");
            frappe.call({
                'method': 'construction.construction.doctype.boq.boq.make_grids',
                args: {
                    'items': data,
                    'boq_detail': {
                        "project": cur_frm.doc.project,
                        "project_structure": cur_frm.doc.project_structure,
                        "item_of_work": cur_frm.doc.item_of_work,
                        "to_uom": cur_frm.doc.to_uom
                        //"boq": cur_frm.doc.name
                    }
                },
                freeze: true
            });
            d.hide();
        },
        primary_action_label: __('Create')
    });
    d.show();
}
frappe.ui.form.on('BOQ', {
    to_uom: function(frm, doc) {
        if (cur_frm.doc.to_uom) {
            cur_frm.set_value("from_uom", cur_frm.doc.to_uom)
        }
    },
    before_submit: function(frm, doc) {
        if (cur_frm.doc.thickness === 0 || cur_frm.doc.thickness === null) {
            cur_frm.set_df_property("thickness", "hidden", true)
        }
        if (cur_frm.doc.width === 0 || cur_frm.doc.width === null) {
            cur_frm.set_df_property("width", "hidden", true)
        }
    },
    setup: function(frm, doc) {
        apply_filters();
        uom_con_factor();
    },
    refresh: function(frm, doc) {
        if (cur_frm.is_new() === 1) {
            child_table_refresh_bug_fix();
            add_empty_row();
        }
        if (cur_frm.doc.docstatus === 1) {
            create_quantity_request();
        }
        if (cur_frm.doc.thickness === 0 || cur_frm.doc.thickness === null) {
            cur_frm.set_df_property("thickness", "hidden", true)
        }
        if (cur_frm.doc.width === 0 || cur_frm.doc.width === null) {
            cur_frm.set_df_property("width", "hidden", true)
        }
        //cur_frm.add_custom_button("Grid", () => make_multi_grid(), __("Grid"));
        if (cur_frm.doc.project_structure) {
            structure_level_filter();
        }
        create_task();
        create_quotation();
    },
    project: function(frm, doc) {
        if (cur_frm.doc.project === undefined || cur_frm.doc.project === '' || cur_frm.doc.project === null) {
            if (cur_frm.doc.project_structure) {
                cur_frm.set_value('project_structure', null);
            }
            if (cur_frm.doc.item_of_work) {
                cur_frm.set_value('item_of_work', null);
            }
        }
    },
    project_structure: function(frm, doc) {
        if (cur_frm.doc.project_structure) {
            structure_level_filter();
        }
    },
    item_of_work: function(frm, doc) {
        if ((cur_frm.doc.item_of_work === undefined || cur_frm.doc.item_of_work === '' || cur_frm.doc.item_of_work === null) && (cur_frm.doc.doctype === 'BOQ')) {
            if (cur_frm.doc.from_uom) {
                cur_frm.set_value('from_uom', null);
            }
        }
    },
    total_material_cost: function(frm, doc) {
        calculate_total_material_and_labour_cost();
    },
    total_labour_cost: function(frm, doc) {
        calculate_total_material_and_labour_cost();
    },
    total_other_taxes_and_charges: function(frm, doc) {
        cur_frm.set_value('total_taxes_and_other_cost', (cur_frm.doc.total_other_taxes_and_charges + cur_frm.doc.lifting_amount));
        if (cur_frm.doc.is_lifting_percentage === 1) {
            let lifting_amount = ((cur_frm.doc.net_total + cur_frm.doc.total_other_taxes_and_charges) * (cur_frm.doc.lifting_percentage / 100));
            let total_taxes_and_other_cost = cur_frm.doc.total_other_taxes_and_charges + lifting_amount;
            cur_frm.set_value('lifting_amount', lifting_amount);
            cur_frm.set_value('total_taxes_and_other_cost', (cur_frm.doc.total_other_taxes_and_charges + lifting_amount));
        } else if (cur_frm.doc.is_lifting_percentage === 0) {
            cur_frm.set_value('lifting_amount', 0);
            cur_frm.set_value('lifting_percentage', 0);
        }
    },
    total_material_and_labour_cost: function(frm, doc) {
        cur_frm.fields_dict["other_taxes_and_charges"].grid.update_docfield_property("rate", "read_only", 1)
        cur_frm.fields_dict['other_taxes_and_charges'].grid.update_docfield_property('amount', 'read_only', 1)
        cur_frm.set_value('net_total', (cur_frm.doc.total_material_and_labour_cost));
        cur_frm.doc.total_other_taxes_and_charges = 0;
        cur_frm.doc.total_taxes_and_other_cost = 0;
        cur_frm.doc.other_taxes_and_charges.forEach(i => {
            if (i.charges_based_on === "Rate") {
                i.total = ((frm.doc.total_material_and_labour_cost * i.rate) / 100);
                i.amount = 0;
            } else if (i.charges_based_on === "Amount") {
                i.total = i.amount;
                i.rate = 0;
            }
            cur_frm.doc.total_other_taxes_and_charges += i.total;
            cur_frm.doc.total_taxes_and_other_cost = cur_frm.doc.total_other_taxes_and_charges + cur_frm.doc.lifting_amount;
            if (cur_frm.doc.is_lifting_percentage === 1) {
                cur_frm.doc.lifting_amount = ((cur_frm.doc.net_total + cur_frm.doc.total_other_taxes_and_charges) * (cur_frm.doc.lifting_percentage / 100));
                cur_frm.doc.total_taxes_and_other_cost = cur_frm.doc.total_other_taxes_and_charges + cur_frm.doc.lifting_amount;
                //cur_frm.set_value('lifting_amount', ((cur_frm.doc.net_total+cur_frm.doc.total_other_taxes_and_charges) * (cur_frm.doc.lifting_percentage/100)))
            } else {
                cur_frm.set_value('lifting_amount', 0);
            }
        });
        cur_frm.refresh_field("other_taxes_and_charges");
        cur_frm.refresh_field("total_other_taxes_and_charges");
        cur_frm.refresh_field("total_taxes_and_other_cost");
        cur_frm.refresh_field("lifting_amount");
    },
    net_total: function(frm, doc) {
        cur_frm.set_value('grand_total', (cur_frm.doc.net_total + cur_frm.doc.total_taxes_and_other_cost));
    },
    total_taxes_and_other_cost: function(frm, doc) {
        cur_frm.set_value('grand_total', (cur_frm.doc.net_total + cur_frm.doc.total_taxes_and_other_cost));
    },
    is_lifting_percentage: function(frm, doc) {
        if (cur_frm.doc.is_lifting_percentage === 0) {
            cur_frm.set_df_property('lifting_amount', 'read_only', 0)
            cur_frm.set_df_property('lifting_percentage', 'read_only', 1)
            cur_frm.set_df_property('lifting_percentage', 'hidden', 1)
            cur_frm.set_value('lifting_percentage', 0);
        } else if (cur_frm.doc.is_lifting_percentage === 1) {
            cur_frm.set_value('lifting_amount', 0)
            cur_frm.set_df_property('lifting_amount', 'read_only', 1)
            cur_frm.set_df_property('lifting_percentage', 'read_only', 0)
            cur_frm.set_df_property('lifting_percentage', 'hidden', 0)
        }
    },
    lifting_percentage: function(frm, doc) {
        if (cur_frm.doc.is_lifting_percentage === 1) {
            cur_frm.set_value('lifting_amount', ((cur_frm.doc.net_total + cur_frm.doc.total_other_taxes_and_charges) * (cur_frm.doc.lifting_percentage / 100)));
        } else {
            cur_frm.set_value('lifting_amount', 0);
        }
    },
    lifting_amount: function(frm, doc) {
        if (cur_frm.doc.lifting_amount !== 0) {
            cur_frm.set_value('total_taxes_and_other_cost', (cur_frm.doc.total_other_taxes_and_charges + cur_frm.doc.lifting_amount));
        } else if (cur_frm.doc.lifting_amount === 0) {
            cur_frm.set_value('total_taxes_and_other_cost', cur_frm.doc.total_other_taxes_and_charges);
        }
    },
    grand_total: function(frm, doc) {
        if (cur_frm.doc.has_conversion === 0) {
            if (cur_frm.doc.additional_discount_amount) {
                cur_frm.set_value("grand_total_amt", (cur_frm.doc.grand_total - cur_frm.doc.additional_discount_amount))
                cur_frm.set_value("rounded_total", ((cur_frm.doc.grand_total - cur_frm.doc.additional_discount_amount) + cur_frm.doc.rounding_adjustment))
            } else {
                cur_frm.set_value("grand_total_amt", (cur_frm.doc.grand_total))
                cur_frm.set_value("rounded_total", (cur_frm.doc.grand_total))
            }
        }
    },
    converted_rate: function(frm, doc) {
        if (cur_frm.doc.rounding_adjustment) {
            cur_frm.set_value("rounded_total", ((cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount) + cur_frm.doc.rounding_adjustment))
        } else {
            cur_frm.set_value("rounded_total", ((cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount)))
        }
    },
    additional_discount_percentage: function(frm, doc) {
        if (cur_frm.doc.has_conversion === 1) {
            let discount_amt = cur_frm.doc.converted_rate * ((cur_frm.doc.additional_discount_percentage) / 100)
            cur_frm.set_value("additional_discount_amount", discount_amt)
            cur_frm.set_value("amount_after_conversion", (cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount))
            cur_frm.set_value("rounded_total", (cur_frm.doc.amount_after_conversion + cur_frm.doc.rounding_adjustment))
        } else {
            let discount_amt = cur_frm.doc.grand_total * ((cur_frm.doc.additional_discount_percentage) / 100)
            cur_frm.set_value("additional_discount_amount", dis_amt)
            cur_frm.set_value("grand_total_amt", (cur_frm.doc.grand_total - cur_frm.doc.additional_discount_amount))
            cur_frm.set_value("rounded_total", (cur_frm.doc.grand_total_amt + cur_frm.doc.rounding_adjustment))
        }
    },
    rounding_adjustment: function(frm, doc) {
        if (cur_frm.doc.has_conversion === 1) {
            cur_frm.set_value("rounded_total", (cur_frm.doc.amount_after_conversion + cur_frm.doc.rounding_adjustment))
        } else if (cur_frm.doc.has_conversion === 0) {
            cur_frm.set_value("rounded_total", (cur_frm.doc.grand_total_amt + cur_frm.doc.rounding_adjustment))
        }
    },
    has_conversion: function(frm, doc) {
        if (cur_frm.doc.has_conversion === 0) {
            cur_frm.set_value("from_uom", null)
            cur_frm.set_value("additional_discount_percentage", 0)
            cur_frm.set_value("additional_discount_amount", 0)
            cur_frm.set_value("rounding_adjustment", 0)
            cur_frm.set_value("grand_total_amt", cur_frm.doc.grand_total)
            cur_frm.set_value("rounded_total", cur_frm.doc.grand_total)
            cur_frm.set_value("from_uom", cur_frm.doc.to_uom)
        } else if (cur_frm.doc.has_conversion === 1) {
            cur_frm.set_value("from_uom", null)
            cur_frm.set_value("additional_discount_percentage", 0)
            cur_frm.set_value("additional_discount_amount", 0)
            cur_frm.set_value("rounding_adjustment", 0)
            cur_frm.set_value("converted_rate", 0)
            cur_frm.set_value("converted_qty", 0)
        }
    },
    converted_qty: function(frm, doc) {
        glow_for_button();
        glow_for_button_for_rate()
    },



    uom_conversion_type: function(frm, doc) {
        if (cur_frm.doc.uom_conversion_type === "Thickness") {
            cur_frm.toggle_display("conversion_factors", false);
        } else if (cur_frm.doc.uom_conversion_type === "Thickness") {
            cur_frm.toggle_display("thickness", true);
        } else if (cur_frm.doc.uom_conversion_type === "Thickness and Conversion Factor") {
            cur_frm.toggle_display("conversion_factors", true);
        } else if (cur_frm.doc.uom_conversion_type === "Thickness and Conversion Factor") {
            cur_frm.toggle_display("thickness", true);
        } else if (cur_frm.doc.uom_conversion_type === "Conversion") {
            cur_frm.toggle_display("conversion_factors", true);
        } else if (cur_frm.doc.uom_conversion_type === "Conversion") {
            cur_frm.toggle_display("thickness", false);
        }
    },
    disable_rounded_total: function(frm, doc) {
        if (cur_frm.doc.disable_rounded_total === 1) {
            cur_frm.set_df_property("rounding_adjustment", "read_only", 1);
            cur_frm.set_value("rounding_adjustment", 0)
        } else if (cur_frm.doc.disable_rounded_total === 0) {
            cur_frm.set_df_property("rounding_adjustment", "read_only", 0)
        }
    },
    qty_conversion: function(frm, doc) {
        frappe.xcall("construction.construction.doctype.boq.boq.type_converter", {
            "from_uom": cur_frm.doc.from_uom || "",
            "to_uom": cur_frm.doc.to_uom || "",
            "value": cur_frm.doc.est_total_qty || 0,
            "tk_value": cur_frm.doc.thickness || 0,
            "tk_uom": cur_frm.doc.thickness_uom || '',
            "w_value": cur_frm.doc.width || 0,
            "w_uom": cur_frm.doc.width_uom || ""
        }).then(r => {
            console.log(r)
            cur_frm.set_value("converted_qty", r)
        })
    },
    rate_conversion: function(frm, doc) {
        frappe.xcall("construction.construction.doctype.boq.boq.type_converter", {
            "from_uom": cur_frm.doc.from_uom || "",
            "to_uom": cur_frm.doc.to_uom || "",
            "value": cur_frm.doc.grand_total || 0,
            "tk_value": cur_frm.doc.thickness || 0,
            "tk_uom": cur_frm.doc.thickness_uom || "",
            "w_value": cur_frm.doc.width || 0,
            "w_uom": cur_frm.doc.width_uom || ""
        }).then(r => {
            console.log(r)
            cur_frm.set_value("converted_rate", r)
            //cur_frm.set_value("amount_after_conversion",cur_frm.doc.converted_rate)
            if (cur_frm.doc.rounding_adjustment !== null && cur_frm.doc.additional_discount_amount !== null) {
                cur_frm.set_value("amount_after_conversion", (cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount))
                cur_frm.set_value("rounded_total", ((cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount) + cur_frm.doc.rounding_adjustment))
            } else if (cur_frm.doc.rounding_adjustment === null && cur_frm.doc.additional_discount_amount !== null) {
                cur_frm.set_value("amount_after_conversion", (cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount))
                cur_frm.set_value("rounded_total", ((cur_frm.doc.converted_rate - cur_frm.doc.additional_discount_amount)))
            } else if (cur_frm.doc.rounding_adjustment !== null && cur_frm.doc.additional_discount_amount === null) {
                cur_frm.set_value("amount_after_conversion", (cur_frm.doc.converted_rate))
                cur_frm.set_value("rounded_total", ((cur_frm.doc.converted_rate + cur_frm.doc.rounding_adjustment)))
            } else if (cur_frm.doc.rounding_adjustment === null && cur_frm.doc.additional_discount_amount === null) {
                cur_frm.set_value("amount_after_conversion", (cur_frm.doc.converted_rate))
                cur_frm.set_value("rounded_total", (cur_frm.doc.amount_after_conversion))
            }
        })
    },
    estimate_quantity: function(frm, doc) {
        cur_frm.set_value("est_total_qty", cur_frm.doc.estimate_quantity)
    },



    from_uom: function(frm, doc) {
        cur_frm.set_value("additional_discount_percentage", 0)
        cur_frm.set_value("additional_discount_amount", 0)
        cur_frm.set_value("rounding_adjustment", 0)
        cur_frm.set_value("grand_total_amt", cur_frm.doc.grand_total)
        cur_frm.set_value("rounded_total", cur_frm.doc.grand_total)
        cur_frm.set_value("converted_rate", 0)
        cur_frm.set_value("converted_qty", 0)
        cur_frm.set_value("amount_after_conversion", 0)
        cur_frm.set_value("rounding_adjustment", 0)
        cur_frm.set_value("rounded_total", 0)
        var to_uom = cur_frm.doc.to_uom
        var from_uom = cur_frm.doc.from_uom
        var to_spt = to_uom.split(" ")[0]
        var from_spt = from_uom.split(" ")[0]
        var len_to_uom = to_uom.split(" ")["length"]
        var len_from_uom = from_uom.split(" ")["length"]
        console.log(len_from_uom)
        if (len_to_uom === 1) {
            if (from_spt === to_spt) {
                cur_frm.toggle_display("thickness", false)
                cur_frm.toggle_display("width", false)
                cur_frm.toggle_display("thickness_uom", false)
                cur_frm.toggle_display("width_uom", false)
            } else if ((to_spt !== "Cubic") && (from_spt === "Cubic")) {
                cur_frm.toggle_display("thickness", true)
                cur_frm.toggle_display("width", true)
                cur_frm.toggle_display("thickness_uom", true)
                cur_frm.toggle_display("width_uom", true)
            } else if ((to_spt !== "Square") && (from_spt === "Square")) {
                cur_frm.toggle_display("width", true)
                cur_frm.toggle_display("width_uom", true)
            }
        } else if (len_from_uom > 1) {
            if (from_spt === to_spt) {
                cur_frm.toggle_display("thickness", false)
                cur_frm.toggle_display("width", false)
                cur_frm.toggle_display("thickness_uom", false)
                cur_frm.toggle_display("width_uom", false)
            } else if ((len_to_uom !== 1) && (from_spt !== "Cubic") || (from_spt !== "Square")) {
                cur_frm.toggle_display("thickness", true)
                cur_frm.toggle_display("width", true)
                cur_frm.toggle_display("thickness_uom", true)
                cur_frm.toggle_display("width_uom", true)
            }
        } else if (len_from_uom === 1) {
            if (from_spt === to_spt) {
                cur_frm.toggle_display("thickness", false)
                cur_frm.toggle_display("width", false)
                cur_frm.toggle_display("thickness_uom", false)
                cur_frm.toggle_display("width_uom", false)
            } else if ((from_spt !== "Cubic") && (to_spt === "Cubic")) {
                cur_frm.toggle_display("thickness", true)
                cur_frm.toggle_display("width", true)
                cur_frm.toggle_display("thickness_uom", true)
                cur_frm.toggle_display("width_uom", true)
            } else if ((from_spt !== "Square") && (to_spt === "Square")) {
                cur_frm.toggle_display("width", true)
                cur_frm.toggle_display("width_uom", true)
            }
        }
    }

});


frappe.ui.form.on('BOQ Material Detail', {
    item_code: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.item_code) {
            frappe.xcall("construction.construction.doctype.boq.boq.get_item_details", {
                "item": d.item_code
            }).then(r => {
                frappe.model.set_value(cdt, cdn, "uom", r.sales_uom);
                frappe.model.set_value(cdt, cdn, "item_name", r.item_name);
            });
        } else {
            frappe.model.set_value(cdt, cdn, "uom", null);
            frappe.model.set_value(cdt, cdn, "qty", 0);
            frappe.model.set_value(cdt, cdn, "item_name", null);
            frappe.model.set_value(cdt, cdn, "stock_uom", null);
            frappe.model.set_value(cdt, cdn, "rate", 0);
            frappe.model.set_value(cdt, cdn, "uom_conversion_factor", 0);
            frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", 0);
        }

        if (d.item_code) {
            frappe.call({
                method: "construction.construction.doctype.boq.boq.fetch_basic_rate",
                args: {
                    "item": d.item_code,
                    "project": cur_frm.doc.project
                },
                freeze: true,
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, "rate", r.message)
                    }
                    refresh_field('rate');
                }
            });
        }
    },
    qty: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.qty > 0) {
            frappe.model.set_value(cdt, cdn, "amount", (d.qty * d.rate));
            frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", (d.qty * d.uom_conversion_factor));
        } else {
            frappe.model.set_value(cdt, cdn, "amount", 0);
            frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", 0);
        }
    },
    rate: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.qty > 0 && d.rate > 0) {
            frappe.model.set_value(cdt, cdn, "amount", (d.qty * d.rate));
        } else {
            frappe.model.set_value(cdt, cdn, "amount", 0);
        }
    },
    amount: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.amount > 0) {
            let total_material_cost = 0;
            cur_frm.doc.items.forEach(item => {
                total_material_cost += item.amount;
            });
            cur_frm.set_value('total_material_cost', total_material_cost);
            cur_frm.set_value('total_no_of_items', cur_frm.doc.items.length);
            cur_frm.refresh_field('total_material_cost');
            cur_frm.refresh_field("total_no_of_items");
        }
    },
    uom: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.uom) {
            frappe.call({
                method: "construction.construction.doctype.boq.boq.uom_conversion_factor",
                args: {
                    "uom": d.uom || " ",
                    "stock_uom": d.stock_uom || " "
                },
                freeze: true,
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, "uom_conversion_factor", r.message);
                        frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", (d.qty * d.uom_conversion_factor));
                    }
                    refresh_field('uom_conversion_factor');
                }
            });
        }
    },
    uom_conversion_factor: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.uom_conversion_factor > 0) {
            frappe.model.set_value(cdt, cdn, "amount", (d.qty * d.rate));
            frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", (d.qty * d.uom_conversion_factor));
        } else {
            frappe.model.set_value(cdt, cdn, "amount", 0);
            frappe.model.set_value(cdt, cdn, "qty_as_per_stock_uom", 0);
        }
    },


    items_remove: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let total_material_cost = 0
        cur_frm.doc.items.forEach(function(i) {
            total_material_cost += i.amount;
        });
        cur_frm.set_value("total_material_cost", total_material_cost);
        cur_frm.set_value('total_no_of_items', cur_frm.doc.items.length);
    },


});
frappe.ui.form.on('BOQ Labour Detail', {
    labour: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.labour) {
            frappe.xcall("construction.construction.doctype.boq.boq.get_labour_details", {
                "labour": d.labour
            }).then(r => {
                frappe.model.set_value(cdt, cdn, "uom", r.stock_uom);
                frappe.model.set_value(cdt, cdn, "primary_labour", r.primary_labour);
            });
        }
    },
    qty: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.qty > 0) {
            frappe.model.set_value(cdt, cdn, "amount", (d.qty * d.rate));
            frappe.model.set_value(cdt, cdn, "qty_as_stock", (d.qty * d.uom_con_factor));
        } else {
            frappe.model.set_value(cdt, cdn, "amount", 0);
            frappe.model.set_value(cdt, cdn, "qty_as_stock", 0);
        }
    },
    rate: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.rate > 0) {
            frappe.model.set_value(cdt, cdn, "amount", (d.qty * d.rate));
        } else {
            frappe.model.set_value(cdt, cdn, "amount", 0);
        }
    },
    amount: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.amount > 0) {
            let total_labour_cost = 0;
            cur_frm.doc.labour_detail.forEach(item => {
                total_labour_cost += item.amount;
            });
            cur_frm.set_value('total_labour_cost', total_labour_cost);
            cur_frm.set_value('total_no_of_labours', cur_frm.doc.labour_detail.length);
            cur_frm.refresh_field("total_labour_cost");
            cur_frm.refresh_field("total_no_of_labours");
        }
    },
    uom: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.stock_uom) {
            frappe.call({
                method: "construction.construction.doctype.boq.boq.uom_conversion_factor",
                args: {
                    "uom": d.uom,
                    "stock_uom": d.stock_uom
                },
                freeze: true,
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, "uom_con_factor", r.message);
                        frappe.model.set_value(cdt, cdn, "qty_as_stock", (d.qty * d.uom_con_factor))
                    }
                    refresh_field('uom_conversion_factor');
                }
            });
        }
    },
    uom_con_factor: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.uom_con_factor) {
            frappe.model.set_value(cdt, cdn, "qty_as_stock", (d.qty * d.uom_con_factor))
        }
    },
    labour_detail_remove: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let total_labour_cost = 0;
        cur_frm.doc.labour_detail.forEach(item => {
            total_labour_cost += item.amount;
        });
        cur_frm.set_value("total_labour_cost", total_labour_cost);
        cur_frm.set_value('total_no_of_labours', cur_frm.doc.labour_detail.length);
    }

});
frappe.ui.form.on('Other Taxes and Charges', {
    charges_based_on: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.charges_based_on === "Rate") {
            frappe.model.set_value(cdt, cdn, "total", ((frm.doc.total_material_and_labour_cost * d.rate) / 100));
            frappe.model.set_value(cdt, cdn, "amount", 0);
            cur_frm.fields_dict['other_taxes_and_charges'].grid.update_docfield_property('amount', 'read_only', 1)
            cur_frm.fields_dict['other_taxes_and_charges'].grid.update_docfield_property('rate', 'read_only', 0)
        } else if (d.charges_based_on === "Amount") {
            frappe.model.set_value(cdt, cdn, "total", d.amount);
            frappe.model.set_value(cdt, cdn, "rate", 0)
            cur_frm.fields_dict["other_taxes_and_charges"].grid.update_docfield_property("rate", "read_only", 1)
            cur_frm.fields_dict['other_taxes_and_charges'].grid.update_docfield_property('amount', 'read_only', 0)
        } else if (d.charges_based_on === "") {
            cur_frm.fields_dict["other_taxes_and_charges"].grid.update_docfield_property("rate", "read_only", 1)
            cur_frm.fields_dict['other_taxes_and_charges'].grid.update_docfield_property('amount', 'read_only', 1)
        }
    },
    rate: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.charges_based_on === "Rate") {
            frappe.model.set_value(cdt, cdn, "total", ((frm.doc.total_material_and_labour_cost * d.rate) / 100));
        }
    },
    amount: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.charges_based_on === "Amount") {
            frappe.model.set_value(cdt, cdn, "total", d.amount);
        }
    },
    total: function(frm, cdt, cdn) {
        let total_other_taxes_and_charges = 0;
        cur_frm.doc.other_taxes_and_charges.forEach(item => total_other_taxes_and_charges += item.total)
        cur_frm.set_value('total_other_taxes_and_charges', total_other_taxes_and_charges)
        cur_frm.refresh_field("total_other_taxes_and_charges");
    },

    other_taxes_and_charges_remove: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let total_other_taxes_and_charges = 0;
        cur_frm.doc.other_taxes_and_charges.forEach(item => total_other_taxes_and_charges += item.total)
        cur_frm.set_value('total_other_taxes_and_charges', total_other_taxes_and_charges);
    }
});

function glow_for_button(frm) {
    if (cur_frm.doc.from_uom) {
        if (cur_frm.doc.has_conversion === 1) {
            let $add_cls = $('<span id ="forbuttons" class="spinner-grow spinner-grow-sm"></span>');
            cur_frm.fields_dict.qty_conversion.$input_wrapper.find('.btn-default').addClass('btn-primary');
            if ((cur_frm.doc.converted_qty === 0) || (cur_frm.doc.converted_qty === null)) {
                cur_frm.fields_dict.qty_conversion.$input_wrapper.find('.btn-default').append($add_cls);
                frappe.utils.play_sound('alert');
                frappe.show_alert({
                    message: __('Update the Converted Qty and Converted Rate'),
                    indicator: 'orange'
                }, 3);
            }
            if (cur_frm.doc.converted_qty !== 0) {
                document.querySelector("#forbuttons").remove()
            }
        }
    }
}

function glow_for_button_for_rate(frm) {
    if (cur_frm.doc.from_uom) {
        if (cur_frm.doc.has_conversion === 1) {
            let $add_cls = $('<span id ="ratebuttons" class="spinner-grow spinner-grow-sm"></span>');
            cur_frm.fields_dict.rate_conversion.$input_wrapper.find('.btn-default').addClass('btn-primary');
            if ((cur_frm.doc.converted_rate === 0) || (cur_frm.doc.converted_rate === null)) {
                cur_frm.fields_dict.rate_conversion.$input_wrapper.find('.btn-default').append($add_cls);
                frappe.utils.play_sound('alert');
                frappe.show_alert({
                    message: __('Update the Converted Qty and Converted Rate'),
                    indicator: 'orange'
                }, 3);
            }
            if (cur_frm.doc.converted_rate !== 0) {
                document.querySelector("#ratebuttons").remove()
            }
        }
    }
}