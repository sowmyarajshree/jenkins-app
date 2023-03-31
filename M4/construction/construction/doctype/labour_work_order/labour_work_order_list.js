frappe.listview_settings["Labour Work Order"] = {
  refresh: function(frm) {
   cur_list.page.fields_dict["project"].get_query = function(doc){
        return{
            filters:[
                    ["Project","status","=","Open"]
                ]
        }
      }
	}
}