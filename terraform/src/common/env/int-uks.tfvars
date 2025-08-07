env                       = "int"
environment               = "integration"
location                  = "uks"
long_location             = "uksouth"
resource_group            = "dct-crccms-rg-int-uks"
subscription_id           = "6a1350a9-9b14-4f69-9653-c8ccec15b48e"
storage_account_name      = "campaignsstrgintuks"
storage_account_container = "campaign-resouce-centre-v3-integration"

deploy_container_apps = true
username              = "nhsuk"
network_address_space = "10.5.8.0/22"

aks_origin = {
  firewall_ip_address = "20.49.224.251"
  origin_host_header  = "crc-v3.nhswebsite-dev.nhs.uk"
}
