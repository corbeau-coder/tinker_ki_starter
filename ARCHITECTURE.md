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
    A["User <br>Sending request per chat"]
    B["App <br>Finds out how to fulfil the request"]
    C["User <br>receiving requested info"]
    
    A -->|send message| B
    B -->|send feedback| C
```


### Container diagram
```mermaid
graph LR
    A["signalbot <br>receiving user requests"]
    B["faster.whisper <br>Speech to text"]
    C["agentic system <br>LLM via Ollama"]
    D["orchestrator <br>order queuing, validating"] 
    E["signalbot <br>transmitting response"]
        
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
    subgraph agent["Agentic system - Python"]
        EXT["outside system <br>interface"]
        
        A["Orchestrator <br>overwatching pipeline states"]
        B["Tool Smith <br>generating/maintaining tools"]
        C["Lexica <br>LLM seeking for the requests solution"]
        E["tool belt <br>MCP tool collection"]
        
        
        A -->|requesting tool list|B
        B -->|sending tool list|A
        A -->|sends request|C
        C -->|receiving answer, might want to adjust tools and repeat|A
        B -->|curating tools|E
        C -->|uses tools|E
        
        
        
        
    end
```

```mermaid
graph TD
    J -->|Max loops/token limit reached| H[respond to request]
    J -->|Exit| H[respond to request]
    A([receiving request]) -->J{Orchestrator to decide}
    B[Orchestrator loads tool list into Lexica]
    B --> C[Lexica is executing request]
    C -->|Sending result| K[TODO: external evaluation?]
    %% TODO: external evaluator?
    K --> J
    F -->|Yes| G[Tool smith to craft tool]
    F -->|No| B
    J -->|Continue looping| F{Tool missing?}
    G -->|Updates tool list| B

```

```mermaid
stateDiagram-v2
    [*] --> Idle
```