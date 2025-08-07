# Campaigns CMS Terraform

This is the terraform to deploy resources to support the Campaigns CMS.

The pipeline runs unit tests, validation and a Trivy scan for configuration issues.

There are currently no resources deployed.

## Plan

To run a local plan, you can initialise and plan for the target environment, for example dev:

```sh
export ENVIRONMENT="dev"
export REGION="uks"

terraform init \
  -backend-config=resource_group_name=dct-crccms-platform-rg-$ENVIRONMENT-$REGION \
  -backend-config=storage_account_name=crccmstfst$ENVIRONMENT$REGION

terraform plan -var-file env/dev-uks.tfvars
```

## Unit test

```sh
terraform test -var-file tests/test.tfvars
```
