# Instalando o K8s em BareMetal

## Configurando as VM's

### Desativando o uso de swap no sistema

Primeiro, devemos desativar a utilização de _SWAP_ no sistema. Isso é necessário 
porque o Kubernetes não trabalha bem com o swap ativado:

```bash
sudo swapoff -a
```

### Carregando os módulos do Kernel

Agora, devemos carregar os módulos o kernel necessários para o funcionamento do k8s:

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
```

### Configurando parâmetros do sistema

Em seguida, vamos configurar alguns parâmetros do sistema. Isso garantirá que nosso cluster funcione corretamente:

```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

### Instalando os pacotes do Kubernetes

Hora de instalar os pacotes do Kubernetes! Coisa linda de ai meu Deus! Aqui vamos nós:

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https curl

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

sudo apt-mark hold kubelet kubeadm kubectl
```

## Instalando containerd

Em seguida, vamos instalar o containerd, que são essenciais para nosso ambiente Kubernetes:

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update && sudo apt-get install -y containerd.io

```

### Configurando o containerd

Agora, vamos configurar o containerd para que ele funcione adequadamente com o nosso cluster:

```bash
sudo containerd config default | sudo tee /etc/containerd/config.toml

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl status containerd

```

### Habilitando o serviço do kubelet

Por fim, vamos habilitar o serviço do _kubelet_ para que ele inicie automaticamente com o sistema:

```bash
sudo systemctl enable --now kubelet
```
