variable "mgc_api_key" {
  description = "value of the API key for the MGC provider authentication"
  type        = string
  sensitive   = true
}

variable "sg_rules" {
  description = "security group rules to Kubernetes cluster"
  type = map(object({
    description = string
    is_egress   = bool
    ipv         = number
    port_min    = number
    port_max    = number
    protocol    = string
    source_cidr = string
  }))
  default = {
    kube-apiserver = {
      description = "API SERVER"
      is_egress   = false
      ipv         = 4
      port_min    = 6443
      port_max    = 6443
      protocol    = "tcp"
      source_cidr = "0.0.0.0/0"
    },
    kube-components = {
      description = "K8S COMPONENTS"
      is_egress   = false
      ipv         = 4
      port_min    = 10250
      port_max    = 10255
      protocol    = "tcp"
      source_cidr = "0.0.0.0/0"
    },
    node-port = {
      description = "NODE PORT"
      is_egress   = false
      ipv         = 4
      port_min    = 30000
      port_max    = 32767
      protocol    = "tcp"
      source_cidr = "0.0.0.0/0"
    },
    kube-components-etcd = {
      description = "K8S COMPONENTS ETCD"
      is_egress   = false
      ipv         = 4
      port_min    = 2379
      port_max    = 2380
      protocol    = "tcp"
      source_cidr = "0.0.0.0/0"
    },
    cni-weave-net-tcp = {
      description = "CNI WEAVE NET TCP"
      is_egress   = false
      ipv         = 4
      port_min    = 6783
      port_max    = 6783
      protocol    = "tcp"
      source_cidr = "0.0.0.0/0"
    },
    cni-weave-net-udp = {
      description = "CNI WEAVE NET UDP"
      is_egress   = false
      ipv         = 4
      port_min    = 6783
      port_max    = 6783
      protocol    = "udp"
      source_cidr = "0.0.0.0/0"
    },
    cni-weave-net-udp2 = {
      description = "CNI WEAVE NET UDP"
      is_egress   = false
      ipv         = 4
      port_min    = 6784
      port_max    = 6784
      protocol    = "udp"
      source_cidr = "0.0.0.0/0"
    }
  }
}

locals {
  region       = "br-se1"
  image        = "cloud-ubuntu-22.04 LTS"
  ssh_key_name = "mgc-personal"

  cluster_name = {
    control_plane = {
      name              = "control-plane"
      machine_type      = "BV2-4-20"
      availability_zone = "${local.region}-a"
    }
    worker_01 = {
      name              = "worker01"
      machine_type      = "BV2-2-10"
      availability_zone = "${local.region}-b"
    }
    worker_02 = {
      name              = "worker02"
      machine_type      = "BV2-2-10"
      availability_zone = "${local.region}-c"
    }
  }

  k8s_sg_id = one([
    for sg in data.mgc_network_security_groups.this.items : sg.id
    if sg.description == "SG for Kubernetes cluster"
  ])
  default_sg_id = one([
    for sg in data.mgc_network_security_groups.this.items : sg.id
    if strcontains(sg.description, "Padrão")
  ])
}
