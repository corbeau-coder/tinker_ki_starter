# Architecture concepts

## Decisions

- [ADR-001](docs/decisions/ADR-001-pipeline-context-object.md) - Pipeline Context Object
- [ADR-002](docs/decisions/ADR-002-multi-tenant-operation.md) - Multi Tenant Operation
- [ADR-003](docs/decisions/ADR-003-opentelemetry.md) - OpenTelemetry
- [ADR-004](docs/decisions/ADR-004-no-langchain-usage.md) - No LangChain
- [ADR-005](docs/decisions/ADR-005-split-signalbot-up-to-improve-DI.md) - Using DI on signalbot interfacing logic
- [ADR-006](docs/decisions/ADR-006-GDPR.md) - GDPR is respected


## Diagrams

### Context diagram
```mermaid
graph LR
    A["User
    Sending request per chat"]
    B["App
    Finds out how to fulfil the request
    "]
    C["User
    receiving requested info"]
    
    A -->|send message| B
    B -->|send feedback| C
```


### Container diagram
```mermaid
graph LR
    A["signalbot
    receiving user requests"]
    B["faster.whisper
    Speech to text"]
    C["agentic system
    LLM via Ollama"]
    D["orchestrator
    order queuing, validating"] 
    E["signalbot
    transmitting response"]
        
    A -->|Audio file via file system or text| D
    D -.->|Audio file| B
    B -.->|Transcript| D
    D -->|transmit request| C
    C -->|Response| D
    D -->|sending out answer| E
```

### Component diagram agentic system
```mermaid
graph LR
    subgraph agent["Agentic system — Python"]
        M["miracle
        "]
        
    end
```

### Sequence diagram
```mermaid
sequenceDiagram
    participant N as Nutzer
    participant S as Signal
    participant W as Whisper
    participant A as Agent

    N->>S: Sprachnachricht
    S->>W: Audiodatei
    Note over W: Transkription läuft...
    W->>A: Transkript
    Note over A: Agent denkt nach...
    A->>S: Textantwort
    S->>N: Antwort via Signal

    rect rgb(250, 220, 220)
        Note over W,S: Fehlerfall
        W-->>S: Fehler-Event
        S->>N: Konnte nicht verarbeiten
    end
```

## Decisions