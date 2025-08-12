# Campaign Resource Centre Terraform

This is the terraform to deploy resources to support the Campaign Resource Centre.

The pipeline runs unit tests, validation and a Trivy scan for configuration issues.

## Plan

To run a local plan, you can initialise and plan for the target environment, for example dev:

```sh
export ENVIRONMENT="dev"
export REGION="uks"
az account set --subscription "dct-crccms-$ENVIRONMENT"
export ARM_SUBSCRIPTION_ID=$(az account show | jq -r .id)

terraform init \
  -backend-config=resource_group_name=dct-crccms-platform-rg-$ENVIRONMENT-$REGION \
  -backend-config=storage_account_name=crccmstfst$ENVIRONMENT$REGION

terraform plan -var-file env/dev-uks.tfvars
```

## Unit test

```sh
terraform test -var-file tests/test.tfvars
```
