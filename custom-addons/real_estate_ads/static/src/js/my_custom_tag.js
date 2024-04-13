odoo.define("real_estate_ads.CustomAction", function (require) {
  "use strict";

  const AbstractAction = require("web.AbstractAction");
  const core = require("web.core");

  const CustomAction = AbstractAction.extend({
    template: "CustomActions",
    start: function () {
      console.log("Action Client");
    },
  });

  core.action_registry.add("custom_client_action", CustomAction);
});
