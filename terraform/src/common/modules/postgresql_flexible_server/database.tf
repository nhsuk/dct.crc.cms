resource "random_password" "administrator_password" {
  length      = 16
  min_special = 1
  min_numeric = 1
  min_upper   = 1
  min_lower   = 1
}

resource "azurerm_postgresql_flexible_server" "database" {
  name                = var.name
  resource_group_name = var.resource_group.name
  location            = var.resource_group.location
  sku_name            = local.database_sku
  version             = "16"

  administrator_login    = "cmsadmin"
  administrator_password = random_password.administrator_password.result

  authentication {
    active_directory_auth_enabled = true
    password_auth_enabled         = true
    tenant_id                     = data.azurerm_client_config.current.tenant_id
  }

  storage_mb        = 32768
  auto_grow_enabled = true

  high_availability {
    mode = "ZoneRedundant"
  }

  geo_redundant_backup_enabled  = true
  public_network_access_enabled = true

  lifecycle {
    # primary and standby zone change when failed over so don't automatically fail back
    ignore_changes = [zone, high_availability[0].standby_availability_zone]
  }
}

resource "azurerm_postgresql_flexible_server" "replica" {
  count = local.database_replica != null ? 1 : 0

  name                = local.database_replica.name
  resource_group_name = local.database_replica.resource_group
  location            = local.database_replica.location
  sku_name            = azurerm_postgresql_flexible_server.database.sku_name
  version             = azurerm_postgresql_flexible_server.database.version

  create_mode      = "Replica"
  source_server_id = azurerm_postgresql_flexible_server.database.id

  administrator_login    = azurerm_postgresql_flexible_server.database.administrator_login
  administrator_password = azurerm_postgresql_flexible_server.database.administrator_password

  authentication {
    active_directory_auth_enabled = true
    password_auth_enabled         = true
    tenant_id                     = data.azurerm_client_config.current.tenant_id
  }

  storage_mb        = azurerm_postgresql_flexible_server.database.storage_mb
  auto_grow_enabled = azurerm_postgresql_flexible_server.database.auto_grow_enabled

  geo_redundant_backup_enabled  = false
  public_network_access_enabled = true

  lifecycle {
    # primary and standby zone change when failed over so don't automatically fail back
    ignore_changes = [zone, high_availability[0].standby_availability_zone]
  }
}

resource "azurerm_postgresql_flexible_server_virtual_endpoint" "database" {
  count = local.database_replica != null ? 1 : 0

  name              = replace(var.resource_group.name, "-rg-", "-vep-")
  source_server_id  = azurerm_postgresql_flexible_server.database.id
  replica_server_id = azurerm_postgresql_flexible_server.replica[0].id
  type              = "ReadWrite"
}

resource "azurerm_postgresql_flexible_server_database" "databases" {
  for_each  = toset(local.databases)
  name      = each.key
  server_id = azurerm_postgresql_flexible_server.database.id
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "firewall_rules" {
  for_each         = local.database_firewall_rules
  name             = each.key
  server_id        = azurerm_postgresql_flexible_server.database.id
  start_ip_address = each.value.start_ip
  end_ip_address   = each.value.end_ip
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "replica_firewall_rules" {
  for_each         = local.replica_firewall_rules
  name             = each.key
  server_id        = azurerm_postgresql_flexible_server.replica[0].id
  start_ip_address = each.value.start_ip
  end_ip_address   = each.value.end_ip
}
