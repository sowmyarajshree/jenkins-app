frappe.listview_settings["Basic Rate"] = {
  refresh: function(frm) {
   cur_list.page.fields_dict["project"].get_query = function(doc){
        return{
            filters:[
                    ["Project","status","=","Open"]
                ]
        }
      }
      cur_list.page.fields_dict["item_code"].get_query = function(doc){
        return{
            filters:[
                    ["Item","nx_item_type","!=","BOQ"]
                ]
        }
      }
	}
}