env            = "stag"
environment    = "staging"
location       = "uks"
resource_group = "dct-crccms-rg-stag-uks"

storage = {
  account   = "campaignsstrgstaguks"
  container = "campaign-resource-centre-v3-staging"
}

deploy_container_apps = true
username              = "nhsuk"
crc_cms_version       = "1.13.0" # initial version to deploy

network_address_space = "10.8.8.0/22"

dr_deployed = true
