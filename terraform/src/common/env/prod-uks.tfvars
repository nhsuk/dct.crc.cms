env            = "prod"
environment    = "production"
location       = "uks"
resource_group = "dct-crccms-rg-prod-uks"

storage = {
  account   = "campaignscrcv3produks"
  container = "campaign-resource-centre-v3-production"
}

deploy_container_apps = true
network_address_space = "10.12.8.0/22"
crc_cms_version       = "1.17.0" # initial version to deploy

dr_deployed = false

container_resources = {
  haproxy = {
    cpu                 = 1
    memory              = "2Gi"
    min_replicas        = 3
    max_replicas        = 6
    concurrent_requests = 500
  },
  redis = {
    cpu                 = 0.25
    memory              = "0.5Gi"
    min_replicas        = 3
    max_replicas        = 6
    concurrent_requests = 100
  },
  wagtail = {
    cpu                 = 2
    memory              = "4Gi"
    min_replicas        = 3
    max_replicas        = 12
    concurrent_requests = 75
  }
}
