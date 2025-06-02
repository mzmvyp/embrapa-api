# Fluxograma do Sistema EMBRAPA

```mermaid
graph LR
    %% Subgraphs organizados horizontalmente
    subgraph Login
        A[Usuário]
        B[API Flask]
    end

    subgraph Dependencias_Compartilhadas
        C[Autenticação JWT]
        F[PostgreSQL]
    end

    subgraph Fonte_de_Dados_Externa
        D[Embrapa - Site Externo]
    end

    subgraph Documentacao_API
        E[Swagger UI]
    end

    subgraph Deploy_e_Consumo
        G[Vercel]
        H[Consumidores]
        I[Relatórios]
        J[Dashboards]
        K["Modelos ML"]
    end

    %% Fluxo Login
    A -->|POST Credenciais| B
    B -->|Valida Credenciais| F
    F -->|Dados do Usuário| B
    B -->|Gera Token| C
    C -->|Token JWT| B
    B -->|200 OK + Token JWT| A

    %% Fluxo Requisição de Dados
    A -->|GET + Token JWT| B
    B -->|Valida Token| C
    C -->|Token Válido| B
    B -->|Coleta dados| D
    D -->|Retorna HTML| B
    B -->|200 OK + Dados JSON| A

    %% Documentação
    B -->|Documentação| E
    E -->|Teste Requisição| B

    %% Deploy e Consumo
    B -->|Deploy| G
    G -->|URL pública| H
    H --> I
    H --> J
    H --> K

    %% Estilos
    classDef defaultNodeStyle fill:#2F4F4F,stroke:#8FBC8F,stroke-width:2px,color:#fff,rx:10,ry:10;
    classDef siteNodeStyle fill:#4682B4,stroke:#8FBC8F,stroke-width:2px,color:#fff,rx:10,ry:10;
    classDef dbNodeStyle fill:#A0522D,stroke:#8FBC8F,stroke-width:2px,color:#fff,rx:10,ry:10;

    class A,B,C,E,G,H,I,J,K defaultNodeStyle
    class D siteNodeStyle
    class F dbNodeStyle

    linkStyle default stroke:#8FBC8F, stroke-width: 2px;
