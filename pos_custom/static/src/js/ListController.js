odoo.define('pos_custom.test', function (require) {
    "use strict";

    var ListController = require("web.ListController");
    
    
    var includeDict = {
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.modelName === "product.product") {
                var coa_button = this.$buttons.find('.o_list_button');
                coa_button.on('click', this.proxy('o_button_click'));
            }
        },
        o_button_click: function(e){
          
                var action = {
                    type: 'ir.actions.client',
                    name: 'New Custom View',
                    tag: 'account_group_hierarchy',
                  
                };
                this.do_action(action);
           

    
        }
    };
    ListController.include(includeDict);
    

});
    