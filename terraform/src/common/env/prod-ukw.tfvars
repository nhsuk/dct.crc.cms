env            = "prod"
environment    = "production"
location       = "ukw"
resource_group = "dct-crccms-rg-prod-ukw"

deploy_container_apps = true
network_address_space = "10.25.8.0/22"
crc_cms_version       = "1.17.0" # initial version to deploy

container_resources = {
  haproxy = {
    cpu          = 1
    memory       = "2Gi"
    min_replicas = 2
    max_replicas = 6
    concurrency  = 500
  },
  redis = {
    cpu          = 0.25
    memory       = "0.5Gi"
    min_replicas = 1
    max_replicas = 6
    concurrency  = 100
  },
  wagtail = {
    cpu          = 2
    memory       = "4Gi"
    min_replicas = 2
    max_replicas = 12
    concurrency  = 75
  }
}
