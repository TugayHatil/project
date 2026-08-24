odoo.define('x_project_devir', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');

    var XProjectDevirController = FormController.extend({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            // Custom button logic can be added here
        },
    });

    core.action_registry.add('x_project_devir_form', XProjectDevirController);

    return {
        'XProjectDevirController': XProjectDevirController,
    };
});
