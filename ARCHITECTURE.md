# Architecture concepts

This diagram should give guidance how the app is build. it especially guides the developer himself to find out of rabbits hole again xD

## Diagrams

### Context diagram
```mermaid
graph LR
    A["User
    Sending request per chat"]
    B["App
    Finds out how to fulfil the request
    "]
    C["Reports back
    Either giving info or reporting state"]
    
    A -->|send message| B
    B -->|send feedback| C
```


### Container diagram
```mermaid
graph LR
    A["signalbot
    Receiving request"]
    B["faster.whisper
    Speech to text"]
    C[agentic system
    LLM via Ollama]
    D[signalbot
    Sending answer]
    
    A -->|Audiofile or text via file system| B
    B -->|Transcript| C
    C -->|Response| D
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