# Justificativa Tecnológica — CorpTech ITSM Analytics

> **Projeto:** Pipeline de Dados para Métricas de ITSM  
> **Disciplina:** TAPR — Tópicos Avançados em Programação  
> **Atividade:** AV1 | 1º Bimestre 2026  
> **Ferramenta de Visualização Escolhida:** Power BI

---

## 1. Azure Functions

### O que é e qual é sua função principal?

Azure Functions é um serviço de computação **serverless** da Microsoft Azure. Ele permite executar trechos de código (funções) em resposta a eventos — como um timer agendado, uma mensagem em fila ou uma requisição HTTP — sem que a equipe precise provisionar, configurar ou gerenciar servidores. O serviço escala automaticamente conforme a demanda e cobra apenas pelo tempo efetivo de execução, sem custo quando a função está ociosa.

### Por que foi escolhido para este projeto? Qual problema específico da CorpTech ele resolve?

No pipeline da CorpTech, a extração dos dados do Jira Service Management é uma tarefa **pontual e periódica** — ocorre uma vez por dia, dura poucos minutos e depois não exige nenhum processamento adicional. Manter um servidor dedicado VM ou container sempre ligado para executar esse único trabalho representaria custo fixo desnecessário e sobrecarga de manutenção.

O Azure Functions resolve exatamente esse problema: a função Python é disparada por um **Timer Trigger** no horário configurado, realiza a extração dos dados do Azure SQL mockado, aplica as transformações necessárias e grava os arquivos no Blob Storage — tudo sem intervenção humana e sem infraestrutura permanente. Ao final da execução, o serviço simplesmente para, zerando o custo operacional até o próximo ciclo.

### Qual seria uma alternativa? Por que foi descartada?

A alternativa mais direta seria uma **Azure Virtual Machine com um script Python agendado via cron**. Embora funcional, a VM exige custo fixo mensal (independente do uso), manutenção do sistema operacional, configuração de segurança e monitoramento manual. Para uma tarefa de poucos minutos por dia, isso representa um custo desproporcional e complexidade operacional que o projeto não justifica. O Azure Functions entrega o mesmo resultado com muito menos esforço e custo.

**Link da documentação oficial:**  
https://learn.microsoft.com/pt-br/azure/azure-functions/functions-overview

---

## 2. Azure Blob Storage

### O que é e qual é sua função principal?

Azure Blob Storage é o serviço de **armazenamento de objetos** da Azure, projetado para guardar grandes volumes de dados não estruturados — arquivos JSON, CSV, Parquet, imagens, logs, backups, entre outros. Os dados são organizados em _containers_ e cada arquivo (blob) é acessível por uma URL única, por SDK ou por API REST. O serviço oferece diferentes camadas de acesso (Hot, Cool, Archive) para otimizar o custo conforme a frequência de uso dos arquivos.

### Por que foi escolhido para este projeto? Qual problema específico da CorpTech ele resolve?

No pipeline da CorpTech, a Azure Function extrai os dados do JSM em formato bruto antes de qualquer transformação ou validação de qualidade. O Blob Storage funciona como a **camada de pouso desses dados brutos**, garantindo que o dado original esteja sempre preservado e disponível para reprocessamento.

Isso é fundamental para a rastreabilidade do pipeline: se houver um erro na transformação ou na carga para o Azure SQL de destino, a equipe pode reprocessar a partir do arquivo raw sem precisar re-extrair do JSM. Além disso, o Blob Storage tem integração nativa com Azure Functions e com o Azure SQL, o que simplifica as conexões entre os blocos da pipeline.

### Qual seria uma alternativa? Por que foi descartada?

A alternativa técnica mais próxima seria o **Azure Data Lake Storage Gen2 (ADLS Gen2)**, que adiciona suporte a hierarquia de diretórios, permissões granulares por pasta (ACL) e otimizações para workloads de Big Data com Apache Spark e Azure Databricks. Contudo, para o volume de dados deste projeto — tickets de ITSM de uma empresa de médio porte — o ADLS Gen2 seria um _over-engineering_: sua configuração é mais complexa, o custo ligeiramente maior e os recursos adicionais não seriam aproveitados. O Blob Storage padrão atende plenamente os requisitos de armazenamento e integração desta pipeline.

**Link da documentação oficial:**  
https://learn.microsoft.com/pt-br/azure/storage/blobs/storage-blobs-introduction

---

## 3. Azure SQL Database

### O que é e qual é sua função principal?

Azure SQL Database é um serviço de **banco de dados relacional totalmente gerenciado** na nuvem, baseado no Microsoft SQL Server. Ele oferece alta disponibilidade com SLA de 99,99%, backups automáticos com retenção configurável, escalabilidade elástica de recursos de computação e compatibilidade com T-SQL — tudo sem necessidade de gerenciar o servidor subjacente (sem patching de SO, sem configuração de HA manual).

### Por que foi escolhido para este projeto? Qual problema específico da CorpTech ele resolve?

O projeto utiliza o Azure SQL Database em dois papéis distintos dentro da pipeline:

1. **Como fonte mockada:** simula o banco de produção da CorpTech que alimenta o JSM, permitindo que a equipe desenvolva e teste a extração sem depender de acesso ao ambiente real desde o início do semestre.

2. **Como destino analítico:** armazena os dados após a transformação realizada pela Azure Function, incluindo as métricas calculadas de ITSM (SLA cumprido vs. violado, tempo médio de resolução, volume por categoria e fila).

A escolha de um banco **relacional** para o destino se justifica porque as métricas têm estrutura tabular bem definida, se beneficiam de queries SQL complexas com JOINs e agregações, e exigem consistência transacional (ACID). Além disso, o Power BI se conecta nativamente ao Azure SQL Database via conector oficial, sem necessidade de configuração adicional de gateway ou middleware.

### Qual seria uma alternativa? Por que foi descartada?

Uma alternativa considerada foi o **Azure Cosmos DB**, banco NoSQL multimodelo da Azure. Ele seria adequado se os dados tivessem estrutura variável ou se o projeto exigisse escala global com latência muito baixa. Contudo, os dados de métricas ITSM têm esquema previsível e bem definido, as consultas são essencialmente relacionais e o Cosmos DB adiciona complexidade de modelagem NoSQL sem benefício real para este caso. O Azure SQL Database é a escolha mais direta e eficiente.

**Link da documentação oficial:**  
https://learn.microsoft.com/pt-br/azure/azure-sql/database/sql-database-paas-overview

---

## 4. Power BI (Ferramenta de Visualização)

### O que é e qual é sua função principal?

Power BI é a plataforma de **Business Intelligence** da Microsoft, composta por três componentes principais: o **Power BI Desktop** aplicativo para criação de relatórios, o **Power BI Service** nuvem para publicação, compartilhamento e agendamento de atualização dos dados e o **Power BI Mobile** consumo em dispositivos móveis. Ele permite conectar a dezenas de fontes de dados, criar visualizações interativas — gráficos, tabelas, mapas, KPIs — e distribuir dashboards para toda a organização com controle de acesso.

### Por que foi escolhido para este projeto? Qual problema específico da CorpTech ele resolve?

O Power BI foi escolhido como ferramenta de visualização por três razões diretamente ligadas ao contexto da CorpTech:

1. **Integração nativa com Azure SQL Database:** a conexão é estabelecida em poucos cliques via conector oficial, sem necessidade de configuração de gateway, scripts de conexão ou middleware adicional. O Power BI Service suporta atualização automática agendada dos dados diretamente do Azure SQL.

2. **Ecossistema Microsoft coeso:** a CorpTech já opera na Azure e, muito provavelmente, utiliza Microsoft 365. O Power BI faz parte desse ecossistema, compartilha autenticação via Azure Active Directory (Entra ID) e pode ser integrado ao Microsoft Teams para distribuição de dashboards — sem fricção adicional de gestão de identidade.

3. **Adequação às métricas de ITSM:** o tipo de dashboard necessário para a CorpTech — SLA cumprido vs. violado, volume de chamados por fila, tempo médio de resolução por categoria — é exatamente o domínio em que o Power BI se destaca, com visuais de KPI, gráficos de barras, filtros de data e slicers interativos prontos para uso sem necessidade de código.

### Qual seria uma alternativa? Por que foi descartada?

As duas alternativas avaliadas foram **Streamlit** e **Metabase**.

- **Streamlit:** excelente para criar dashboards analíticos com Python de forma rápida. Porém, exige um servidor web em execução contínua para hospedar a aplicação (custo adicional de infraestrutura), não possui conector nativo para Azure SQL com atualização agendada, e sua capacidade de compartilhamento enterprise é limitada. Para um projeto com usuários finais não-técnicos, o Streamlit adiciona complexidade desnecessária.

- **Metabase:** ferramenta open source de BI com interface amigável e boa para exploração ad-hoc de dados. Contudo, na versão gratuita exige infraestrutura própria para hospedar (servidor Linux ou Docker), o que adiciona um novo recurso a gerenciar. A versão Cloud tem custo e, mesmo assim, a integração com o ecossistema Azure não é tão fluida quanto a do Power BI. Dado que a CorpTech já investe na Azure, o Power BI representa a escolha com menor atrito operacional.

**Link da documentação oficial:**  
https://learn.microsoft.com/pt-br/power-bi/fundamentals/power-bi-overview

---

## Resumo das Escolhas

| Serviço | Papel na Pipeline | Principal Justificativa |
|---|---|---|
| Azure SQL (Mockado) | Fonte de dados JSM | Simula banco de produção sem exposição do ambiente real |
| Azure Functions | Extração e Transformação | Serverless: sem custo ocioso, escala automática, timer trigger |
| Azure Blob Storage | Armazenamento raw | Preservação do dado original, rastreabilidade, baixo custo por GB |
| Azure SQL (Destino) | Destino analítico | Estrutura relacional para métricas, T-SQL, conector nativo Power BI |
| Power BI | Visualização | Integração nativa Azure, ecossistema Microsoft, dashboards ITSM prontos |

---

*Documento elaborado com base nas documentações oficiais da Microsoft Azure e Power BI.*  
*Todos os links de referência estão indicados em cada seção.*
