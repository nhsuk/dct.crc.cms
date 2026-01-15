data "azurerm_subscription" "sub" {
  subscription_id = var.subscription_id
}

resource "azurerm_consumption_budget_subscription" "standard" {
  count           = local.deploy_budget ? 1 : 0
  name            = data.azurerm_subscription.sub.display_name
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = var.dr_deployed ? 800 : 400
  time_grain      = "Monthly"
  time_period {
    start_date = "2026-01-01T00:00:00Z"
    end_date   = "2035-12-31T23:59:59Z"
  }
  notification {
    threshold      = 100
    operator       = "GreaterThan"
    threshold_type = "Forecasted"
    contact_emails = [
      module.config.campaigns_monitoring_email,
      module.config.nhsuk_infra_email,
    ]
  }
  lifecycle {
    create_before_destroy = true
  }
}

import {
  for_each = toset(local.deploy_budget ? [var.subscription_id] : [])
  id       = "/subscriptions/${each.value}/providers/Microsoft.Consumption/budgets/subscription_budget"
  to       = azurerm_consumption_budget_subscription.standard[0]
}