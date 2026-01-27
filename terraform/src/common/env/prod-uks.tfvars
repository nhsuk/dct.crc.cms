env             = "prod"
environment     = "production"
location        = "uks"
resource_group  = "dct-crccms-rg-prod-uks"
subscription_id = "984dd01f-f3aa-4fa8-ba8a-e804f38e49d0"

storage = {
  account   = "campaignscrcv3produks"
  container = "campaign-resource-centre-v3-production"
}

deploy_container_apps = true
network_address_space = "10.12.8.0/22"
crc_cms_version       = "1.17.0" # initial version to deploy

dr_deployed = true

container_resources = {
  haproxy = {
    cpu          = 1
    memory       = "2Gi"
    min_replicas = 3
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
    min_replicas = 3
    max_replicas = 12
    concurrency  = 75
  }
}
