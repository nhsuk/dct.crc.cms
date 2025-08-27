module "aca_wagtail" {
  source = "git::https://github.com/nhsuk/dct.terraform-modules.wagtail-container-apps?ref=a573a40b55f087f9fb77354cda2822fd92dcc123"

  # dev container apps get deployed separately to allow for many transient environments
  count = var.deploy_container_apps && var.env != "dev" ? 1 : 0

  environment                       = var.env
  org                               = local.org
  app                               = local.app
  short_app_name                    = local.short_app_name
  app_image                         = "dct/crc-cms:${var.crc_cms_version}"
  container_registry                = "dctcampaignsacrproduks.azurecr.io"
  healthcheck_path                  = "/"
  resource_group                    = data.azurerm_resource_group.rg.name
  container_app_environment_id      = module.container_app_env[0].container_app_environment_id
  identity_id                       = module.container_app_env[0].identity_id
  frontdoor_profile                 = local.frontdoor_profile
  frontdoor_firewall_policy_enabled = true
  frontdoor_firewall_policy_id      = module.network_spoke[0].waf_policy_id
  key_vault_id                      = module.container_app_env[0].key_vault_id
  username                          = var.username
  sha_512_password                  = var.sha_512_password #gitleaks:allow not actually the password
  init_args                         = local.init_args
  init_config                       = local.init_config
  init_secrets                      = local.init_secrets
  app_secrets                       = local.app_secrets
  alerts_action_group_id            = module.container_app_env[0].alerts_action_group_id
}
