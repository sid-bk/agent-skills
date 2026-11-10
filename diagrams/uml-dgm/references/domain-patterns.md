# Domain patterns, decomposition, and review

Contents: architecture styles · APIs, events, data · AI/agentic systems · distributed systems · decomposition sets · review heuristics

---

## Architecture styles

**Layered** — Presentation → Application → Domain → Infrastructure. Distinguish *dependency direction* from *runtime call direction*: under dependency inversion the domain defines a repository interface that infrastructure implements, so the dependency arrow points inward while the call goes outward. Drawing only one of the two, unlabeled, is the usual source of confusion. Show interface ownership explicitly.

**Microservices** — model services, API boundaries, per-service datastores, events, brokers, and external systems. Do not put internal classes in a service architecture diagram. Make database ownership explicit: a shared database between two services is an architectural fact worth its own edge, not an implementation detail. Distinguish request/response from event-driven edges.

**Monolith** — component or package diagrams for module boundaries, bounded contexts, dependency direction, and shared infrastructure. The useful question is usually "which modules may depend on which", so orient the diagram around allowed vs actual dependency direction.

**Event-driven** — the broker is a first-class element, not an arrow. Show topics/queues as nodes so fan-out and multiple consumers are visible. Publisher and subscriber are decoupled: never draw a direct edge between them.

**Domain-driven design** — model entities, value objects, aggregates and their roots, repositories, domain services, application services, and bounded contexts *only where the code or design supports the classification*. Aggregate boundaries are the load-bearing information; mark them (`<<aggregate root>>` on the root, boundary drawn around members). Do not assign DDD stereotypes to a codebase that does not use DDD.

---

## APIs, events, and data

**APIs** — represent as interfaces or component ports with the contract, not one class per endpoint. Endpoint-level modeling is justified only when the endpoint set itself is the subject.

**Messages** — distinguish, and name accordingly:

```
Command  → requested action, one handler, may be rejected     (Imperative: ChargeCard)
Event    → fact that already happened, many subscribers        (Past tense: CardCharged)
Query    → request for information, no state change            (GetBalance)
```

**Data** — three separate models, never silently merged:
- component/deployment diagram: where the data lives and who owns it
- class diagram: the domain model and its invariants
- ER diagram: the relational schema

A domain class is not a table. An aggregate may span tables; a table may exist purely for infrastructure (outbox, audit, join tables). If the mapping is the subject, show both models side by side and annotate the mapping.

---

## AI and agentic systems

Do not collapse the model, orchestrator, tools, and memory into one "AI" box when their boundaries matter — which is most of the time, because that boundary is where latency, cost, failure, and security live.

Distinguish these responsibilities when present:

```
Agent API / entry point      Orchestration / graph runtime
Planning                     Execution / tool invocation
Tool registry                Individual tools + the external systems they reach
Model / LLM provider         Short-term state (per-run)  vs  long-term memory (persisted)
Retrieval (index + store)    Event/callback stream, human-in-the-loop interrupts
Guardrails / policy          Evaluation and tracing
```

Which diagram answers which question:
- **Component** — what the runtime is made of; where the LLM boundary and the tool boundary sit; which tools reach external systems.
- **Sequence** — one run: prompt assembly, model call, tool call, tool result, loop, termination. Model calls are network calls to an external system; draw them as such. Show retries, timeouts, and the loop-termination condition — these are where agent designs actually fail.
- **State machine** — the run lifecycle: `Planning → ToolCall → Observing → Planning … → Complete`, plus `Failed`, `Interrupted`, `AwaitingHuman`. Guards carry the step/token budget.
- **Class** — only when tool schemas, message types, or state objects are the subject.

Common modeling errors specific to these systems: drawing the LLM as internal; drawing streaming as a single synchronous return; omitting the loop so the diagram implies one tool call; showing memory as a component while hiding what persists it; conflating per-run state with cross-run memory.

---

## Distributed systems and deployment

Deployment diagrams answer "where does this execute". Model physical/virtual machines, containers, pods, serverless functions, devices, execution environments, deployed artifacts (with versions when relevant), and network relationships.

Make these boundaries explicit, because each is a place the system can fail differently:

```
process boundary       network boundary       failure boundary
data ownership         synchronous edge       asynchronous edge
persistent storage     external system        trust/security boundary
```

Never draw an asynchronous interaction as a synchronous call — it changes what a reader concludes about latency, coupling, and failure propagation. Annotate protocol and port when the diagram is for operations.

---

## Decomposition sets

A complex system is a set of focused diagrams, each with one purpose. Produce the ones the question needs; offer the rest.

```
01-system-context            who uses it, what it talks to        (L1 / C4 Context)
02-component-architecture    internal units and dependencies      (L2–L3)
03-domain-class-model        core types and their relationships   (L4)
04-primary-execution-flow    the main request or run, end to end  (sequence)
05-lifecycle-state-machine   the entity or run lifecycle          (state)
06-deployment                where it executes                    (deployment)
07-data-model                relational schema                    (ER)
```

Keep names, boundaries, terminology, and relationship semantics consistent across the set. An element that appears in two diagrams must be the same element, at a declared level, under the same name.

---

## Review heuristics

When reviewing a diagram or deriving architecture from code, examine:

```
coupling                    cohesion                  dependency direction
circular dependencies       layer violations          leaky abstractions
god classes/components      excessive external coupling
unclear data ownership      incorrect lifecycle relationships
missing boundaries          hidden synchronous coupling in an "async" design
```

Two rules keep review honest:

1. **Do not call something an architectural problem merely because it violates a preferred pattern.** Name the concrete dependency, responsibility, or failure consequence. "Repository is called from the controller" is a pattern deviation; "the controller depends on the Postgres driver, so the domain cannot be tested without a database" is a problem.
2. **Do not infer a design flaw from diagram appearance.** A crowded box may be a modeling failure — wrong abstraction level, too many diagrams collapsed into one — rather than a god component. Check responsibilities, dependency direction, and runtime behavior in the source before making the claim.

When reviewing someone else's diagram, separate three findings: notation errors (wrong arrow), modeling errors (relationship not supported by the system), and architecture findings (the system itself). They have different audiences and different fixes.
