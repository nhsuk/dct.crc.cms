module "aca_wagtail" {
  source = "git::https://github.com/nhsuk/dct.terraform-modules.wagtail-container-apps?ref=0.2.0"

  environment                  = local.environment
  org                          = local.org
  app                          = local.app
  short_app_name               = local.short_app_name
  app_image                    = "dct/crc-cms:${var.crc_cms_version}"
  container_registry           = "dctcampaignsacrproduks.azurecr.io"
  healthcheck_path             = "/"
  dev_instance                 = var.dev_instance
  resource_group               = data.azurerm_resource_group.wagtail.name
  container_app_environment_id = data.azurerm_container_app_environment.wagtail.id
  identity_id                  = data.azurerm_user_assigned_identity.wagtail.id
  frontdoor_profile            = data.azurerm_cdn_frontdoor_profile.wagtail
  key_vault_id                 = data.azurerm_key_vault.wagtail.id
  username                     = var.username
  sha_512_password             = var.sha_512_password #gitleaks:allow not actually the password
  init_config                  = local.init_config
  init_secrets                 = local.init_secrets
  app_secrets                  = local.app_secrets
  alerts_action_group_id       = data.azurerm_monitor_action_group.action_group.id
}
