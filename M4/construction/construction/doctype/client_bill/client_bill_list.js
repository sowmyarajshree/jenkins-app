frappe.listview_settings['Client Bill'] = {
  add_fields:["nx_status"],
  get_indicator : function(doc){
    if (doc.nx_status == "Draft"){
      return[__("Draft"), "red" ,"nx_status,=,Draft"];
    }
    else if (doc.nx_status === "Pending"){
      return[__("Pending"), "orange" ,"nx_status,=,Pending"]
    }
    else if (doc.nx_status === "Completed"){
      return[__("Completed"),"green","nx_status,=,Completed"]
    }
    else if (doc.nx_status === "Cancelled"){
      return[__("Cancelled"),"red","nx_status,=,Cancelled"]
    }

  }
};