env            = "stag"
environment    = "staging"
location       = "ukw"
resource_group = "dct-crccms-rg-stag-ukw"

deploy_container_apps = true
username              = "nhsuk"
crc_cms_version       = "1.14.2" # initial version to deploy

network_address_space = "10.20.8.0/22"

container_resources = {
  haproxy = {
    cpu                 = 1
    memory              = "2Gi"
    min_replicas        = 1
    max_replicas        = 3
    concurrent_requests = 500
  },
  redis = {
    cpu                 = 0.25
    memory              = "0.5Gi"
    min_replicas        = 1
    max_replicas        = 3
    concurrent_requests = 100
  },
  wagtail = {
    cpu                 = 2
    memory              = "4Gi"
    min_replicas        = 1
    max_replicas        = 3
    concurrent_requests = 100
  }
}
