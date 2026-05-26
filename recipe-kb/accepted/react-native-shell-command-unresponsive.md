---
id: react-native-shell-command-unresponsive
kind: debug-recipe
status: accepted
stack:
- react-native
failure_class: react-native/android-build
symptoms:
- Android build fails with ShellCommandUnresponsiveException during task execution
fingerprints:
- ShellCommandUnresponsiveException
- Execution failed for task
- :app:installDebug
- DeviceException
first_checks:
- Check whether the ADB server is running and responsive with adb devices
- Check whether the ADB server needs to be restarted with adb kill-server && adb start-server
- Check the USB cable or emulator connection if running on a physical device
do_not:
- Do not reinstall the Android SDK before restarting the ADB server
- Do not increase Gradle timeout as a workaround without diagnosing the ADB unresponsiveness
evidence_needed:
- Capture the adb devices output to verify device connectivity
- Capture the full Gradle stack trace showing which task failed
minimal_fix_scope:
- The ADB server process
- The Gradle build execution environment
validation_ladder:
- Restart the ADB server and run adb devices to verify connectivity
- Re-attempt the Android build and verify it completes successfully
- Run the Android build smoke test
regression_guard:
- Add a pre-build script that restarts ADB if no devices are detected
evidence_refs:
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-29
  short_excerpt: 'If you encounter a ShellCommandUnresponsiveException exception such
    as:'
  quote_hash: sha256:4d6f03f923970ca45e4f99d18b2395efd7cc9e5c318f5666548ab88331fa473c
- source_id: react-native-troubleshooting
  url: https://reactnative.dev/docs/troubleshooting
  final_url: https://reactnative.dev/docs/troubleshooting
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-troubleshooting-30
  short_excerpt: 'Execution failed for task '':app:installDebug'' . com . android
    . builder . testing . api . DeviceException : com . android . ddmlib . ShellCommandUnresponsiveException'
  quote_hash: sha256:427d88495fa7cf332536b0d9f8841cff50663d55ba42e122ecf29c349a32abfd
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-native-shell-command-unresponsive

## Failure Class
react-native/android-build

## Symptoms
- Android build fails with ShellCommandUnresponsiveException during task execution

## Fingerprints
- ShellCommandUnresponsiveException
- Execution failed for task
- :app:installDebug
- DeviceException

## First Checks
- Check whether the ADB server is running and responsive with adb devices
- Check whether the ADB server needs to be restarted with adb kill-server && adb start-server
- Check the USB cable or emulator connection if running on a physical device

## Do Not Patch Yet
- Do not reinstall the Android SDK before restarting the ADB server
- Do not increase Gradle timeout as a workaround without diagnosing the ADB unresponsiveness

## Evidence Needed
- Capture the adb devices output to verify device connectivity
- Capture the full Gradle stack trace showing which task failed

## Minimal Fix Scope
- The ADB server process
- The Gradle build execution environment

## Validation Ladder
- Restart the ADB server and run adb devices to verify connectivity
- Re-attempt the Android build and verify it completes successfully
- Run the Android build smoke test

## Regression Guard
- Add a pre-build script that restarts ADB if no devices are detected

## Reviewer Notes
