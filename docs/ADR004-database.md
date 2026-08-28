# ADR-004: Escolha da database

**Status:** Aceito
**Data:** [2026-08-27]
**Autores:** Fellipe N. Prim

## Contexto

O projeto utiliza o Azure SQL Database em dois papéis distintos dentro da pipeline:

Como fonte mockada: simula o banco de produção da CorpTech que alimenta o JSM, permitindo que a equipe desenvolva e teste a extração sem depender de acesso ao ambiente real desde o início do semestre.

Como destino analítico: armazena os dados após a transformação realizada pela Azure Function, incluindo as métricas calculadas de ITSM (SLA cumprido vs. violado, tempo médio de resolução, volume por categoria e fila).

A escolha de um banco relacional para o destino se justifica porque as métricas têm estrutura tabular bem definida, se beneficiam de queries SQL complexas com JOINs e agregações, e exigem consistência transacional (ACID). Além disso, o Power BI se conecta nativamente ao Azure SQL Database via conector oficial, sem necessidade de configuração adicional de gateway ou middleware.

## Decisão

Adoção do Azure SQL Database

## Consequências
+ SLA de 99,99%
+ backups automáticos com retenção configurável
+ escalabilidade elástica de recursos de computação
+ compatibilidade com T-SQL
- possível dependência do ecossistema

## Alternativas rejeitadas

Uma alternativa considerada foi o Azure Cosmos DB, banco NoSQL multimodelo da Azure. Ele seria adequado se os dados tivessem estrutura variável ou se o projeto exigisse escala global com latência muito baixa. Contudo, os dados de métricas ITSM têm esquema previsível e bem definido, as consultas são essencialmente relacionais e o Cosmos DB adiciona complexidade de modelagem NoSQL sem benefício real para este caso. O Azure SQL Database é a escolha mais direta e eficiente.

## Links

Link da documentação oficial:
https://learn.microsoft.com/pt-br/azure/azure-sql/database/sql-database-paas-overview
