### Title:
ADR-004 no langchain usage for now
### Status:
ACCEPTED

### Context:
owning your data and audio files as potential sample is a main motivation to build this local solution - where ever 
possible data has to stay locally

### Decision:
langchain is seen a potential problem if not handled correctly. Not having a lot of experience and
also not having much benefit from it leads to ruling out langchain for now as a tool.

### Consequences:
for now all calls to models will be done directly via ollama-api

### Date:
2026-04-27