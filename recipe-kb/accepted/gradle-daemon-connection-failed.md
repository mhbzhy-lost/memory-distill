---
id: gradle-daemon-connection-failed
kind: debug-recipe
status: accepted
stack:
- android
- kotlin
- gradle
failure_class: gradle/daemon
symptoms:
- Gradle build fails because a new daemon was started but could not be connected to
fingerprints:
- A new daemon was started but could not be connected to
- Gradle Daemon
- could not reuse
- Starting a Gradle Daemon
first_checks:
- Check gradle --status to see existing daemon processes
- Check whether a firewall or NAT masquerade is blocking the daemon connection
- Check whether gradle.properties has org.gradle.jvmargs that conflict with available
  memory
do_not:
- Do not disable the daemon with --no-daemon as a permanent fix; diagnose the connection
  issue first
- Do not kill Gradle daemon processes without first checking whether another project
  is sharing them
evidence_needed:
- Capture the full Gradle daemon startup failure message
- Check gradle --status output for existing daemons
minimal_fix_scope:
- The Gradle daemon configuration in gradle.properties
- The system firewall or network settings blocking daemon connection
validation_ladder:
- Run gradle --stop and retry the build
- Verify gradle --status shows a healthy daemon process
- Run the Gradle build smoke test
regression_guard:
- Add a CI pre-build step that runs gradle --stop to clean stale daemons
evidence_refs:
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-8
  short_excerpt: '------------------------------------------------------------ Gradle
    {gradleVersion} ------------------------------------------------------------ Build
    time: 2025-05-13 06:56:13 UTC Revision: 3c890746756262d3778e12eaa5155d661d7cbdf2
    Kotlin: 2.1.21 Groovy: 4.0.28 Ant: Apache Ant(TM) version 1.10.15 compiled on
    August 25 2024 Launcher JVM: 22.0.1 (Oracle Corporation 22.0.1+8-16) Daemon JVM:
    Compatible with Java 17, any vendor, nativeImageCapable=false (from gradle/gradle-daemon-jvm.properties)
    OS: Mac OS X 15.5 aarch64'
  quote_hash: sha256:df9d119e978843f380892acf75ecbe2307bf6296e1ddd7a13196ef3150cb358e
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-42
  short_excerpt: $ GRADLE_USER_HOME /daemon/9.5.1/
  quote_hash: sha256:4d8d2297b3e0fd7f8547998c01d1d85992f443d8decc3d5abed2939e2eeeea11
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-52
  short_excerpt: Troubleshooting daemon connection issues
  quote_hash: sha256:c22bd5283a35c1f1797053954e8e885c6ebdf6027e0ee848f74f488af9edad5f
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-53
  short_excerpt: 'If your Gradle build fails before running any tasks, you may be
    encountering network configuration problems. When Gradle is unable to communicate
    with the Gradle daemon process, the build will immediately fail with a message
    similar to this:'
  quote_hash: sha256:9351c47697c962b118a99b67ac661f8e7314bb5e7f4e33d263d74006a15b1f93
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-55
  short_excerpt: 'Starting a Gradle Daemon, 1 stopped Daemon could not be reused,
    use --status for details FAILURE: Build failed with an exception. * What went
    wrong: A new daemon was started but could not be connected to: pid=DaemonInfo{pid=55913,
    address=[7fb34c82-1907-4c32-afda-888c9b6e2279 port:42751, addresses:[/127.0.0.1]],
    state=Busy, ...'
  quote_hash: sha256:f282e5572562a6998b3798e9768c2492ea6c1ddde91546ce3ea8884f9c0544a6
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-58
  short_excerpt: You can monitor the detected network setup and the connection requests
    in the daemon log file ( $ GRADLE_USER_HOME /daemon/<Gradle version>/daemon-<PID>.out.log
    ).
  quote_hash: sha256:6311ecd064081a203e7593585803f1b0773870b9d35013267801e9238cf3de25
- source_id: gradle-build-troubleshooting
  url: https://docs.gradle.org/current/userguide/troubleshooting.html
  final_url: https://docs.gradle.org/current/userguide/troubleshooting.html
  source_type: build_tool_doc
  captured_at: '2026-05-26T10:27:19.494775Z'
  section_anchor: root
  span_id: gradle-build-troubleshooting-59
  short_excerpt: 2021-08-12T12:01:50.755+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses]
    Adding IP addresses for network interface enp0s3 2021-08-12T12:01:50.759+0200
    [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Is this a loopback
    interface? false 2021-08-12T12:01:50.769+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses]
    Adding remote address /fe80:0:0:0:85ba:3f3e:1b88:c0e1%enp0s3 2021-08-12T12:01:50.770+0200
    [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding remote
    address /10.0.2.15 2021-08-12T12:01:50.770+0200 [DEBUG] [org.gra
  quote_hash: sha256:da233f88566596d59b90785fc56e270529d7af3940be61919233291a0b9b5f5f
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# gradle-daemon-connection-failed

## Failure Class
gradle/daemon

## Symptoms
- Gradle build fails because a new daemon was started but could not be connected to

## Fingerprints
- A new daemon was started but could not be connected to
- Gradle Daemon
- could not reuse
- Starting a Gradle Daemon

## First Checks
- Check gradle --status to see existing daemon processes
- Check whether a firewall or NAT masquerade is blocking the daemon connection
- Check whether gradle.properties has org.gradle.jvmargs that conflict with available memory

## Do Not Patch Yet
- Do not disable the daemon with --no-daemon as a permanent fix; diagnose the connection issue first
- Do not kill Gradle daemon processes without first checking whether another project is sharing them

## Evidence Needed
- Capture the full Gradle daemon startup failure message
- Check gradle --status output for existing daemons

## Minimal Fix Scope
- The Gradle daemon configuration in gradle.properties
- The system firewall or network settings blocking daemon connection

## Validation Ladder
- Run gradle --stop and retry the build
- Verify gradle --status shows a healthy daemon process
- Run the Gradle build smoke test

## Regression Guard
- Add a CI pre-build step that runs gradle --stop to clean stale daemons

## Reviewer Notes
