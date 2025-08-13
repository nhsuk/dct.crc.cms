env            = "prod"
environment    = "production"
location       = "uks"
resource_group = "dct-crccms-rg-prod-uks"

deploy_container_apps = false
network_address_space = "10.12.8.0/22"

aks_origin = {
  firewall_ip_address = "51.11.24.240"
  origin_host_header  = "campaignresources.dhsc.gov.uk"
}
