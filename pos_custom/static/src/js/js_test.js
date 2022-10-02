odoo.define('js_test.main', function (require) { 
     "Use strict";

     const AbstractAction = require('web.AbstractAction');
     console.log(AbstractAction);
     const core = require('web.core');
     const OurAction = AbstractAction.extend({  start: function () {          this.$el.html('hello');      }  });                    

     core.action_registry.add('js_test.action', OurAction);

    });                    
