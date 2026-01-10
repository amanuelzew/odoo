/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

// 1. Define the UI Component
class MyCustomClientAction extends Component {
  static template = "real_estate_ads.MyCustomActionTemplate";

  setup() {
    this.message = "Hello from Custom Client Action!";
  }

  onButtonClick() {
    alert("Action Triggered!");
  }
}

// 2. Register the tag in the 'actions' category
registry.category("actions").add("my_custom_tag", MyCustomClientAction);
