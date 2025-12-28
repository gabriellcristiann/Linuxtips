terraform {
  required_version = ">1.0, < 2.0"
  required_providers {
    mgc = {
      source  = "magalucloud/mgc"
      version = "~> 0.41.1"
    }
  }
  backend "s3" {
    bucket                      = "gabs-terraform-tfstate"
    key                         = "study/kubernetes/cluster/terraform.tfstate"
    region                      = "br-se1"
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    endpoints = {
      s3 = "https://br-se1.magaluobjects.com/"
    }
  }
}

provider "mgc" {
  api_key = var.mgc_api_key
  region  = local.region
}

data "mgc_network_security_groups" "this" {}

output "data_instances" {
  description = "Public IP of Instances"
  value = tomap({
    for instance in mgc_virtual_machine_instances.this :
    instance.name => {
      Public_IP  = instance.ipv4
      Private_IP = instance.local_ipv4
    }
  })
}