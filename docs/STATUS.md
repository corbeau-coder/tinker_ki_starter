### Now:
create OTel environment (set up OTel colletor docker, LangFuse and Prometheus)

### Next:
* create python test testing langfuse and prometheus
* check https://langfuse.com/integrations/native/opentelemetry#propagating-attributes

### Blocked:

### Open Questions:
* how and when to decide whether an additional agent evaluating lexicas result makes sense?
* refactore to use openAI so seemless modell switching and automatic instrumentialization is possible?
* how to fix absolute paths for prometheus and otel-config due to docker compose start up?

### Last Session:
* set up langfuse and prometheus using otel-con (but not tested e2e)
* imported signalbot into project dir