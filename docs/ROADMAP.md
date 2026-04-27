## Delivery Promise: The application is the everyday servant AI 

The purpose is AI should serve as the best servant it can be - knowing everything, memorize everything and always
"know one" - It can create tools on the fly and might decide to persist them and their results

### Acceptance Criteria:
* can communicate via signal messenger (direct chat, group chat)
* isolates properly different user (groups)
* memorize what it was asked for
* GDPR conformity

### Milestones
* [x] M1: signalbot up, running and responding on audio messages
* [ ] M2: agentic network concept is proven by PoC (no tool creation yet, only find out what is missing to reach best result)
* [ ] M3: PoC for tool creation and persistence decision
* [ ] M4: TDD red phase: Create E2E tests reflecting use cases
* [ ] M5: TDD green phase: Implement first E2E version including tool creation

### Current Milestone: M2

### Steps
* [ ] finalize container drawing in ARCHITECTURE.md
* [ ] check for fitting model with MCP capability
* [ ] create OTel environment (set up OTel colletor, LangFuse and Prometheus)
* [ ] build 5 artifical requests the agents should "solve"
* [ ] implement first version including instrumentation
* [ ] start/debug/analyze first version the 5 requests