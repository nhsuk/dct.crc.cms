env            = "prod"
environment    = "production"
location       = "ukw"
resource_group = "dct-crccms-rg-prod-ukw"

deploy_container_apps = false
network_address_space = "10.25.8.0/22"

container_resources = {
  haproxy = {
    cpu                 = 1
    memory              = "2Gi"
    min_replicas        = 2
    max_replicas        = 6
    concurrent_requests = 500
  },
  redis = {
    cpu                 = 0.25
    memory              = "0.5Gi"
    min_replicas        = 2
    max_replicas        = 6
    concurrent_requests = 100
  },
  wagtail = {
    cpu                 = 2
    memory              = "4Gi"
    min_replicas        = 2
    max_replicas        = 12
    concurrent_requests = 50
  }
}
