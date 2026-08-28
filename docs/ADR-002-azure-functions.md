# ADR-002: Azure Functions

**Status:** Aceito
**Data:** [2026-08-27]
**Autores:** Fellipe N. Prim

## Contexto

Azure Functions é um serviço de computação serverless da Microsoft Azure. Ele permite executar trechos de código (funções) em resposta a eventos — como um timer agendado, uma mensagem em fila ou uma requisição HTTP — sem que a equipe precise provisionar, configurar ou gerenciar servidores. O serviço escala automaticamente conforme a demanda e cobra apenas pelo tempo efetivo de execução, sem custo quando a função está ociosa.

## Decisão

Adoção do Azure Functions

## Consequências
+ No pipeline da CorpTech, a extração dos dados do Jira Service Management é uma tarefa pontual e periódica — ocorre uma vez por dia, dura poucos minutos e depois não exige nenhum processamento adicional. Manter um servidor dedicado VM ou container sempre ligado para executar esse único trabalho representaria custo fixo desnecessário e sobrecarga de manutenção.

+ O Azure Functions resolve exatamente esse problema: a função Python é disparada por um Timer Trigger no horário configurado, realiza a extração dos dados do Azure SQL mockado, aplica as transformações necessárias e grava os arquivos no Blob Storage — tudo sem intervenção humana e sem infraestrutura permanente. Ao final da execução, o serviço simplesmente para, zerando o custo operacional até o próximo ciclo.

## Alternativas rejeitadas

A alternativa mais direta seria uma Azure Virtual Machine com um script Python agendado via cron. Embora funcional, a VM exige custo fixo mensal (independente do uso), manutenção do sistema operacional, configuração de segurança e monitoramento manual. Para uma tarefa de poucos minutos por dia, isso representa um custo desproporcional e complexidade operacional que o projeto não justifica. O Azure Functions entrega o mesmo resultado com muito menos esforço e custo.

## Links

Link da documentação oficial:
https://learn.microsoft.com/pt-br/azure/azure-functions/functions-overview
