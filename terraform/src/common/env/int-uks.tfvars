env            = "int"
environment    = "integration"
location       = "uks"
long_location  = "uksouth"
resource_group = "dct-crccms-rg-int-uks"

deploy_container_apps = true
username              = "nhsuk"
network_address_space = "10.5.8.0/22"

aks_origin = {
  firewall_ip_address = "20.49.224.251"
  origin_host_header  = "crc-v3.nhswebsite-dev.nhs.uk"
}

imported_storage_subscription_id = "d5cef883-89a0-4c73-bb50-57e3fdbba0d6"
imported_storage_resource_group  = "dct-search-rg-int-uks"
imported_storage_name            = "campaignscrcv3strgintuks"