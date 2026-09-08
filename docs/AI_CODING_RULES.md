# BioHub — AI Coding Rules

These rules apply to AI coding agents working on the BioHub repository.

---

# 1. Before Any Change

Before modifying code:

1. Read `docs/PROJECT_STATE.md`.
2. Read `docs/PROJECT_SPECIFICATION.md`.
3. Read `docs/ARCHITECTURE.md` if relevant.
4. Read `docs/DECISIONS.md`.
5. Inspect the existing repository.
6. Inspect the files relevant to the requested task.
7. Identify dependencies and existing implementations.
8. Do not assume that a requested feature does not already exist.

---

# 2. Scope Control

Implement ONLY the requested task.

Do not:

* Build future modules
* Rewrite unrelated code
* Change architecture without approval
* Replace working libraries without justification
* Add unnecessary dependencies
* Refactor unrelated files

---

# 3. Existing Code

Before creating a new implementation:

* Search for existing functionality.
* Reuse existing utilities where appropriate.
* Avoid duplicate classes/functions/components.
* Preserve working behavior unless the task explicitly requires a change.

---

# 4. Architecture

Respect the architecture documented in:

`docs/ARCHITECTURE.md`

If implementation requires a significant architectural change:

STOP and report:

* What needs to change
* Why it needs to change
* Alternatives
* Impact
* Recommended solution

Do not silently make the architectural change.

---

# 5. Database

Do not silently modify:

* Tables
* Columns
* Relationships
* Constraints
* Indexes

Any meaningful database change must be documented and reflected in the appropriate migration/schema documentation.

Never delete production-style data merely to make a test pass.

---

# 6. API Contracts

Do not silently change an existing API contract.

If an endpoint changes:

* Request schema
* Response schema
* HTTP method
* URL
* Authentication
* Error format

then identify the impact on the frontend and documentation.

---

# 7. Sample ID

BioHub uses Sample ID / Experiment ID as the central integration mechanism.

Do not create unrelated identifiers that break module integration without a clear reason.

---

# 8. Biological Data

Never invent biological results.

Never claim:

* Laboratory measurements
* Clinical results
* Experimental results
* Model accuracy
* Dataset statistics

unless they were actually obtained and verified.

---

# 9. Raw Files

Never silently overwrite original uploaded biological files.

Maintain separation between:

RAW DATA

and

PROCESSED DATA.

---

# 10. Machine Learning

Never fabricate model performance.

Do not report:

* Accuracy
* Precision
* Recall
* F1
* ROC-AUC
* Confusion matrices

until they have actually been calculated.

Avoid data leakage.

Do not use the test set to tune the final model.

---

# 11. Security

Never:

* Hard-code passwords
* Hard-code API keys
* Commit secrets
* Disable security validation merely to make development easier
* Trust uploaded filenames
* Trust user input blindly

Use environment variables for secrets.

---

# 12. Dependencies

Before adding a dependency:

1. Determine whether the functionality already exists.
2. Check whether the dependency is maintained.
3. Check compatibility with the project.
4. Prefer established libraries.
5. Add only what is necessary.

For current library/API questions, verify official documentation when appropriate.

---

# 13. File Uploads

Validate:

* File type
* File size
* Filename
* Path
* Content where appropriate

Do not trust the file extension alone.

---

# 14. Error Handling

Errors should be:

* Controlled
* Understandable
* Logged appropriately
* Safe for users

Do not expose secrets, stack traces, or sensitive internal information unnecessarily.

---

# 15. Testing

After meaningful changes:

1. Run relevant tests.
2. Run lint/type checks where configured.
3. Run the application if appropriate.
4. Verify the requested functionality.
5. Report failures honestly.

Never say "tests passed" without actually running them.

---

# 16. Documentation

After completing a meaningful task:

Update relevant documentation.

At minimum, update:

`docs/PROJECT_STATE.md`

Include:

* What was implemented
* Files changed
* Tests performed
* Known issues
* Current status
* Next task

Update `CHANGELOG.md` when that file exists and the change is significant.

---

# 17. Git

Keep changes logically organized.

Do not:

* Commit secrets
* Commit huge datasets unnecessarily
* Commit temporary files
* Commit generated caches
* Rewrite Git history without explicit approval

---

# 18. AI Communication

Before implementation, briefly state:

* Understanding of task
* Files expected to change
* Potential risks

After implementation, report:

```text
Task:
Status:

Files created:
-

Files modified:
-

Dependencies:
-

Tests:
-

Verification:
-

Known issues:
-

Documentation updated:
-

Recommended next task:
-
```

---

# 19. When Requirements Are Ambiguous

Do not invent an important requirement.

If clarification is genuinely necessary:

1. Explain exactly what is unclear.
2. Give the relevant options.
3. Explain the trade-off.
4. Ask for the smallest necessary decision.

If the ambiguity is minor and a safe default exists, use the default and document the assumption.

---

# 20. When Something Is Technically Wrong

Do not implement a technically incorrect request merely because it was requested.

Explain:

* Why it is incorrect
* What could break
* Better alternatives
* Recommended implementation

---

# 21. Completion Rule

A task is NOT complete merely because code exists.

A task is complete only when:

* Implementation exists
* Relevant tests run
* Expected behavior is verified
* Documentation is updated
* Known limitations are recorded

---

# 22. Final Principle

Optimize for:

Technical correctness

>

Scientific honesty

>

Maintainability

>

Security

>

Testability

>

Simplicity

>

Development speed

Never optimize for "looks impressive" at the expense of correctness.
