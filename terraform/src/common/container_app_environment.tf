module "container_app_env" {
  source = "git::https://github.com/nhsuk/dct.terraform-modules.container-app-env?ref=1.0.1"

  count = var.deploy_container_apps ? 1 : 0

  location                   = data.azurerm_resource_group.rg.location
  environment                = var.env
  resource_group             = var.resource_group
  subnet_id                  = one([for subnet in module.network_spoke[0].vnet.subnet : subnet if strcontains(subnet.name, "cae")]).id
  org                        = local.org
  app                        = local.app
  short_app_name             = local.short_app_name
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id

  providers = {
    azurerm.law = azurerm.law
  }
}
