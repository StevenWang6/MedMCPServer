"""Built-in IEC 62304 knowledge base.

This module encodes the structure and key requirements of IEC 62304
("Medical device software — Software life cycle processes") as a typed,
searchable collection of :class:`~medmcp.models.KnowledgeEntry` objects.

The content is a structured, educational summary of the standard's clauses and
is intended to support navigation and comprehension. It is NOT a substitute for
the normative text: organizations must implement the processes required by the
published standard and their applicable regulatory framework.
"""

from __future__ import annotations

from medmcp.models import Category, KnowledgeEntry

# (id, clause, title, category, keywords, related, safety_class, content)
# Entries are kept as raw tuples for compact authoring and converted below.
_RAW: list[tuple[str, str, str, Category, list[str], list[str], str | None, str]] = [
    # ---------------------------------------------------------------- Clause 1
    (
        "1", "1", "Scope",
        "general",
        ["scope", "medical device software", "life cycle", "applicability"],
        ["4", "5"],
        None,
        "IEC 62304 defines the life cycle requirements for MEDICAL DEVICE SOFTWARE. "
        "It provides a common framework for the development and maintenance of software "
        "that is itself a medical device, or an embedded or integral part of a medical "
        "device. The standard is a process standard: it prescribes processes, activities "
        "and tasks, not a specific development methodology.",
    ),
    (
        "2", "2", "Normative references",
        "general",
        ["references", "iso 14971", "iso 13485", "risk management"],
        ["4.2", "4.1"],
        None,
        "IEC 62304 references other standards that are indispensable for its application. "
        "Key references include ISO 14971 (risk management for medical devices) and, in the "
        "context of quality management, ISO 13485. Where dated references are cited, only "
        "the cited edition applies; for undated references the latest edition applies.",
    ),
    # ---------------------------------------------------------------- Clause 3
    (
        "3", "3", "Terms and definitions",
        "concept",
        ["terms", "definitions", "vocabulary", "software item", "software unit"],
        ["5"],
        None,
        "Clause 3 defines terminology used throughout the standard. Important terms include: "
        "MEDICAL DEVICE SOFTWARE (software or software system intended to be part of a "
        "medical device or itself a medical device); SOFTWARE SYSTEM (an integrated composite "
        "of software items); SOFTWARE ITEM (an identifiable part of a computer program); "
        "SOFTWARE UNIT (the smallest separately testable software item); and RISK "
        "(combination of probability of harm and severity of that harm).",
    ),
    (
        "3.1", "3.1", "Medical device software",
        "concept",
        ["medical device software", "definition", "software system"],
        ["1", "4.3"],
        None,
        "MEDICAL DEVICE SOFTWARE is software (including its embedded operating environment) "
        "that is intended by its manufacturer to be incorporated into a medical device, or "
        "that is intended by its manufacturer to be used by itself as a medical device.",
    ),
    (
        "3.2", "3.2", "Software system / software item / software unit",
        "concept",
        ["software system", "software item", "software unit", "decomposition"],
        ["5.3", "5.4", "5.5"],
        None,
        "A SOFTWARE SYSTEM is an integrated set of SOFTWARE ITEMS assembled to accomplish a "
        "specific function or set of functions. A SOFTWARE ITEM is an identifiable part of a "
        "computer program. A SOFTWARE UNIT is the smallest software item that can be "
        "independently compiled, linked and tested. These terms anchor the hierarchical "
        "decomposition used in the architectural and detailed design clauses.",
    ),
    # ---------------------------------------------------------------- Clause 4
    (
        "4", "4", "General requirements",
        "general",
        ["general requirements", "quality", "risk management", "safety classification", "legacy"],
        ["4.1", "4.2", "4.3", "4.4", "5"],
        None,
        "Clause 4 establishes four general requirements that apply to the whole software life "
        "cycle: (4.1) a quality management system; (4.2) risk management; (4.3) software "
        "safety classification; and (4.4) handling of legacy software.",
    ),
    (
        "4.1", "4.1", "Quality management system",
        "general",
        ["qms", "quality management system", "iso 13485", "organization"],
        ["2", "5", "8", "9"],
        None,
        "The organization shall have a QUALITY MANAGEMENT SYSTEM (QMS), typically compliant "
        "with ISO 13485, covering the development and maintenance of the medical device "
        "software. The processes of IEC 62304 are expected to operate within that QMS.",
    ),
    (
        "4.2", "4.2", "Risk management",
        "general",
        ["risk management", "iso 14971", "hazard", "risk analysis"],
        ["2", "7", "5.2.4", "5.3.3", "5.4.3"],
        None,
        "The organization shall apply a RISK MANAGEMENT process complying with ISO 14971 to "
        "the medical device software. Software-related risks shall be analysed and controlled "
        "throughout the life cycle. Clause 7 elaborates the software risk management process.",
    ),
    (
        "4.3", "4.3", "Software safety classification",
        "general",
        ["safety classification", "class a", "class b", "class c", "severity", "harm"],
        ["4.2", "7.1", "5.1.7"],
        None,
        "Software shall be classified according to the severity of harm that a failure of the "
        "software could contribute to. CLASS A: no injury or damage to health is possible. "
        "CLASS B: non-serious injury is possible. CLASS C: death or serious injury is possible. "
        "Classification drives the depth of documentation and verification required for many "
        "activities; the safety class shall be documented and its rationale recorded.",
    ),
    (
        "4.3.1", "4.3", "Safety class A — no harm possible",
        "general",
        ["class a", "safety class a", "no harm"],
        ["4.3", "5.1.7"],
        "A",
        "CLASS A applies when a failure of the software system cannot result in any injury or "
        "damage to health. Example candidates include software that only processes data without "
        "affecting diagnosis or therapy (e.g. a purely administrative records display with no "
        "safety impact).",
    ),
    (
        "4.3.2", "4.3", "Safety class B — non-serious injury possible",
        "general",
        ["class b", "safety class b", "non-serious injury"],
        ["4.3", "5.1.7"],
        "B",
        "CLASS B applies when a software failure could result in non-serious injury. This is "
        "typically determined through risk analysis (ISO 14971) based on the severity of the "
        "consequences of a hazardous situation to which the software contributes.",
    ),
    (
        "4.3.3", "4.3", "Safety class C — death or serious injury possible",
        "general",
        ["class c", "safety class c", "serious injury", "death"],
        ["4.3", "5.1.7"],
        "C",
        "CLASS C applies when a software failure could result in death or serious injury. "
        "Class C software demands the most rigorous documentation and verification, and the "
        "software risk management process (clause 7) is mandatory for such software.",
    ),
    (
        "4.4", "4.4", "Legacy software",
        "general",
        ["legacy software", "software of unknown provenance", "soup"],
        ["4.3", "5"],
        None,
        "For LEGACY SOFTWARE (software already in use that was not developed under the "
        "current processes, sometimes including software of unknown provenance / SOUP), the "
        "organization shall establish documented plans and processes. Typically this means "
        "evaluating the legacy software's intended use, its safety classification, its known "
        "problems, and performing gap analysis so it can be brought under configuration and "
        "risk management control.",
    ),
    # ---------------------------------------------------------------- Clause 5
    (
        "5", "5", "Software development process",
        "development",
        ["software development process", "development life cycle", "v-model"],
        ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8"],
        None,
        "Clause 5 defines the SOFTWARE DEVELOPMENT PROCESS and its eight sub-processes: "
        "(5.1) development planning; (5.2) requirements analysis; (5.3) architectural design; "
        "(5.4) detailed design; (5.5) unit implementation and verification; (5.6) integration "
        "and integration testing; (5.7) system testing; and (5.8) release.",
    ),
    (
        "5.1", "5.1", "Software development planning",
        "development",
        ["development planning", "plan", "sdlc", "life cycle model"],
        ["5", "5.1.1", "5.1.4", "5.1.5", "5.1.6", "5.1.7"],
        None,
        "The manufacturer shall plan the software development. The plan shall describe the "
        "software development life cycle model used and the activities and tasks to be "
        "performed. The plan shall be kept updated as development proceeds.",
    ),
    (
        "5.1.1", "5.1.1", "Development plan content",
        "development",
        ["development plan", "plan content", "activities", "tasks"],
        ["5.1"],
        None,
        "The development plan shall define the activities and tasks to be performed, the life "
        "cycle model, deliverables, resources, responsibilities, and the interfaces between "
        "activities (including those carried out by third parties).",
    ),
    (
        "5.1.2", "5.1.2", "Keep the development plan updated",
        "development",
        ["plan update", "maintain plan"],
        ["5.1", "5.1.1"],
        None,
        "The software development plan shall be kept up to date throughout the development "
        "life cycle to reflect the actual state of the development work.",
    ),
    (
        "5.1.3", "5.1.3", "Plan reference to system design and development",
        "development",
        ["system design", "system development", "plan reference"],
        ["5.1"],
        None,
        "The software development plan shall reference the system design and development "
        "activities, so that software activities are coordinated with the overall medical "
        "device design and development effort.",
    ),
    (
        "5.1.4", "5.1.4", "Software development standards, methods and tools",
        "development",
        ["standards", "methods", "tools", "coding standards"],
        ["5.1", "5.5"],
        None,
        "The organization shall document or reference the standards, methods and tools to be "
        "used for software development, such as coding standards, naming conventions, "
        "development tools and verification tooling.",
    ),
    (
        "5.1.5", "5.1.5", "Software integration and integration testing plan",
        "development",
        ["integration plan", "integration testing plan"],
        ["5.1", "5.6"],
        None,
        "A plan for software integration and integration testing shall be established, "
        "defining how software items and units will be assembled and how integration will be "
        "verified.",
    ),
    (
        "5.1.6", "5.1.6", "Software verification plan",
        "development",
        ["verification plan", "v&v"],
        ["5.1", "5.5.2", "5.6.3", "5.7.4"],
        None,
        "A software verification plan shall define the activities for verifying that the "
        "software meets its requirements, including unit, integration and system level "
        "verification approaches and responsibilities.",
    ),
    (
        "5.1.7", "5.1.7", "Software risk management plan",
        "development",
        ["risk management plan", "risk plan"],
        ["5.1", "7"],
        None,
        "A software risk management plan shall be established, describing how the software "
        "risk management process (clause 7) will be applied and how the software safety "
        "classification (clause 4.3) will be determined and maintained.",
    ),
    (
        "5.1.8", "5.1.8", "Documentation plan",
        "development",
        ["documentation plan", "documents", "records"],
        ["5.1", "5.8"],
        None,
        "A documentation plan shall define the documentation to be produced during software "
        "development, including its form and content, so that the development activities and "
        "the resulting software are adequately documented.",
    ),
    (
        "5.1.9", "5.1.9", "Software configuration management plan",
        "development",
        ["configuration management plan", "scm plan"],
        ["5.1", "8"],
        None,
        "A software configuration management plan shall be established, describing how "
        "configuration identification, change control and configuration status accounting "
        "(clause 8) will be performed.",
    ),
    (
        "5.1.10", "5.1.10", "Supporting items to be controlled",
        "development",
        ["supporting items", "soup", "third party software"],
        ["5.1", "8", "4.4"],
        None,
        "The plan shall address supporting items, such as third-party software and software of "
        "unknown provenance (SOUP), so that they are identified, controlled and verified for "
        "their intended use.",
    ),
    (
        "5.2", "5.2", "Software requirements analysis",
        "development",
        ["software requirements", "requirements analysis", "srs"],
        ["5", "5.2.1", "5.2.2", "5.2.3", "5.2.4"],
        None,
        "The manufacturer shall define and document the software requirements, covering "
        "functional and performance requirements, interfaces, alarms, security and other "
        "content required by clause 5.2.2. The requirements shall be verified.",
    ),
    (
        "5.2.1", "5.2.1", "Define and document software requirements",
        "development",
        ["software requirements", "srs", "define requirements"],
        ["5.2"],
        None,
        "Software requirements shall be defined and documented in a form that allows them to "
        "be traced and verified. They include functional and performance requirements and the "
        "environment in which the software must operate.",
    ),
    (
        "5.2.2", "5.2.2", "Content of software requirements",
        "development",
        ["requirements content", "functional requirements", "performance", "interfaces", "security", "alarms"],
        ["5.2", "5.2.1"],
        None,
        "Software requirements shall include, as applicable: (a) functional and performance "
        "requirements; (b) inputs and outputs; (c) interfaces to other systems and to users; "
        "(d) software-driven alarms, warnings and operator messages; (e) security "
        "requirements; (f) user interface requirements; (g) data definitions and database "
        "requirements; (h) installation and acceptance requirements; (i) operation and "
        "maintenance requirements; (j) networking requirements; (k) user documentation "
        "requirements; and (l) regulatory requirements.",
    ),
    (
        "5.2.3", "5.2.3", "Verify software requirements",
        "development",
        ["verify requirements", "requirements review"],
        ["5.2", "5.1.6"],
        None,
        "Software requirements shall be verified to ensure they are correct, unambiguous, "
        "complete, consistent and testable, and that they meet the needs of the intended use.",
    ),
    (
        "5.2.4", "5.2.4", "Software requirements for risk control",
        "development",
        ["risk control requirements", "safety requirements"],
        ["5.2", "7.2"],
        None,
        "The software requirements shall include requirements that implement the risk control "
        "measures identified by the risk management process (clause 7), so that safety-related "
        "requirements are traceable to risk controls.",
    ),
    (
        "5.3", "5.3", "Software architectural design",
        "development",
        ["architectural design", "architecture", "software items"],
        ["5", "5.3.1", "5.3.2", "5.3.3"],
        None,
        "The software shall be decomposed into software items and the software architecture "
        "shall be designed and documented. The architecture shall be verified against the "
        "software requirements.",
    ),
    (
        "5.3.1", "5.3.1", "Document the architecture",
        "development",
        ["architecture document", "decompose", "software items"],
        ["5.3"],
        None,
        "The software architecture shall be documented, decomposing the software into software "
        "items and describing their interfaces and interactions, so that requirements can be "
        "allocated to architecture components.",
    ),
    (
        "5.3.2", "5.3.2", "Verify the architecture",
        "development",
        ["verify architecture", "architecture review"],
        ["5.3", "5.3.1"],
        None,
        "The software architecture shall be verified to ensure it satisfies the software "
        "requirements, including functional, performance, interface and safety requirements.",
    ),
    (
        "5.3.3", "5.3.3", "Risk control in the architecture",
        "development",
        ["risk control", "architecture safety", "segregation"],
        ["5.3", "7.2"],
        None,
        "Where risk control measures are implemented in the software architecture (for example "
        "by segregating safety-critical software items), these measures shall be identified "
        "and documented and their effectiveness verified.",
    ),
    (
        "5.4", "5.4", "Software detailed design",
        "development",
        ["detailed design", "software units", "design"],
        ["5", "5.4.1", "5.4.2", "5.4.3"],
        None,
        "The software architecture shall be refined into a detailed design subdividing the "
        "software into software units and specifying their internal logic, interfaces and "
        "data structures. The detailed design shall be verified.",
    ),
    (
        "5.4.1", "5.4.1", "Subdivide into software units and document the design",
        "development",
        ["software units", "detailed design document"],
        ["5.4", "3.2"],
        None,
        "The software shall be subdivided into software units, and the detailed design of each "
        "unit shall be documented, describing its functions, algorithms, data structures and "
        "interfaces at a level sufficient to allow implementation and unit verification.",
    ),
    (
        "5.4.2", "5.4.2", "Verify the detailed design",
        "development",
        ["verify detailed design", "design review"],
        ["5.4", "5.4.1"],
        None,
        "The detailed design shall be verified to ensure it correctly implements the "
        "architecture and satisfies the allocated software requirements.",
    ),
    (
        "5.4.3", "5.4.3", "Risk control in the detailed design",
        "development",
        ["risk control", "detailed design safety"],
        ["5.4", "7.2"],
        None,
        "Where risk control measures are implemented in the detailed design, these measures "
        "shall be identified and documented and their effectiveness verified.",
    ),
    (
        "5.5", "5.5", "Software unit implementation and verification",
        "development",
        ["unit implementation", "unit testing", "unit verification", "coding"],
        ["5", "5.5.1", "5.5.2", "5.5.3", "5.5.4", "5.5.5"],
        None,
        "Each software unit shall be implemented and verified. Verification procedures shall "
        "be established, acceptance criteria defined, and unit verification performed before "
        "the unit is integrated.",
    ),
    (
        "5.5.1", "5.5.1", "Implement each software unit",
        "development",
        ["implement unit", "coding", "implementation"],
        ["5.5", "5.1.4"],
        None,
        "Each software unit shall be implemented according to the detailed design and the "
        "documented software development standards, methods and tools (clause 5.1.4).",
    ),
    (
        "5.5.2", "5.5.2", "Establish unit verification procedure",
        "development",
        ["unit verification procedure", "test procedure"],
        ["5.5", "5.1.6"],
        None,
        "A procedure shall be established to verify each software unit, defining how unit "
        "verification (for example unit testing) is performed and documented.",
    ),
    (
        "5.5.3", "5.5.3", "Software unit acceptance criteria",
        "development",
        ["acceptance criteria", "unit acceptance"],
        ["5.5"],
        None,
        "Acceptance criteria shall be defined for each software unit, against which the unit "
        "verification results are judged.",
    ),
    (
        "5.5.4", "5.5.4", "Additional unit verification criteria",
        "development",
        ["events", "data flow", "control flow", "unit criteria"],
        ["5.5", "5.5.3"],
        None,
        "Where applicable, unit verification shall additionally demonstrate that the unit "
        "handles proper and improper events correctly, processes data and control flow as "
        "specified, and that boundary and error conditions behave as required.",
    ),
    (
        "5.5.5", "5.5.5", "Verify the software unit",
        "development",
        ["verify unit", "unit test results"],
        ["5.5", "5.5.2", "5.5.3"],
        None,
        "Each software unit shall be verified using the established procedure, and the results "
        "and their conformance to the acceptance criteria shall be recorded.",
    ),
    (
        "5.6", "5.6", "Software integration and integration testing",
        "development",
        ["integration", "integration testing"],
        ["5", "5.6.1", "5.6.2", "5.6.3", "5.6.4", "5.6.5", "5.6.6", "5.6.7"],
        None,
        "Software units and software items shall be integrated according to the integration "
        "plan and integration testing shall be performed to verify that the integrated "
        "software works together as required.",
    ),
    (
        "5.6.1", "5.6.1", "Integration plan",
        "development",
        ["integration plan", "integration order"],
        ["5.6", "5.1.5"],
        None,
        "The order and approach of integration (for example top-down, bottom-up, or a defined "
        "build sequence) shall be planned so that integration proceeds in a controlled manner.",
    ),
    (
        "5.6.2", "5.6.2", "Integrate the software units",
        "development",
        ["integrate units", "build"],
        ["5.6", "5.6.1"],
        None,
        "Software units shall be integrated into software items and the software system "
        "according to the integration plan.",
    ),
    (
        "5.6.3", "5.6.3", "Verify integration",
        "development",
        ["verify integration", "integration test"],
        ["5.6", "5.1.6"],
        None,
        "Each integration step shall be verified, typically by integration testing, to confirm "
        "that the assembled components work together and that interfaces function correctly.",
    ),
    (
        "5.6.4", "5.6.4", "Integration testing content",
        "development",
        ["integration test content", "interfaces"],
        ["5.6", "5.6.3"],
        None,
        "Integration testing shall verify, as applicable, that data flows and control flows "
        "between integrated software items are correct, and that timing, synchronization and "
        "interfaces behave as specified.",
    ),
    (
        "5.6.5", "5.6.5", "Re-integrate after changes",
        "development",
        ["re-integration", "change", "regression"],
        ["5.6", "8.2"],
        None,
        "When software is changed, the affected units and items shall be re-integrated and "
        "re-tested as necessary, using the configuration management and change control "
        "processes to determine the scope of re-verification.",
    ),
    (
        "5.6.6", "5.6.6", "Integration testing records",
        "development",
        ["integration test records", "test records"],
        ["5.6", "5.6.3"],
        None,
        "Integration testing activities and results shall be documented, including the test "
        "environment, test cases, observed results and pass/fail disposition.",
    ),
    (
        "5.6.7", "5.6.7", "Regression testing in integration",
        "development",
        ["regression testing", "regression"],
        ["5.6", "5.6.5"],
        None,
        "Regression testing shall be applied as appropriate after changes, to verify that "
        "previously working functionality has not been broken by the modification.",
    ),
    (
        "5.7", "5.7", "Software system testing",
        "development",
        ["system testing", "system test", "software system test"],
        ["5", "5.7.1", "5.7.2", "5.7.3", "5.7.4", "5.7.5"],
        None,
        "Software system testing shall be performed to verify that the complete, integrated "
        "software meets the software requirements, including any risk control measures.",
    ),
    (
        "5.7.1", "5.7.1", "Test against the requirements",
        "development",
        ["system test requirements", "traceability"],
        ["5.7", "5.2"],
        None,
        "Software system testing shall verify that the software meets the documented software "
        "requirements (clause 5.2), demonstrating traceability between requirements and tests.",
    ),
    (
        "5.7.2", "5.7.2", "Test risk control measures",
        "development",
        ["risk control testing", "safety test"],
        ["5.7", "7.3", "5.2.4"],
        None,
        "Software system testing shall include tests that verify the effectiveness of risk "
        "control measures implemented in software, as identified by the software risk "
        "management process.",
    ),
    (
        "5.7.3", "5.7.3", "Test in simulated or real environment",
        "development",
        ["test environment", "simulated environment", "real environment"],
        ["5.7"],
        None,
        "Software system testing shall be performed in an environment that is appropriate to "
        "the intended use, which may be a simulated environment or, where necessary, the real "
        "environment (for example on the target hardware platform).",
    ),
    (
        "5.7.4", "5.7.4", "Verify system testing",
        "development",
        ["verify system test", "test review"],
        ["5.7", "5.1.6"],
        None,
        "Software system testing activities and results shall be verified for correctness, "
        "completeness and traceability to requirements.",
    ),
    (
        "5.7.5", "5.7.5", "Re-test after changes",
        "development",
        ["re-test", "regression", "change"],
        ["5.7", "5.6.5", "8.2"],
        None,
        "After changes, the software system shall be re-tested as necessary, including "
        "regression testing, to confirm that requirements continue to be met.",
    ),
    (
        "5.8", "5.8", "Software release",
        "development",
        ["software release", "release", "distribution"],
        ["5", "5.8.1", "5.8.2", "5.8.3", "5.8.4", "5.8.5", "5.8.6", "5.8.7", "5.8.8"],
        None,
        "The software shall be released in a controlled manner. The release process shall "
        "ensure that verification is complete, residual anomalies are documented, the software "
        "is evaluated against its requirements, released versions are identified, and the "
        "software is archived and delivered reliably.",
    ),
    (
        "5.8.1", "5.8.1", "Ensure verification is complete before release",
        "development",
        ["release verification", "pre-release check"],
        ["5.8", "5.1.6"],
        None,
        "Before release, the manufacturer shall ensure that all required verification "
        "activities for the software have been completed and that the software is suitable "
        "for release.",
    ),
    (
        "5.8.2", "5.8.2", "Document known residual anomalies",
        "development",
        ["residual anomalies", "known problems", "release notes"],
        ["5.8", "9"],
        None,
        "Any known residual anomalies in the software shall be documented, including their "
        "known impact and any workarounds, so that users and the organization are aware of "
        "them at release.",
    ),
    (
        "5.8.3", "5.8.3", "Evaluate the released software against requirements",
        "development",
        ["evaluate release", "requirements evaluation"],
        ["5.8", "5.7"],
        None,
        "The released software shall be evaluated against the documented software requirements "
        "to confirm that it meets its intended use before distribution.",
    ),
    (
        "5.8.4", "5.8.4", "Document the released versions",
        "development",
        ["released version", "version identification"],
        ["5.8", "8.1"],
        None,
        "The versions of the software being released, and of the supporting items, shall be "
        "documented and uniquely identified (see configuration identification, clause 8.1).",
    ),
    (
        "5.8.5", "5.8.5", "Document how the released software was created",
        "development",
        ["build documentation", "reproducibility", "release creation"],
        ["5.8", "8.1"],
        None,
        "The method by which the released software was created (for example the build "
        "procedure, environment, and inputs) shall be documented so that the release is "
        "traceable and reproducible.",
    ),
    (
        "5.8.6", "5.8.6", "Ensure activities and tasks are complete",
        "development",
        ["complete activities", "release checklist"],
        ["5.8"],
        None,
        "The manufacturer shall ensure that all required development activities and tasks have "
        "been completed prior to release, in accordance with the development plan.",
    ),
    (
        "5.8.7", "5.8.7", "Archive the software",
        "development",
        ["archive", "retention", "release archive"],
        ["5.8", "8.1"],
        None,
        "The released software and its associated documentation shall be archived in a "
        "controlled manner, with retention appropriate to the product's lifetime and "
        "regulatory requirements.",
    ),
    (
        "5.8.8", "5.8.8", "Provide a reliable means to deliver the released software",
        "development",
        ["delivery", "distribution", "deployment"],
        ["5.8", "5.8.4"],
        None,
        "A reliable means shall be provided to deliver the released software to its intended "
        "environment, ensuring the correct version reaches the field.",
    ),
    # ---------------------------------------------------------------- Clause 6
    (
        "6", "6", "Software maintenance process",
        "maintenance",
        ["maintenance process", "maintenance", "change after release"],
        ["6.1", "6.2", "6.3", "5.8"],
        None,
        "Clause 6 defines the SOFTWARE MAINTENANCE PROCESS, covering the establishment of a "
        "maintenance plan, problem and modification analysis, and the implementation of "
        "modifications after the software has been released.",
    ),
    (
        "6.1", "6.1", "Establish a software maintenance plan",
        "maintenance",
        ["maintenance plan", "service"],
        ["6", "5.1.1"],
        None,
        "A software maintenance plan shall be established, describing how post-release "
        "feedback, problems and modifications will be handled, including resources and "
        "responsibilities for maintenance.",
    ),
    (
        "6.2", "6.2", "Problem and modification analysis",
        "maintenance",
        ["problem analysis", "modification analysis", "feedback"],
        ["6", "6.2.1", "6.2.2", "6.2.3", "6.2.4"],
        None,
        "Feedback on the released software (including problems) shall be analysed and "
        "evaluated to determine whether and how the software should be modified.",
    ),
    (
        "6.2.1", "6.2.1", "Document feedback and problem reports",
        "maintenance",
        ["feedback", "problem report"],
        ["6.2", "9.1"],
        None,
        "Feedback and problem reports relating to the released software shall be documented.",
    ),
    (
        "6.2.2", "6.2.2", "Evaluate the impact of feedback",
        "maintenance",
        ["impact analysis", "evaluate feedback"],
        ["6.2", "7.4"],
        None,
        "The impact of each problem or modification request on the software, its safety "
        "classification, risk and on released versions shall be evaluated.",
    ),
    (
        "6.2.3", "6.2.3", "Use change control for modifications",
        "maintenance",
        ["change control", "modification"],
        ["6.2", "8.2"],
        None,
        "Decisions to modify the software shall be handled through the change control process "
        "(clause 8.2).",
    ),
    (
        "6.2.4", "6.2.4", "Communicate with relevant parties",
        "maintenance",
        ["communication", "relevant parties", "notification"],
        ["6.2", "9.3"],
        None,
        "The outcome of the analysis shall be communicated to the relevant parties, including "
        "users and regulatory parties where applicable.",
    ),
    (
        "6.3", "6.3", "Implementing modifications",
        "maintenance",
        ["implement modification", "re-release", "patch"],
        ["6", "6.3.1", "6.3.2", "8.2"],
        None,
        "Modifications shall be implemented using an established process, and the modified "
        "software shall be re-released in a controlled manner.",
    ),
    (
        "6.3.1", "6.3.1", "Use an established process to implement modifications",
        "maintenance",
        ["established process", "modification process"],
        ["6.3", "8.2"],
        None,
        "Modifications shall be implemented using a defined process (for example by re-entering "
        "the applicable activities of the development process, clause 5) that ensures the "
        "modification is planned, implemented, verified and documented.",
    ),
    (
        "6.3.2", "6.3.2", "Re-release the modified software",
        "maintenance",
        ["re-release", "release modification"],
        ["6.3", "5.8"],
        None,
        "The modified software shall be re-released through the software release process "
        "(clause 5.8), including appropriate re-verification and documentation of the changes.",
    ),
    # ---------------------------------------------------------------- Clause 7
    (
        "7", "7", "Software risk management process",
        "risk",
        ["software risk management", "risk management process", "risk control"],
        ["7.1", "7.2", "7.3", "7.4", "4.2"],
        None,
        "Clause 7 defines the SOFTWARE RISK MANAGEMENT PROCESS, extending ISO 14971 to software: "
        "(7.1) analysis of software contributing to hazardous situations; (7.2) risk control "
        "measures; (7.3) verification of risk control measures; and (7.4) risk management of "
        "software changes.",
    ),
    (
        "7.1", "7.1", "Analysis of software contributing to hazardous situations",
        "risk",
        ["hazardous situation", "software hazard", "risk analysis"],
        ["7", "4.2", "4.3"],
        None,
        "The manufacturer shall identify the potential hazardous situations and analyse how "
        "software (including failures and incorrect behaviour) could contribute to them. This "
        "analysis feeds the determination of the software safety classification (clause 4.3).",
    ),
    (
        "7.2", "7.2", "Risk control measures",
        "risk",
        ["risk control measures", "mitigation", "risk reduction"],
        ["7", "5.2.4", "5.3.3", "5.4.3"],
        None,
        "Risk control measures shall be defined for software-related risks. These measures "
        "shall be allocated to software requirements (clause 5.2.4) and implemented in the "
        "architecture (5.3.3) and detailed design (5.4.3) as applicable.",
    ),
    (
        "7.3", "7.3", "Verification of risk control measures",
        "risk",
        ["verify risk control", "safety verification", "effectiveness"],
        ["7", "5.7.2", "5.5"],
        None,
        "The effectiveness of risk control measures implemented in software shall be verified, "
        "for example through unit, integration and system testing, and the results documented.",
    ),
    (
        "7.4", "7.4", "Risk management of software changes",
        "risk",
        ["software change risk", "change risk", "re-evaluate risk"],
        ["7", "7.4.1", "7.4.2", "8.2"],
        None,
        "Changes to the software shall be analysed for their impact on risk. The contribution "
        "of the changed software to hazardous situations shall be re-evaluated, and risk "
        "control measures re-verified as necessary.",
    ),
    (
        "7.4.1", "7.4.1", "Analyse the impact of software changes",
        "risk",
        ["impact of change", "change analysis"],
        ["7.4", "6.2.2"],
        None,
        "Each software change shall be analysed to determine whether it could introduce new "
        "hazards or affect existing risk control measures.",
    ),
    (
        "7.4.2", "7.4.2", "Re-evaluate severity and probability",
        "risk",
        ["re-evaluate risk", "severity", "probability"],
        ["7.4", "7.1"],
        None,
        "Where a change affects safety, the severity and probability of harm associated with "
        "the affected hazardous situations shall be re-evaluated, and the software safety "
        "classification re-confirmed if necessary.",
    ),
    # ---------------------------------------------------------------- Clause 8
    (
        "8", "8", "Software configuration management process",
        "configuration",
        ["configuration management", "scm", "version control"],
        ["8.1", "8.2", "8.3", "5.1.9"],
        None,
        "Clause 8 defines the SOFTWARE CONFIGURATION MANAGEMENT PROCESS: (8.1) configuration "
        "identification; (8.2) change control; and (8.3) configuration status accounting.",
    ),
    (
        "8.1", "8.1", "Configuration identification",
        "configuration",
        ["configuration identification", "baseline", "version"],
        ["8", "5.8.4", "5.1.10"],
        None,
        "Configuration items (including software, documentation and supporting items) shall be "
        "uniquely identified, and baselines established to mark controlled configurations at "
        "defined points in the life cycle.",
    ),
    (
        "8.2", "8.2", "Change control",
        "configuration",
        ["change control", "change request", "approval"],
        ["8", "6.2.3", "5.6.5", "9.4"],
        None,
        "A change control process shall be established so that changes to configuration items "
        "are requested, evaluated, approved or rejected, implemented and documented in a "
        "controlled manner.",
    ),
    (
        "8.3", "8.3", "Configuration status accounting",
        "configuration",
        ["status accounting", "configuration status", "history"],
        ["8", "8.1", "8.2"],
        None,
        "Configuration status accounting shall maintain records of the configuration items, "
        "their versions, and the status of changes, so that the configuration and its history "
        "can be reported at any time.",
    ),
    # ---------------------------------------------------------------- Clause 9
    (
        "9", "9", "Software problem resolution process",
        "problem",
        ["problem resolution", "defect", "bug", "problem report"],
        ["9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7", "9.8"],
        None,
        "Clause 9 defines the SOFTWARE PROBLEM RESOLUTION PROCESS: preparing problem reports, "
        "investigating problems, advising relevant parties, using change control, maintaining "
        "records, analysing trends, verifying resolution and documenting test content.",
    ),
    (
        "9.1", "9.1", "Prepare problem reports",
        "problem",
        ["problem report", "report problem", "issue report"],
        ["9", "6.2.1"],
        None,
        "Problems found in the software shall be recorded in problem reports that describe the "
        "problem, its circumstances, and information needed to investigate it.",
    ),
    (
        "9.2", "9.2", "Investigate the problem",
        "problem",
        ["investigate problem", "root cause"],
        ["9", "9.1"],
        None,
        "Each problem shall be investigated to determine its cause and potential impact, and "
        "to evaluate possible corrective actions.",
    ),
    (
        "9.3", "9.3", "Advise relevant parties",
        "problem",
        ["advise parties", "notification", "escalation"],
        ["9", "6.2.4"],
        None,
        "Relevant parties shall be advised of the problem and its status as appropriate, "
        "including the safety implications if the problem is safety-related.",
    ),
    (
        "9.4", "9.4", "Use the change control process",
        "problem",
        ["change control", "corrective action"],
        ["9", "8.2"],
        None,
        "Actions to correct the problem shall be handled through the change control process "
        "(clause 8.2).",
    ),
    (
        "9.5", "9.5", "Maintain records",
        "problem",
        ["records", "problem records", "documentation"],
        ["9", "9.1"],
        None,
        "Records of problem reports, investigations and their resolution shall be maintained.",
    ),
    (
        "9.6", "9.6", "Analyse problems for trends",
        "problem",
        ["trend analysis", "trends", "metrics"],
        ["9", "9.5"],
        None,
        "Problems shall be analysed for trends, so that systemic issues can be detected and "
        "addressed proactively.",
    ),
    (
        "9.7", "9.7", "Verify software problem resolution",
        "problem",
        ["verify resolution", "verify fix"],
        ["9", "9.4", "5.5", "5.6", "5.7"],
        None,
        "The resolution of each problem shall be verified, for example by re-verification or "
        "regression testing, to confirm the problem is corrected and no new issues are "
        "introduced.",
    ),
    (
        "9.8", "9.8", "Test documentation contents",
        "problem",
        ["test documentation", "test content", "problem test"],
        ["9", "9.7"],
        None,
        "Problem resolution documentation shall include, as applicable, the tests or "
        "verification used to confirm the resolution, so that the verification is traceable.",
    ),
    # ---------------------------------------------------- Cross-cutting concepts
    (
        "traceability", "traceability", "Traceability",
        "concept",
        ["traceability", "traceability matrix", "requirements traceability"],
        ["5.2", "5.7.1", "5.8.3"],
        None,
        "Traceability is the ability to link related work products across the life cycle: for "
        "example from software requirements (5.2) to architecture (5.3), detailed design "
        "(5.4), code (5.5), integration tests (5.6) and system tests (5.7), and onward to "
        "risk control measures (7.2). A traceability matrix is a common tool to demonstrate "
        "these links.",
    ),
    (
        "vmodel", "v-model", "V-model life cycle",
        "concept",
        ["v-model", "v model", "life cycle model", "verification"],
        ["5", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7"],
        None,
        "The V-model is a widely used software life cycle model that maps IEC 62304 activities "
        "onto a 'V': the descending side is specification and design (requirements 5.2, "
        "architecture 5.3, detailed design 5.4), the bottom is coding (5.5), and the ascending "
        "side is verification and validation (unit 5.5, integration 5.6, system 5.7), with each "
        "verification level tracing back to its corresponding specification level.",
    ),
    (
        "soup", "SOUP", "Software of unknown provenance (SOUP)",
        "concept",
        ["soup", "software of unknown provenance", "third party", "cots", "off-the-shelf"],
        ["4.4", "5.1.10", "8.1"],
        None,
        "SOUP (Software of Unknown Provenance) is software already developed and generally "
        "available that was not developed for the purpose of being incorporated into the "
        "medical device, or software for which adequate development records are unavailable. "
        "SOUP items shall be identified, evaluated for their intended use, safety classified "
        "where relevant, and brought under configuration management (see clauses 4.4, 5.1.10 "
        "and 8.1).",
    ),
    (
        "verification-validation", "verification/validation", "Verification vs. validation",
        "concept",
        ["verification", "validation", "v&v", "difference"],
        ["5.5", "5.6", "5.7", "5.8.3"],
        None,
        "VERIFICATION confirms that the software meets its specified requirements ('did we "
        "build it right?'), performed through review, analysis and testing at unit, integration "
        "and system levels. VALIDATION (in the broader medical device context) confirms the "
        "device meets user needs and intended use ('did we build the right thing?'). IEC 62304 "
        "focuses on verification activities within the software life cycle.",
    ),
]


def build_entries() -> list[KnowledgeEntry]:
    """Convert the raw tuples into validated :class:`KnowledgeEntry` objects."""
    entries: list[KnowledgeEntry] = []
    for raw in _RAW:
        _id, clause, title, category, keywords, related, safety_class, content = raw
        entries.append(
            KnowledgeEntry(
                id=_id,
                clause=clause,
                title=title,
                content=content,
                category=category,
                keywords=keywords,
                related=related,
                safety_class=safety_class,
            )
        )
    return entries


BUILTIN_ENTRIES: list[KnowledgeEntry] = build_entries()

# Index helpers ---------------------------------------------------------------

_ENTRY_BY_ID: dict[str, KnowledgeEntry] = {e.id: e for e in BUILTIN_ENTRIES}
_ENTRY_BY_CLAUSE: dict[str, KnowledgeEntry] = {e.clause: e for e in BUILTIN_ENTRIES}

# Safety class summaries ------------------------------------------------------

SAFETY_CLASSES: dict[str, dict] = {
    "A": {
        "safety_class": "A",
        "description": "No injury or damage to health is possible from a software failure.",
        "risk_criterion": (
            "A failure of the software system cannot result in any injury or damage to health."
        ),
        "applicable_clauses": ["4.3", "5", "5.1.7"],
    },
    "B": {
        "safety_class": "B",
        "description": "Non-serious injury is possible from a software failure.",
        "risk_criterion": (
            "A failure of the software system could result in non-serious injury."
        ),
        "applicable_clauses": ["4.3", "5", "5.1.7", "7"],
    },
    "C": {
        "safety_class": "C",
        "description": "Death or serious injury is possible from a software failure.",
        "risk_criterion": (
            "A failure of the software system could result in death or serious injury."
        ),
        "applicable_clauses": ["4.3", "5", "5.1.7", "7"],
    },
}


def get_entry(entry_id: str) -> KnowledgeEntry | None:
    """Return an entry by its stable id (e.g. '5.1.3') or by clause reference."""
    return _ENTRY_BY_ID.get(entry_id) or _ENTRY_BY_CLAUSE.get(entry_id)


def get_all_entries() -> list[KnowledgeEntry]:
    return list(BUILTIN_ENTRIES)


__all__ = [
    "BUILTIN_ENTRIES",
    "SAFETY_CLASSES",
    "build_entries",
    "get_entry",
    "get_all_entries",
]
