# ADR-001: Cloud

**Status:** Aceito
**Data:** [2026-08-27]
**Autores:** Fellipe N. Prim

## Contexto

Azure Blob Storage é o serviço de armazenamento de objetos da Azure, projetado para guardar grandes volumes de dados não estruturados — arquivos JSON, CSV, Parquet, imagens, logs, backups, entre outros. Os dados são organizados em containers e cada arquivo (blob) é acessível por uma URL única, por SDK ou por API REST. O serviço oferece diferentes camadas de acesso (Hot, Cool, Archive) para otimizar o custo conforme a frequência de uso dos arquivos.

## Decisão

Adoção do Azure Functions

## Consequências
+ No pipeline da CorpTech, a Azure Function extrai os dados do JSM em formato bruto antes de qualquer transformação ou validação de qualidade. O Blob Storage funciona como a camada de pouso desses dados brutos, garantindo que o dado original esteja sempre preservado e disponível para reprocessamento.

+ Isso é fundamental para a rastreabilidade do pipeline: se houver um erro na transformação ou na carga para o Azure SQL de destino, a equipe pode reprocessar a partir do arquivo raw sem precisar re-extrair do JSM. Além disso, o Blob Storage tem integração nativa com Azure Functions e com o Azure SQL, o que simplifica as conexões entre os blocos da pipeline.

## Alternativas rejeitadas

A alternativa técnica mais próxima seria o Azure Data Lake Storage Gen2 (ADLS Gen2), que adiciona suporte a hierarquia de diretórios, permissões granulares por pasta (ACL) e otimizações para workloads de Big Data com Apache Spark e Azure Databricks. Contudo, para o volume de dados deste projeto — tickets de ITSM de uma empresa de médio porte — o ADLS Gen2 seria um over-engineering: sua configuração é mais complexa, o custo ligeiramente maior e os recursos adicionais não seriam aproveitados. O Blob Storage padrão atende plenamente os requisitos de armazenamento e integração desta pipeline.

## Links

Link da documentação oficial:
https://learn.microsoft.com/pt-br/azure/storage/blobs/storage-blobs-introduction
