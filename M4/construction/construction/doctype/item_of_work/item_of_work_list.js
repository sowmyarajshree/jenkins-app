frappe.listview_settings["Item of Work"] = {
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