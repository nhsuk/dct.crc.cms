locals {
  database_skus = {
    development = "GP_Standard_D2s_v3" # General Purpose, 2 vCores, 8 GiB RAM
    integration = "GP_Standard_D2s_v3" # General Purpose, 2 vCores, 8 GiB RAM
    staging     = "GP_Standard_D2s_v3" # General Purpose, 2 vCores, 8 GiB RAM
    production  = "GP_Standard_D2s_v3" # General Purpose, 2 vCores, 8 GiB RAM
  }

  database_sku = local.database_skus[var.environment]

  database_firewall_rules = {
    AllowAllAzure = {
      start_ip = "0.0.0.0"
      end_ip   = "0.0.0.0"
    }
  }

  database_replicas = {
    production = {
      name           = "dct-crccms-psql-prod-ukw"
      resource_group = "dct-crccms-rg-prod-ukw"
      location       = "ukwest"
    }
  }

  database_replica = lookup(local.database_replicas, var.environment, null)

  replica_firewall_rules = local.database_replica != null ? local.database_firewall_rules : {}

  databases = [
    "crc"
  ]

  law_name                = var.environment != "prod" ? "nhsuk-law-nonprod-uks" : "nhsuk-law-prod-uks"
  law_resource_group_name = var.environment != "prod" ? "nhsuk-law-rg-nonprod-uks" : "nhsuk-law-rg-prod-uks"
}
