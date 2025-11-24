# Serverless URL Shortener com Ansible e AWS

Este projeto é um estudo prático sobre **Infraestrutura como Código (IaC)** e arquitetura **Serverless**. 

O objetivo foi criar um encurtador de URL funcional provisionando 100% da infraestrutura utilizando **Ansible** para orquestrar serviços da AWS (Lambda, DynamoDB e API Gateway).

O projeto provisiona os seguintes recursos:
* **DynamoDB:** Tabela `url-shortener-table` para armazenar o par `short_code` e `long_url`.
* **AWS Lambda:** Duas funções Python:
    * `create-link`: Recebe uma URL e gera um código curto.
    * `redirect-link`: Recebe o código e redireciona (HTTP 302) para o site original.
* **API Gateway:** Interface REST pública configurada via Swagger/OpenAPI para expor as funções.


## Pré-requisitos
* Ansible instalado.
* AWS CLI v2 instalado e configurado (`aws configure`).
* Coleções AWS para Ansible (`ansible-galaxy collection install community.aws amazon.aws`).

###  Obtenha seu ID da conta AWS
Você precisará do seu ID numérico de 12 dígitos. Você pode encontrá-lo no console da AWS ou rodando:
```bash
aws sts get-caller-identity --query Account --output text
