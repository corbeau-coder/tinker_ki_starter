### Now:
create OTel environment (set up OTel colletor docker, LangFuse and Prometheus)

### Next:
ADR Session / solving open questions

### Blocked:

### Open Questions:
* how and when to decide whether an additional agent evaluating lexicas result makes sense?
* refactore to use openAI so seemless modell switching and automatic instrumentialization is possible?
* how to fix absolute paths for prometheus and otel-config due to docker compose start up?
* how to offloading tool building to cloud-based models? ADR?!?
* missing ADR: how to implement token monitoring?
* events not working on langfuse
* ADR session needed - implementation should work with both, cloud and local setup

### Last Session:
* set up langfuse and prometheus using otel-con (but not tested e2e)
* imported signalbot into project dir
* added baggage