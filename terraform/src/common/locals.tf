locals {
  common_tags = {
    "cost code"       = "P0406/02"
    "created by"      = "Azure Pipeline"
    "created date"    = "07/03/2024"
    "environment"     = var.environment
    "product owner"   = "Jeni Riordan"
    "requested by"    = "Evan Harris"
    "service-product" = "Campaigns CRC CMS"
    "team"            = "Digital Campaigns"
  }

  scheduler_logic_app_name         = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")
  search_reindex_logic_app_name    = replace(data.azurerm_resource_group.rg.name, "-rg-", "-search-reindex-la-")
  key_vault_name                   = replace(data.azurerm_resource_group.rg.name, "-rg-", "-kv2-")
  log_analytics_workspace_name     = replace(data.azurerm_resource_group.rg.name, "-rg-", "-log-")
  aks_app_insights_name            = replace(data.azurerm_resource_group.rg.name, "-rg-", "-appi-aks-")
  postgres_flex_name               = replace(data.azurerm_resource_group.rg.name, "-rg-", "-psql-")
  postgres_flex_id                 = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.DBforPostgreSQL/flexibleServers/${local.postgres_flex_name}"
  activeconnections_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-la-")
  activeconnections_logic_app_id   = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Logic/workflows/${local.activeconnections_logic_app_name}"
  backup_vault_name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-bv-")
  backup_vault_resource_group_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-vault-rg-")

  secret_names = [
    "alertingWebhook",
    "pubToken",
    "pubEndpoint",
    "searchIndexEndpoint",
    "basicAuth"
  ]

  deploy_database = var.location == "uks" # Only deploy database module for primary regions (replica will be deployed to dr)

  law_name                = var.environment != "production" ? "nhsuk-law-nonprod-uks" : "nhsuk-law-prod-uks"
  law_resource_group_name = var.environment != "production" ? "nhsuk-law-rg-nonprod-uks" : "nhsuk-law-rg-prod-uks"

  org            = "dct"
  app            = "crccms"
  short_app_name = "crc"

  should_import = false

  init_args = [
    "bash",
    "-c",
    "bash ./initializer-entrypoint.sh"
  ]
  init_secrets = [
    "DB_HOST",
    "DB_NAME",
    "DB_PASS",
    "DB_USER",
    "DEBUG",
    "DJANGO_SETTINGS_MODULE",
    "GUNICORN_CMD_ARGS",
    "NOTIFY_DEBUG",
    "PARAGON_API_ENDPOINT",
    "PARAGON_API_KEY",
    "PARAGON_ENCRYPTION_KEY",
    "PARAGON_MOCK",
    "PARAGON_SALT",
    "PARAGON_SIGN_KEY",
    "PRIMARY_HOST",
    "PUBTOKEN",
    "REDIS_URL",
    "REPORTING_ENABLED",
    "REPORTING_ENDPOINT",
    "SECRET_KEY",
    "STATIC_DIR",
    "STATIC_URL",
    "TWO_FA",
    "WAGTAIL_PASSWORD",
    "WAGTAIL_USER",
    "WEB_CONCURRENCY",
  ]
  init_config = {}
  app_secrets = [
    "ADOBE_TRACKING_URL",
    "ALLOWED_HOSTS",
    "AZURE_ACCOUNT_KEY",
    "AZURE_ACCOUNT_NAME",
    "AZURE_CONTAINER",
    "AZURE_CUSTOM_DOMAIN",
    "AZURE_SEARCH_ACCESS_KEY",
    "AZURE_SEARCH_API_HOST",
    "AZURE_SEARCH_API_KEY",
    "AZURE_SEARCH_API_VERSION",
    "AZURE_SEARCH_CONTAINER",
    "AZURE_SEARCH_DELETE_API_HOST",
    "AZURE_SEARCH_DELETE_API_VERSION",
    "AZURE_SEARCH_FACETS",
    "AZURE_SEARCH_PREFIX",
    "AZURE_SEARCH_STORAGE_ACCOUNT_NAME",
    "CAMPAIGNS_EVENT_API_ENDPOINT",
    "COOKIE_CONSENT_CAMPAIGNS",
    "COOKIE_DECLARATION",
    "DB_HOST",
    "DB_NAME",
    "DB_PASS",
    "DB_USER",
    "DEBUG",
    "DJANGO_SETTINGS_MODULE",
    "GUNICORN_CMD_ARGS",
    "MEDIA_DIR",
    "NOTIFY_API_KEY",
    "NOTIFY_DEBUG",
    "PARAGON_API_ENDPOINT",
    "PARAGON_API_KEY",
    "PARAGON_ENCRYPTION_KEY",
    "PARAGON_MOCK",
    "PARAGON_SALT",
    "PARAGON_SIGN_KEY",
    "PHE_PARTNERSHIPS_EMAIL",
    "PRIMARY_HOST",
    "PUBTOKEN",
    "REDIS_URL",
    "REPORTING_ENABLED",
    "REPORTING_ENDPOINT",
    "SECRET_KEY",
    "SECURE_SSL_REDIRECT",
    "STATIC_DIR",
    "STATIC_URL",
    "TWO_FA",
    "WAGTAIL_PASSWORD",
    "WAGTAIL_USER",
    "WEB_CONCURRENCY",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
    "OTEL_SERVICE_NAME",
    "OTEL_RESOURCE_ATTRIBUTES",
    "CSRF_TRUSTED_ORIGIN"
  ]
}
