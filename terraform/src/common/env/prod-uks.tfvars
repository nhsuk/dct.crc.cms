env            = "prod"
environment    = "production"
location       = "uks"
long_location  = "uksouth"
resource_group = "dct-crccms-rg-prod-uks"

deploy_container_apps = false
network_address_space = "10.12.8.0/22"

aks_origin = {
  firewall_ip_address = "51.11.24.240"
  origin_host_header  = "campaignresources.dhsc.gov.uk"
}

imported_storage_subscription_id = "b03d0d19-f998-49c9-938b-d92bb295e28d"
imported_storage_resource_group  = "dct-search-rg-prod-uks"
imported_storage_name            = "campaignscrcv3produks"