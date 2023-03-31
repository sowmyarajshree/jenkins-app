frappe.ui.form.on('Grid', {
    refresh: function(frm, doc) {
        apply_project_filter()
        apply_project_structure_filter()
        apply_item_of_work_filter()
        apply_boq_filter()

        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === 'Labour Progress Entry') {
            //cur_frm.set_va lue('project_structure',frappe.get_doc('BOQ',frappe.get_prev_route()[2]).project_structure);
            let doc = frappe.model.get_doc('Labour Progress Entry', frappe.get_prev_route()[2])
            console.log(doc)
            cur_frm.set_value({
                'project': doc.project_name,
                'boq': doc.boq,
                'item_of_work': doc.item_of_work,
                'project_structure': doc.project_structure
            })
        }

    }
})

function apply_project_filter() {
    cur_frm.set_query("project", function() {
        return {
            filters: [
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
                ["Item of Work", "project", "=", cur_frm.doc.project]
            ]
        };
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
        };
    })
}