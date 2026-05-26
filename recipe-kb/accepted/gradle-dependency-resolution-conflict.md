---
id: gradle-dependency-resolution-conflict
kind: debug-recipe
status: accepted
stack:
- android
- kotlin
- gradle
failure_class: gradle/dependencies
symptoms:
- Gradle build fails because of conflicting transitive dependency versions that cannot
  be resolved
fingerprints:
- dependency resolution
- dependency conflict
- Could not resolve
- Conflict with dependency
- requested version
first_checks:
- Run gradle dependencies or the Dependencies view to see the full transitive tree
- Check whether a resolutionStrategy block forces a particular version
- Check whether the conflict is between implementation and test classpath variants
do_not:
- Do not add exclude rules globally; scope excludes to the minimum affected configuration
- Do not force a version without first understanding whether the forced version is
  API-compatible
evidence_needed:
- Capture the full dependency tree output showing the conflict
- Identify which module versions are incompatible and why
minimal_fix_scope:
- The build.gradle(.kts) dependency declaration or resolutionStrategy block
- The dependency configuration (implementation, api, testImplementation) with the
  conflict
validation_ladder:
- Run gradle dependencies and locate the conflicting transitive path
- Apply a resolutionStrategy or version pin that resolves the conflict
- Run the Gradle build and the affected module tests
regression_guard:
- Add a dependency-lock check or resolution strategy test to the build pipeline
evidence_refs:
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-24
  short_excerpt: Debugging dependency resolution
  quote_hash: sha256:b84b2c44f56fa0c55b2d8c86532abc06fa3e8181db521253360a8f5cd0628ef8
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# gradle-dependency-resolution-conflict

## Failure Class
gradle/dependencies

## Symptoms
- Gradle build fails because of conflicting transitive dependency versions that cannot be resolved

## Fingerprints
- dependency resolution
- dependency conflict
- Could not resolve
- Conflict with dependency
- requested version

## First Checks
- Run gradle dependencies or the Dependencies view to see the full transitive tree
- Check whether a resolutionStrategy block forces a particular version
- Check whether the conflict is between implementation and test classpath variants

## Do Not Patch Yet
- Do not add exclude rules globally; scope excludes to the minimum affected configuration
- Do not force a version without first understanding whether the forced version is API-compatible

## Evidence Needed
- Capture the full dependency tree output showing the conflict
- Identify which module versions are incompatible and why

## Minimal Fix Scope
- The build.gradle(.kts) dependency declaration or resolutionStrategy block
- The dependency configuration (implementation, api, testImplementation) with the conflict

## Validation Ladder
- Run gradle dependencies and locate the conflicting transitive path
- Apply a resolutionStrategy or version pin that resolves the conflict
- Run the Gradle build and the affected module tests

## Regression Guard
- Add a dependency-lock check or resolution strategy test to the build pipeline

## Reviewer Notes
