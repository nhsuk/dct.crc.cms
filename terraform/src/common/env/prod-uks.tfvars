env                       = "prod"
environment               = "production"
location                  = "uks"
long_location             = "uksouth"
resource_group            = "dct-crccms-rg-prod-uks"
subscription_id           = "1e543650-5458-44ea-a3b1-35a6d0d92cc9"
storage_resource_group    = "dct-crccms-rg-prod-uks"
storage_account_name      = "campaignscrcv3produks"
storage_account_container = "campaign-resource-centre-v3-production"

deploy_container_apps = false
network_address_space = "10.12.8.0/22"

aks_origin = {
  firewall_ip_address = "51.11.24.240"
  origin_host_header  = "campaignresources.dhsc.gov.uk"
}
