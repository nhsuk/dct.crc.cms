env                       = "stag"
environment               = "staging"
location                  = "uks"
long_location             = "uksouth"
resource_group            = "dct-crccms-rg-stag-uks"
subscription_id           = "4a2822f1-f87c-4ce3-8c8c-3ef1ffdde025"
storage_resource_group    = "dct-crccms-rg-stag-uks"
storage_account_name      = "campaignsstrgstaguks"
storage_account_container = "campaign-resource-centre-v3-staging"

deploy_container_apps = true
username              = "nhsuk"
crc_cms_version       = "1.13.0" # initial version to deploy

network_address_space = "10.8.8.0/22"

aks_origin = {
  firewall_ip_address = "20.49.242.14"
  origin_host_header  = "staging.campaignresources.dhsc.gov.uk"
}
