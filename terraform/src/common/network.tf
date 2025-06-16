resource "random_uuid" "akamai_guid" {}

module "network_spoke" {
  source = "git::https://github.com/nhsuk/nhsuk.platform.terraform-modules.network-spoke?ref=0.0.7"

  count = var.deploy_container_apps ? 1 : 0

  location            = data.azurerm_resource_group.rg.location
  environment         = var.env
  org                 = local.org
  app                 = local.app
  resource_group_name = data.azurerm_resource_group.rg.name
  address_space       = [var.network_address_space]

  subnets = {
    "cae" : {
      address_prefixes        = [cidrsubnet(var.network_address_space, 1, 0)],
      route_table_association = true,
      delegations = {
        "delegation" = {
          service_name = "Microsoft.App/environments"
          service_actions = [
            "Microsoft.Network/virtualNetworks/subnets/join/action"
          ]
        }
      }
    }
  }

  create_frontdoor = true
  enable_waf       = var.env != "dev" # Disbale WAF policy for dev
  akamai_guid      = random_uuid.akamai_guid.result
  peer_hub         = var.env != "dev" # Disbale hub network for dev

  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id

  providers = {
    azurerm.hub = azurerm.hub
  }
}
