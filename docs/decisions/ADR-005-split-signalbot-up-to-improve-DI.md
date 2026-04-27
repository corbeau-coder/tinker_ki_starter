### Title:
ADR-005 splitting up signalbots interface for in as for outgoing communication for better testing 
### Status:
ACCEPTED

### Context:
signalbot is the main interface with the user and start and endpoint of a pipeline cycle. its implementation should be
tested thoroughly

### Decision:
Implement/wrap signalbot in a way that in and outcoming interface can be used per DI

### Consequences:
Care while implementing signalbot

### Date:
2026-04-27