---
id: gradle-java-home-invalid
kind: debug-recipe
status: accepted
stack:
- android
- kotlin
- gradle
failure_class: gradle/environment
symptoms:
- 'Gradle build fails with ERROR: JAVA_HOME is set to an invalid directory'
fingerprints:
- JAVA_HOME is set to an invalid directory
- 'ERROR: JAVA_HOME'
- please set JAVA_HOME
- Java Development Kit
first_checks:
- Check echo $JAVA_HOME to verify the directory exists
- Check whether JAVA_HOME points to the JDK root (not bin/ or jre/)
- Check whether the JDK version matches the Gradle project's required compatibility
do_not:
- Do not unset JAVA_HOME entirely; Gradle requires it to be set explicitly
- Do not point JAVA_HOME at a JRE if the project needs a full JDK
evidence_needed:
- Capture the JAVA_HOME environment variable value
- Capture the Gradle error message showing the invalid directory path
minimal_fix_scope:
- The JAVA_HOME environment variable configuration
- The shell profile or CI environment that sets JAVA_HOME
validation_ladder:
- Run echo $JAVA_HOME and verify the directory exists and contains bin/javac
- Run gradle --version and verify it reports the expected Java version
- Run the Gradle build smoke test
regression_guard:
- Add a CI check that validates JAVA_HOME before running Gradle builds
evidence_refs:
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-12
  short_excerpt: JAVA_HOME is set to an invalid directory
  quote_hash: sha256:58f8df38a60a2bdff6460224308765160c58ca39423b319137c2d85ec1b0255e
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-14
  short_excerpt: 'ERROR: JAVA_HOME is set to an invalid directory'
  quote_hash: sha256:e7a18b2353a33075f864766a10e86b11ef5bf17e5be298abe7061ca5c6865ab7
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-15
  short_excerpt: 'Set the JAVA_HOME variable in your environment to match the location
    of your Java installation:'
  quote_hash: sha256:31693bd2ce030ce9ec4892820723a06822bdb988189067154d128a29508b51a1
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-16
  short_excerpt: $ export JAVA_HOME=/Users/user/Library/Java/JavaVirtualMachines/corretto-22.0.1/Contents/Home
    $ echo $JAVA_HOME
  quote_hash: sha256:289f34c5d5d03ceec026b476a2f42086facd23a7c39f6e79954726a89fa82f8f
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-18
  short_excerpt: You must ensure that a Java Development Kit version 17 or higher
    is properly installed , the JAVA_HOME environment variable is set, and Java is
    added to your PATH .
  quote_hash: sha256:cb688c36c7d5b2215dc84571d6090d77d3b5eac5ece2c9c25c1935d14e172b18
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# gradle-java-home-invalid

## Failure Class
gradle/environment

## Symptoms
- Gradle build fails with ERROR: JAVA_HOME is set to an invalid directory

## Fingerprints
- JAVA_HOME is set to an invalid directory
- ERROR: JAVA_HOME
- please set JAVA_HOME
- Java Development Kit

## First Checks
- Check echo $JAVA_HOME to verify the directory exists
- Check whether JAVA_HOME points to the JDK root (not bin/ or jre/)
- Check whether the JDK version matches the Gradle project's required compatibility

## Do Not Patch Yet
- Do not unset JAVA_HOME entirely; Gradle requires it to be set explicitly
- Do not point JAVA_HOME at a JRE if the project needs a full JDK

## Evidence Needed
- Capture the JAVA_HOME environment variable value
- Capture the Gradle error message showing the invalid directory path

## Minimal Fix Scope
- The JAVA_HOME environment variable configuration
- The shell profile or CI environment that sets JAVA_HOME

## Validation Ladder
- Run echo $JAVA_HOME and verify the directory exists and contains bin/javac
- Run gradle --version and verify it reports the expected Java version
- Run the Gradle build smoke test

## Regression Guard
- Add a CI check that validates JAVA_HOME before running Gradle builds

## Reviewer Notes
