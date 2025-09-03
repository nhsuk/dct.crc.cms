env            = "int"
environment    = "integration"
location       = "uks"
resource_group = "dct-crccms-rg-int-uks"

storage = {
  account   = "campaignsstrgintuks"
  container = "campaign-resouce-centre-v3-integration" # existing typo
}

deploy_container_apps = true
username              = "nhsuk"
network_address_space = "10.5.8.0/22"

aks_origin = {
  firewall_ip_address = "20.49.224.251"
  origin_host_header  = "crc-v3.nhswebsite-dev.nhs.uk"
}
