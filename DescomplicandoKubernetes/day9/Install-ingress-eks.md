# Instalando o Ingress Nginx no EKS

Antes de mais nada, precisamos ter um cluster EKS rodando, para isso, podemos utilizar o _eksctl_, que é uma ferramenta de linha de comando para criar e gerenciar clusters EKS.

```bash
eksctl create cluster \
    --name=eks-cluster \
    --region=us-east-1 \
    --nodegroup-name=eks-cluster-nodegroup \
    --node-type=t3.medium \
    --nodes=2 \
    --nodes-min=1 \
    --nodes-max=3 \
    --managed
```
Para fazermos a instalação do Ingress Controller no EKS, podemos seguir os mesmos passos que fizemos para o Kind trocando apenar a _URL_ do repositório do _nginx_.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.3/deploy/static/provider/aws/deploy.yaml
```
