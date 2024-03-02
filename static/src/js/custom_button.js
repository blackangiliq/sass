odoo.define('sass.custom_button', function (require) {
    "use strict";

    var ListView = require('web.ListView');

    ListView.include({
        custom_events: _.extend({}, ListView.prototype.custom_events, {
            'click .custom_action': '_onClickCustomAction',
        }),

        _onClickCustomAction: function () {
            // Logic to perform when the custom button is clicked
            // For example, open a wizard or perform a custom action
            // This function will be called when the button is clicked
        },
    });
});
