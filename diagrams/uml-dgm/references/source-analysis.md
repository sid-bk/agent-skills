# Source analysis — modeling an existing codebase

Contents: reading budget · procedure · source-to-UML mapping · language semantics · forward modeling

The output must explain the architecture. If the diagram is isomorphic to the file tree or the class list, it has added nothing a `ls` would not.

---

## Reading budget

Unbounded source reading is the main failure mode when reverse-engineering: either the whole repo gets loaded, or two files get skimmed and the rest is invented. Bound it explicitly, in this order, stopping as soon as the diagram's question can be answered.

1. **Boundary artifacts first** — `README`, `docker-compose.yml`, Kubernetes manifests, Terraform, `pyproject.toml`/`package.json`/`go.mod`, OpenAPI specs, migration files. These establish services, external systems, and deployment topology faster than any source file.
2. **Entry points** — `main`, route/handler registration, consumer subscriptions, CLI commands, cron/worker definitions. These give the real component list.
3. **Wiring** — DI containers, factories, registries, plugin loaders. These carry the dependency edges that imports alone will not show.
4. **Interfaces and models** — the type definitions the entry points reference.
5. **Implementations** — only for elements the diagram will actually show, and only for the specific question (ownership, sync/async, failure paths).

Stop when new files stop changing the model. If the budget runs out with the question unanswered, say which part of the model is unestablished and label it `[Assumed]` or omit it. Do not close the gap by inference from names.

Static imports lie in both directions: dynamic registration, reflection, DI, event subscription, and configuration-driven dispatch create real dependencies with no import; unused and type-only imports create imports with no dependency.

---

## Procedure

1. Establish the system boundary — what is inside, what is external.
2. Identify packages/modules and their dependency direction.
3. Identify major components (things with a lifecycle and a responsibility, not every class).
4. Identify important classes and interfaces.
5. Identify actual dependencies, separating compile-time from runtime.
6. Identify inheritance and realization, checking substitutability rather than the keyword.
7. Identify ownership and lifecycle relationships — who constructs what, who destroys what.
8. Identify external systems, datastores, and brokers.
9. Identify the runtime interactions worth a sequence diagram.
10. Identify process, network, and failure boundaries when deployment matters.
11. Select the diagram type and abstraction level.
12. Remove implementation detail that does not answer the question.
13. Validate every element and edge against the source; cite `path:line` for load-bearing claims.

---

## Source-to-UML mapping

Heuristics, not conversions. Each row is a *candidate* that requires semantic confirmation.

| Construct | Candidate UML | Promote only if |
|---|---|---|
| class / struct | class | — |
| abstract class | abstract class | it has shared state or implementation |
| interface / protocol / trait | interface | — |
| `implements` / conformance | realization | — |
| `extends` / subclassing | generalization | subtype is substitutable; otherwise it is reuse, model differently |
| long-lived field holding another object | association | the reference outlives a single call |
| object constructed by owner, not shared | composition | the part cannot outlive or be reassigned away from the whole |
| injected or shared collaborator | aggregation or association | prefer association unless whole-part is real |
| method parameter / local / return type | dependency | — |
| import | dependency | it is actually used at runtime |
| module / package | package | — |
| deployable service, worker, daemon | component | — |
| process, container, VM, function | node | — |
| database, cache, object store | database / component | — |
| HTTP/gRPC surface | interface / component port | — |
| message published to a broker | asynchronous message | — |

Default to the weaker relationship. A wrong `*--` claims a lifecycle guarantee the code does not make; a wrong `--` costs almost nothing.

---

## Language semantics

**Java** — `extends` → generalization, `implements` → realization, package → package, modifiers → visibility. Watch for: framework-managed lifecycles (Spring beans are usually associations, not compositions), annotation-driven wiring, and inner classes (a non-static inner class is genuinely composed).

**Python** — no declared interfaces; conformance comes from ABCs, `Protocol`, or duck typing. Inspect constructors and attribute assignment for ownership, type hints for association targets, decorators and registries for runtime wiring, and metaclasses/`__init_subclass__` for implicit hierarchies. Mixins are usually reuse, not `is-a` — do not draw them as generalization without substitutability. Names prove nothing.

**TypeScript** — structural typing means a class satisfies an interface without declaring it; realization edges may need inference, and should be labeled `[Inferred]`. `interface` and `type` erase at runtime, so they never appear in a deployment or runtime component view. Distinguish `import type` (no runtime dependency) from value imports. Module boundaries are files, not directories.

**Go** — interface satisfaction is implicit; the realization edge must be inferred from usage sites, not declarations. Struct embedding is delegation, not classical inheritance: model as composition or association unless the promoted method set is genuinely used polymorphically. Packages are the real module boundary. Goroutines and channels are asynchronous — do not draw them as synchronous calls.

**Rust** — `impl Trait for T` → realization. Ownership (`T` vs `&T` vs `Arc<T>`) is memory semantics, not automatically UML composition: `Arc<T>` shared across owners is closer to association or aggregation. Enums with data are sum types, often better modeled as a state machine or a generalization hierarchy than as an `<<enumeration>>`. Traits with default methods resemble abstract classes.

**Anywhere** — dependency injection, event buses, plugin registries, and config-driven dispatch produce runtime edges invisible to static analysis. If the diagram claims a runtime dependency, say how it was established.

---

## Forward modeling from requirements

When there is no source:

1. Identify actors and their goals.
2. Identify system responsibilities.
3. Identify domain concepts and their invariants.
4. Establish architectural boundaries before enumerating classes.
5. Identify components/services and their interfaces.
6. Identify external dependencies.
7. Model the two or three workflows that carry the most risk.
8. Model lifecycle/state where legality of operations depends on state.
9. Model deployment only when infrastructure constrains the design.
10. Validate against the requirements, naming what the requirements do not settle.

Do not generate hundreds of classes ahead of the decisions that would justify them. Every element in a forward model is `[Proposed]`; label the diagram accordingly and keep it separate from any current-state diagram.
