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

container_resources = {
  haproxy = {
    cpu          = 0.5
    memory       = "1Gi"
    min_replicas = 1
    max_replicas = 3
    concurrency  = 100
  },
  redis = {
    cpu          = 0.25
    memory       = "0.5Gi"
    min_replicas = 1
    max_replicas = 3
    concurrency  = 10
  },
  wagtail = {
    cpu          = 2
    memory       = "4Gi"
    min_replicas = 1
    max_replicas = 3
    concurrency  = 50
  }
}
