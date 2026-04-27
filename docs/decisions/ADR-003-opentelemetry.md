### Title:
ADR-003 OpenTelemetry framework as framework for telemetry, monitoring and debugging

### Status:
ACCEPTED

### Context:
Especially with the tool smith-agent concept it is needed to closely monitor the application. The checkpoints are already
having most of the needed data, so a format/API/framework shall be used which make us easily instrument these information
by not blocking out langfuse or others.

### Decision:
the open telemetry framework shall be used to publish the checkpoints.

### Consequences:
* all checkpoints shall be published with OTel
* security concept, payload may include sensitive data
* create a central backend consuming the traces persistent over debug sessions/programm versions
* create a logging concept how data model version and application version is reflected
* it pressures the point of create the concept for multi tenant operation

### Date:
2026-04-27
