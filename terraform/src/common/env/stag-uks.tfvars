env            = "stag"
environment    = "staging"
location       = "uks"
resource_group = "dct-crccms-rg-stag-uks"

deploy_container_apps = true
username              = "nhsuk"
crc_cms_version       = "1.13.0" # initial version to deploy

network_address_space = "10.8.8.0/22"

dr_deployed = true
