module "aca_wagtail" {
  source = "git::https://github.com/nhsuk/dct.terraform-modules.wagtail-container-apps?ref=4f160e44b17f5dd0604240c9477c08d08775ece4"

  # dev container apps get deployed separately to allow for many transient environments
  count = var.deploy_container_apps && var.env != "dev" ? 1 : 0

  environment                       = var.env
  location                          = data.azurerm_resource_group.rg.location
  org                               = local.org
  app                               = local.app
  short_app_name                    = local.short_app_name
  app_image                         = "dct/crc-cms:${var.crc_cms_version}"
  haproxy_image                     = "dct/haproxy-front-door:1.0.1"
  container_registry                = "dctcampaignsacrproduks.azurecr.io"
  healthcheck_path                  = "/"
  resource_group                    = data.azurerm_resource_group.rg.name
  container_app_environment_id      = module.container_app_env[0].container_app_environment_id
  identity_id                       = module.container_app_env[0].identity_id
  frontdoor_profile                 = var.location == "uks" ? module.network_spoke[0].frontdoor : data.azurerm_cdn_frontdoor_profile.frontdoor[0]
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
  dr_origin                         = var.dr_deployed ? data.azurerm_container_app.dr[0].ingress[0].fqdn : null
  container_resources               = var.container_resources
}
