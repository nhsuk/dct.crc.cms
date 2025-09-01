env            = "prod"
environment    = "production"
location       = "uks"
resource_group = "dct-crccms-rg-prod-uks"

storage = {
  account   = "campaignscrcv3produks"
  container = "campaign-resource-centre-v3-production"
}

deploy_container_apps = false
network_address_space = "10.12.8.0/22"
