resource "random_uuid" "akamai_guid" {}

module "network_spoke" {
  source = "git::https://github.com/nhsuk/nhsuk.platform.terraform-modules.network-spoke?ref=0.0.10"

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
      nsg_rules = {
        Allow80Inbound = {
          priority                   = 100
          direction                  = "Inbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "80"
          source_address_prefix      = "*"
          destination_address_prefix = "*"
        },
        Allow31080Inbound = {
          priority                   = 110
          direction                  = "Inbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "31080"
          source_address_prefix      = "*"
          destination_address_prefix = "*"
        },
        Allow443Inbound = {
          priority                   = 120
          direction                  = "Inbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "*"
        },
        Allow31443Inbound = {
          priority                   = 130
          direction                  = "Inbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "31443"
          source_address_prefix      = "*"
          destination_address_prefix = "*"
        },
        AllowAzureLoadBalancerInbound = {
          priority                   = 140
          direction                  = "Inbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "30000-32767"
          source_address_prefix      = "AzureLoadBalancer"
          destination_address_prefix = "*"
        },
        AllowACROutbound = {
          priority                   = 150
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "MicrosoftContainerRegistry"
        },
        AllowAzureFrontDoorOutbound = {
          priority                   = 160
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "AzureFrontDoor.FirstParty"
        },
        AllowAADOutbound = {
          priority                   = 170
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "AzureActiveDirectory"
        },
        AllowDNSOutbound = {
          priority                   = 180
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "53"
          source_address_prefix      = "*"
          destination_address_prefix = "168.63.129.16"
        },
        AllowStorageUKSOutbound = {
          priority                   = 190
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "Storage.uksouth"
        }
        AllowStorageUKWOutbound = {
          priority                   = 200
          direction                  = "Outbound"
          access                     = "Allow"
          protocol                   = "Tcp"
          source_port_range          = "*"
          destination_port_range     = "443"
          source_address_prefix      = "*"
          destination_address_prefix = "Storage.ukwest"
        }
      }
    }
  }

  create_frontdoor = var.location == "uks" ? true : false # only deploy the front door to primary region
  enable_waf       = var.env != "dev"                     # disable WAF policy for dev
  akamai_guid      = random_uuid.akamai_guid.result
  peer_hub         = var.env != "dev" # disable hub network for dev

  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id

  providers = {
    azurerm.hub = azurerm.hub
  }
}
