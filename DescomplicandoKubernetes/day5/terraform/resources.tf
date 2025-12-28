resource "mgc_virtual_machine_instances" "this" {
  for_each                 = local.cluster_name
  name                     = each.value.name
  machine_type             = each.value.machine_type
  image                    = local.image
  ssh_key_name             = local.ssh_key_name
  allocate_public_ipv4     = true
  creation_security_groups = [mgc_network_security_groups.this.id]
  availability_zone        = each.value.availability_zone
}

resource "mgc_network_security_groups" "this" {
  name                  = "allow-traffic-k8s"
  description           = "SG for Kubernetes cluster"
  disable_default_rules = false
}

resource "mgc_network_security_groups_rules" "this" {
  for_each          = var.sg_rules
  description       = each.value.description
  direction         = each.value.is_egress == false ? "ingress" : "egress"
  ethertype         = tonumber(each.value.ipv) == 4 || each.value.ipv == 6 ? "IPv${each.value.ipv}" : "ERRO: value not support, use only 4 or 6"
  port_range_min    = tonumber(each.value.port_min)
  port_range_max    = tonumber(each.value.port_max)
  protocol          = each.value.protocol == "tcp" || each.value.protocol == "udp" || each.value.protocol == "icmp" ? each.value.protocol : "ERRO: value not support, use only tcp, udp or icmp"
  remote_ip_prefix  = each.value.source_cidr
  security_group_id = mgc_network_security_groups.this.id
}

resource "mgc_network_security_groups_attach" "this" {
  for_each          = mgc_virtual_machine_instances.this
  security_group_id = local.default_sg_id
  interface_id      = each.value.network_interface_id
}
