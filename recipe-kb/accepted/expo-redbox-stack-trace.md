---
id: expo-redbox-stack-trace
kind: debug-recipe
status: accepted
stack:
- expo
- react-native
failure_class: expo/debugging
symptoms:
- A fatal error displays a Redbox with a stack trace that is unclear or the error
  location points to the wrong file
fingerprints:
- Redbox
- Yellowbox
- stack trace
- LogBox
- fatal error
first_checks:
- Check the stack trace for the file name and line number where the error occurred
- Check whether console.warn or console.error is the source of a Yellowbox warning
  versus an uncaught error
- Check whether a development build is showing the error or Expo Go is showing it,
  as stack traces differ
do_not:
- Do not ignore Yellowbox warnings; they indicate issues that may become Redbox errors
  after upgrade
- Do not suppress the error via error boundaries before identifying the root cause
  in the stack trace
evidence_needed:
- Capture the full stack trace from the Redbox or terminal output
- Identify the project file and line number mentioned in the trace
minimal_fix_scope:
- The file and line identified in the stack trace
- The component or function producing the fatal error
validation_ladder:
- Re-read the stack trace and navigate to the source location
- Fix the issue and verify the Redbox no longer appears on reload
- Run the component test or app smoke test
regression_guard:
- Add a component test for the error path that produced the Redbox
evidence_refs:
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-4
  short_excerpt: Learn about Redbox errors and stack traces in your Expo project.
  quote_hash: sha256:3a3bff6bdb56ec4c95e98144f0edbad93b9f2e11eef65af03aeb10df7a717c89
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-6
  short_excerpt: When developing an application using Expo, you'll encounter a Redbox
    error or Yellowbox warning. These logging experiences are provided by LogBox in
    React Native .
  quote_hash: sha256:bfd7bd52d4594936084f3b92131ae019cbbc47470e2e7209461b975c2597bad7
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-7
  short_excerpt: Redbox error and Yellowbox warning
  quote_hash: sha256:8a3c1f90846f596d259a6e30df0f42d8755483f1078e7418d68e05585a928a52
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-8
  short_excerpt: A Redbox error is displayed when a fatal error prevents your app
    from running. A Yellowbox warning is displayed to inform you that there is a possible
    issue and you should probably resolve it before shipping your app.
  quote_hash: sha256:288aa085167d6fdb3cff3318880cf61f94397311a66f5b74ab7fa0ef05db05a8
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-9
  short_excerpt: 'You can also create warnings and errors on your own with console.warn("Warning
    message") and console.error("Error message") . Another way to trigger the redbox
    is to throw an error and not catch it: throw Error("Error message") .'
  quote_hash: sha256:263e83dc2bb403ad6a17702103b21f02c3f930d7fed9f106a06362d4c3dfb31e
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-11
  short_excerpt: Stack traces
  quote_hash: sha256:23fd83bac6dd26368e8de728c45348c1cf9a32605dfe0438ff24a9f1d8ddc009
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-12
  short_excerpt: When you encounter an error during development, you'll see the error
    message and a stack trace , which is a report of the recent calls your application
    made when it crashed. This stack trace is shown both in your terminal and the
    Expo Go app or if you have created a development build.
  quote_hash: sha256:866e8e5870e119258b322e27f109caa0ac6d96245baf07716897b9f0e1e0c411
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-13
  short_excerpt: This stack trace is extremely valuable since it gives you the location
    of the error's occurrence. For example, in the following image, the error comes
    from the file HomeScreen.js and is caused on line 7 in that file.
  quote_hash: sha256:0e18c336faf8f11dab8121390205f4a8b8a34e963dffa21db5d141de7c8669b7
- source_id: expo-errors-and-warnings
  url: https://docs.expo.dev/debugging/errors-and-warnings/
  final_url: https://docs.expo.dev/debugging/errors-and-warnings/
  source_type: official_doc
  captured_at: '2026-05-26T09:52:36.774688Z'
  section_anchor: root
  span_id: expo-errors-and-warnings-14
  short_excerpt: When you look at that file, on line 7, you will see that a variable
    called renderDescription is referenced. The error message describes that the variable
    is not found because the variable is not declared in HomeScreen.js . This is a
    typical example of how helpful error messages and stack traces can be if you take
    the time to decipher them.
  quote_hash: sha256:0ff8d02c5d5a95706466c9f5a5d27532738a9a186a866050d7f9fcc1a6871d09
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# expo-redbox-stack-trace

## Failure Class
expo/debugging

## Symptoms
- A fatal error displays a Redbox with a stack trace that is unclear or the error location points to the wrong file

## Fingerprints
- Redbox
- Yellowbox
- stack trace
- LogBox
- fatal error

## First Checks
- Check the stack trace for the file name and line number where the error occurred
- Check whether console.warn or console.error is the source of a Yellowbox warning versus an uncaught error
- Check whether a development build is showing the error or Expo Go is showing it, as stack traces differ

## Do Not Patch Yet
- Do not ignore Yellowbox warnings; they indicate issues that may become Redbox errors after upgrade
- Do not suppress the error via error boundaries before identifying the root cause in the stack trace

## Evidence Needed
- Capture the full stack trace from the Redbox or terminal output
- Identify the project file and line number mentioned in the trace

## Minimal Fix Scope
- The file and line identified in the stack trace
- The component or function producing the fatal error

## Validation Ladder
- Re-read the stack trace and navigate to the source location
- Fix the issue and verify the Redbox no longer appears on reload
- Run the component test or app smoke test

## Regression Guard
- Add a component test for the error path that produced the Redbox

## Reviewer Notes
