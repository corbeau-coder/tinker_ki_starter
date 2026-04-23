### Title:
ADR-001 Pipeline context object as format between pipeline steps

### Status:
ACCEPTED

### Context:
A few factors were driving this:
* how to properly debug the system?
* how to monitor the system properly?
* how to test the system, especially the AI parts in it?

Consulting AI i learned about observing agentic systems through checkpoints where you instrument them. 
It drew my attention, it felt like it is obvious serving all the points above - so i read about this concept and it feels
like the right thing to do - but good, another bunch of extra work - but also earning extra learning \o/

### Decision:
there is a explicit object in which the complete payload is communicated - it has to be serializable for dumping it at
every checkpoint

### Consequences:
it will add extra work in coding preparation. Extra classes and probably a good bunch of thoughts about what is taking
a ride through the pipeline.
it will pay back while testing and debugging it.

### Date of decision:
2026-04-23
