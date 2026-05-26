---
id: react-native-metro-port-8081
kind: debug-recipe
status: accepted
stack:
- react-native
failure_class: react-native/metro-bundler
symptoms:
- Metro bundler fails to start because another process is already listening on port
  8081
fingerprints:
- port 8081
- Port already in use
- Metro bundler
- lsof -i :8081
first_checks:
- Check whether another process is occupying port 8081 using sudo lsof -i :8081
- Check whether a stale Metro process is still running from a previous session
- Check whether you can start Metro on a different port to bypass the conflict
do_not:
- Do not reboot the machine as the first fix; terminating the occupying process is
  faster and safer
- Do not change the default port permanently without documenting the change for the
  team
evidence_needed:
- Capture the output of lsof -i :8081 showing the PID of the occupying process
- Confirm Metro actually fails on port binding, not another error
minimal_fix_scope:
- The Metro bundler process startup invocation
- The port configuration in the project's metro.config.js or start command
validation_ladder:
- Kill the occupying process and verify Metro starts on port 8081
- Verify the app connects to the Metro bundler and hot reloads
- Run the dev server smoke test
regression_guard:
- Add a CI pre-check script that reports stale Metro processes before builds
evidence_refs:
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-2
  short_excerpt: Port already in use ​
  quote_hash: sha256:74e01cfbd4e93dbdee6b078762674654ec4f9d2daca3eafd662ff9d016f5e771
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-3
  short_excerpt: The Metro bundler runs on port 8081. If another process is already
    using that port, you can either terminate that process, or change the port that
    the bundler uses.
  quote_hash: sha256:0156a0c97f357dc95fa825ace331755d2452994300309030b61695ff99fdf461
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-4
  short_excerpt: 'Run the following command to find the id for the process that is
    listening on port 8081:'
  quote_hash: sha256:ff99684d14ef0ce2c448f7d0d65f55820ab122c089663c78513262603ef6ea62
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-5
  short_excerpt: sudo lsof -i :8081
  quote_hash: sha256:8ffd367f2ab66c6eb02818737b610998c0661454753569c74f2b8216365a0b0a
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-8
  short_excerpt: On Windows you can find the process using port 8081 using Resource
    Monitor and stop it using Task Manager.
  quote_hash: sha256:2fd94b48fffc3e44ea25288ce6dba9ca5f1b0fc5571d84934615bd709ecd2ac7
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-12
  short_excerpt: npm start -- --port = 8088
  quote_hash: sha256:f71465c97bfa4231cd8e52840a5b059a9cebdc635262dba1907c3c9fad15c84e
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-native-metro-port-8081

## Failure Class
react-native/metro-bundler

## Symptoms
- Metro bundler fails to start because another process is already listening on port 8081

## Fingerprints
- port 8081
- Port already in use
- Metro bundler
- lsof -i :8081

## First Checks
- Check whether another process is occupying port 8081 using sudo lsof -i :8081
- Check whether a stale Metro process is still running from a previous session
- Check whether you can start Metro on a different port to bypass the conflict

## Do Not Patch Yet
- Do not reboot the machine as the first fix; terminating the occupying process is faster and safer
- Do not change the default port permanently without documenting the change for the team

## Evidence Needed
- Capture the output of lsof -i :8081 showing the PID of the occupying process
- Confirm Metro actually fails on port binding, not another error

## Minimal Fix Scope
- The Metro bundler process startup invocation
- The port configuration in the project's metro.config.js or start command

## Validation Ladder
- Kill the occupying process and verify Metro starts on port 8081
- Verify the app connects to the Metro bundler and hot reloads
- Run the dev server smoke test

## Regression Guard
- Add a CI pre-check script that reports stale Metro processes before builds

## Reviewer Notes
