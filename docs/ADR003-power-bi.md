# ADR-003: Power BI

**Status:** Aceito
**Data:** [2026-08-27]
**Autores:** Fellipe N. Prim

## Contexto

Power BI é a plataforma de Business Intelligence da Microsoft, composta por três componentes principais: o Power BI Desktop aplicativo para criação de relatórios, o Power BI Service nuvem para publicação, compartilhamento e agendamento de atualização dos dados e o Power BI Mobile consumo em dispositivos móveis. Ele permite conectar a dezenas de fontes de dados, criar visualizações interativas — gráficos, tabelas, mapas, KPIs — e distribuir dashboards para toda a organização com controle de acesso.

## Decisão

Adoção do Power BI

## Consequências
+ Integração nativa com Azure SQL Database: a conexão é estabelecida em poucos cliques via conector oficial, sem necessidade de configuração de gateway, scripts de conexão ou middleware adicional. O Power BI Service suporta atualização automática agendada dos dados diretamente do Azure SQL.

+ Ecossistema Microsoft coeso: a CorpTech já opera na Azure e, muito provavelmente, utiliza Microsoft 365. O Power BI faz parte desse ecossistema, compartilha autenticação via Azure Active Directory (Entra ID) e pode ser integrado ao Microsoft Teams para distribuição de dashboards — sem fricção adicional de gestão de identidade.

+ Adequação às métricas de ITSM: o tipo de dashboard necessário para a CorpTech — SLA cumprido vs. violado, volume de chamados por fila, tempo médio de resolução por categoria — é exatamente o domínio em que o Power BI se destaca, com visuais de KPI, gráficos de barras, filtros de data e slicers interativos prontos para uso sem necessidade de código.

## Alternativas rejeitadas

As duas alternativas avaliadas foram Streamlit e Metabase.

Streamlit: excelente para criar dashboards analíticos com Python de forma rápida. Porém, exige um servidor web em execução contínua para hospedar a aplicação (custo adicional de infraestrutura), não possui conector nativo para Azure SQL com atualização agendada, e sua capacidade de compartilhamento enterprise é limitada. Para um projeto com usuários finais não-técnicos, o Streamlit adiciona complexidade desnecessária.

Metabase: ferramenta open source de BI com interface amigável e boa para exploração ad-hoc de dados. Contudo, na versão gratuita exige infraestrutura própria para hospedar (servidor Linux ou Docker), o que adiciona um novo recurso a gerenciar. A versão Cloud tem custo e, mesmo assim, a integração com o ecossistema Azure não é tão fluida quanto a do Power BI. Dado que a CorpTech já investe na Azure, o Power BI representa a escolha com menor atrito operacional.

## Links

Link da documentação oficial:
https://learn.microsoft.com/pt-br/power-bi/fundamentals/power-bi-overview
