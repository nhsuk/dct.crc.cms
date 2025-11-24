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
    concurrent_requests = 75
  }
}
