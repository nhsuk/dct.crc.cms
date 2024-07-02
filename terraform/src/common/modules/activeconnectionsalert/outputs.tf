output "postgresql_server_name" {
  value = local.postgresql_server_name
}

output "postgresql_server_id" {
  value = data.azurerm_postgresql_server.postgres_server.id
}