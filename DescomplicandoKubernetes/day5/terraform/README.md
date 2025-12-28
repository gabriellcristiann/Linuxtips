# Terraform MGC Kubernetes Cluster

Este _IAC_ cria os recursos necessários para subir um cluster Kubernetes (_BareMetal_) na Magalu Cloud utilizando o provedor MGC do Terraform.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >1.0, < 2.0 |
| <a name="requirement_mgc"></a> [mgc](#requirement\_mgc) | ~> 0.41.1 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_mgc"></a> [mgc](#provider\_mgc) | 0.41.1 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [mgc_network_security_groups.this](https://registry.terraform.io/providers/magalucloud/mgc/latest/docs/resources/network_security_groups) | resource |
| [mgc_network_security_groups_attach.this](https://registry.terraform.io/providers/magalucloud/mgc/latest/docs/resources/network_security_groups_attach) | resource |
| [mgc_network_security_groups_rules.this](https://registry.terraform.io/providers/magalucloud/mgc/latest/docs/resources/network_security_groups_rules) | resource |
| [mgc_virtual_machine_instances.this](https://registry.terraform.io/providers/magalucloud/mgc/latest/docs/resources/virtual_machine_instances) | resource |
| [mgc_network_security_groups.this](https://registry.terraform.io/providers/magalucloud/mgc/latest/docs/data-sources/network_security_groups) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_mgc_api_key"></a> [mgc\_api\_key](#input\_mgc\_api\_key) | value of the API key for the MGC provider authentication | `string` | n/a | yes |
| <a name="input_sg_rules"></a> [sg\_rules](#input\_sg\_rules) | security group rules to Kubernetes cluster | <pre>map(object({<br/>    description = string<br/>    is_egress   = bool<br/>    ipv         = number<br/>    port_min    = number<br/>    port_max    = number<br/>    protocol    = string<br/>    source_cidr = string<br/>  }))</pre> | <pre>{<br/>  "kube-apiserver": {<br/>    "description": "API SERVER",<br/>    "ipv": 4,<br/>    "is_egress": false,<br/>    "port_max": 6443,<br/>    "port_min": 6443,<br/>    "protocol": "tcp",<br/>    "source_cidr": "0.0.0.0/0"<br/>  },<br/>  "kube-components": {<br/>    "description": "K8S COMPONENTS",<br/>    "ipv": 4,<br/>    "is_egress": false,<br/>    "port_max": 10255,<br/>    "port_min": 10250,<br/>    "protocol": "tcp",<br/>    "source_cidr": "0.0.0.0/0"<br/>  },<br/>  "kube-components-etcd": {<br/>    "description": "K8S COMPONENTS ETCD",<br/>    "ipv": 4,<br/>    "is_egress": false,<br/>    "port_max": 2380,<br/>    "port_min": 2379,<br/>    "protocol": "tcp",<br/>    "source_cidr": "0.0.0.0/0"<br/>  },<br/>  "node-port": {<br/>    "description": "NODE PORT",<br/>    "ipv": 4,<br/>    "is_egress": false,<br/>    "port_max": 32767,<br/>    "port_min": 30000,<br/>    "protocol": "tcp",<br/>    "source_cidr": "0.0.0.0/0"<br/>  }<br/>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_data_instances"></a> [data\_instances](#output\_data\_instances) | Public IP of Instances |
