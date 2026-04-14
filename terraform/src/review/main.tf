module "aca_wagtail" {
  source = "git::https://github.com/nhsuk/dct.terraform-modules.wagtail-container-apps?ref=2.0.1"

  environment                  = local.environment
  org                          = local.org
  app                          = local.app
  app_image                    = "dct/crc-cms:${var.crc_cms_version}"
  haproxy_image                = "dct/haproxy-front-door:1.0.1"
  redis_image                  = "redis:4.0.14-alpine"
  container_registry           = "dctcampaignsacrproduks.azurecr.io"
  healthcheck_path             = "/"
  dev_instance                 = var.dev_instance
  resource_group               = data.azurerm_resource_group.wagtail.name
  container_app_environment_id = data.azurerm_container_app_environment.wagtail.id
  identity_id                  = data.azurerm_user_assigned_identity.wagtail.id
  frontdoor_profile            = data.azurerm_cdn_frontdoor_profile.wagtail
  username                     = var.username
  sha_512_password             = var.sha_512_password #gitleaks:allow not actually the password
  init_args                    = local.init_args
  init_config                  = local.init_config
  init_secrets = [
    for secret in data.azurerm_key_vault_secret.wagtail :
    secret if contains(local.init_secrets, upper(replace(replace(secret.name, "${var.dev_instance}--", ""), "-", "_")))
  ]
  app_config = local.app_config
  app_secrets = [
    for secret in data.azurerm_key_vault_secret.wagtail :
    secret if contains(local.app_secrets, upper(replace(replace(secret.name, "${var.dev_instance}--", ""), "-", "_")))
  ]
  alerts_action_group_id = null
  enable_alerts          = false
  container_resources    = local.container_resources
}
