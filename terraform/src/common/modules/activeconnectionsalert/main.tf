data "azurerm_postgresql_server" "postgres_server" {
  name                = local.postgresql_server_name
  resource_group_name = local.postgresql_resource_group
}

data "azurerm_resource_group" "postgresql_rg" {
  name = local.postgresql_resource_group
}

