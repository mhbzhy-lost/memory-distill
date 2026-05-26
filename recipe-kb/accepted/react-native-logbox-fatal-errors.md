---
id: react-native-logbox-fatal-errors
kind: debug-recipe
status: accepted
stack:
- react-native
failure_class: react-native/debugging
symptoms:
- LogBox displays an undismissable fatal error because JavaScript cannot be executed
  due to a syntax or runtime error
fingerprints:
- LogBox
- fatal error
- JavaScript syntax error
- not dismissable
- Fast Refresh
first_checks:
- Check the LogBox error message for the file and line of the fatal syntax error
- Check whether Fast Refresh will automatically resolve the error after fixing the
  syntax
- Check whether the fatal error is coming from React Native DevTools console logs
  rather than app code
do_not:
- Do not use LogBox.ignoreAllLogs() to hide fatal errors; it is meant for suppressing
  warnings during demos
- Do not rely on LogBox as the sole debugging tool; open React Native DevTools Console
  for authoritative logs
evidence_needed:
- Capture the LogBox error message and stack trace
- Confirm whether React Native DevTools Console shows the same or more detail
minimal_fix_scope:
- The file and line identified by LogBox as the fatal error source
- The JavaScript module that fails to parse or execute
validation_ladder:
- Fix the syntax error shown in LogBox
- Verify the Redbox/LogBox automatically dismisses after Fast Refresh or manual reload
- Run the app smoke test to verify functionality
regression_guard:
- Add a build or lint check that catches the same class of syntax error before runtime
evidence_refs:
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-1
  short_excerpt: Debugging features, such as the Dev Menu, LogBox, and React Native
    DevTools are disabled in release (production) builds.
  quote_hash: sha256:70956886175e6a144167b2ab6073cb542c732aed32b60bde08747979ddf07889
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-6
  short_excerpt: Opening DevTools ​
  quote_hash: sha256:5b56ac7e07dfd4dbaf912a43a167e8827c020a13752ab1a0b8f33154409c91c4
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-7
  short_excerpt: React Native DevTools is our built-in debugger for React Native.
    It allows you to inspect and understand how your JavaScript code is running, similar
    to a web browser.
  quote_hash: sha256:f72c9069fe0dee24404e61cf747634b57ff7c12e5c0d6450de3cb28f28ce6dbe
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-8
  short_excerpt: 'To open DevTools, either:'
  quote_hash: sha256:8377cc3c1aa421af6cb686a684f1bebff2e986eae897ea833f71dd7737eecc87
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-9
  short_excerpt: Select "Open DevTools" in the Dev Menu.
  quote_hash: sha256:53e7d938065ca8d996f874752320ed021cd1edd436da668e5fd249345f7f84b2
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-11
  short_excerpt: On first launch, DevTools will open to a welcome panel, along with
    an open console drawer where you can view logs and interact with the JavaScript
    runtime. From the top of the window, you can navigate to other panels, including
    the integrated React Components Inspector and Profiler.
  quote_hash: sha256:8b706b7c855bc2c9e0f19013dc6a249c6c3e863308e1335a63089347ed16fd7b
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-12
  short_excerpt: Learn more in our React Native DevTools guide .
  quote_hash: sha256:1f0eee049242dd51ca5de2f58a9cf44d892bb9fd565098120c7b2a939c48a949
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-13
  short_excerpt: LogBox ​
  quote_hash: sha256:49a02c9d8a03aff6c561e600646dcfd8a8fd1aff626ef4dd788f6bee5bf49284
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-14
  short_excerpt: LogBox is an in-app tool that displays when warnings or errors are
    logged by your app.
  quote_hash: sha256:adfd252142ba9c110f2227319a4b74092b977028e037d0c6968d9f266985f271
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-15
  short_excerpt: Fatal Errors ​
  quote_hash: sha256:955b216e4eee7618ccd7a1f2a94074678982f41dadd6d3da68508fec4b0220a7
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-16
  short_excerpt: When an unrecoverable error occurs, such as a JavaScript syntax error,
    LogBox will open with the location of the error. In this state, LogBox is not
    dismissable since your code cannot be executed. LogBox will automatically dismiss
    once the syntax error is fixed — either via Fast Refresh or after a manual reload.
  quote_hash: sha256:a01a9608ef42e2ca4850ab997c1ced98c1227cade0fd28d400152744c965f2b0
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-20
  short_excerpt: Warnings will display a notification banner without details, prompting
    you to open React Native DevTools.
  quote_hash: sha256:2bdb02b5c21fcc83b44923b56fafbbd3c9cd76d2e17a7c4226328f90ec4cb10f
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-21
  short_excerpt: When React Native DevTools is open, all errors except fatal errors
    will be hidden to LogBox. We recommend using the Console panel within React Native
    DevTools as a source of truth, due to various LogBox options which can hide or
    adjust the level of certain logs.
  quote_hash: sha256:2850573c65ad904b924279f1310b1f42e28aff325babc7c7167a36ba71a35b5c
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-22
  short_excerpt: LogBox can be configured via the LogBox API.
  quote_hash: sha256:bb14c365f65aa120f445a07501d337a9b6ff93834166adbe67f4273672f5fcdf
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-23
  short_excerpt: import { LogBox } from 'react-native' ;
  quote_hash: sha256:f126b20908664af0ecf29bd72bd19e9b7fec5bb7eaedfb8399f10e67c4e828fe
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-24
  short_excerpt: LogBox notifications can be disabled using LogBox.ignoreAllLogs()
    . This can be useful in situations such as giving product demos.
  quote_hash: sha256:45d355c5ef39ef314d8faf221d4f0666476f9456054288e3a8f7812e4bb8a671
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-25
  short_excerpt: LogBox . ignoreAllLogs ( ) ;
  quote_hash: sha256:4242b6c1c7c99b0b4e4314bf784e191ecc918d25963487ca9a9ad2e4416f4956
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-26
  short_excerpt: Notifications can be disabled on a per-log basis via LogBox.ignoreLogs()
    . This can be useful for noisy warnings or those that cannot be fixed, e.g. in
    a third-party dependency.
  quote_hash: sha256:cb6e1d7dd565a544a700edb4c34d75bf28800e99d6060946b190b61025a862f5
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-27
  short_excerpt: 'LogBox . ignoreLogs ( [ // Exact message ''Warning: componentWillReceiveProps
    has been renamed'' , // Substring or regex match / GraphQL error : . * / , ] )
    ;'
  quote_hash: sha256:307d4baadf47afe1a28f5f472b23656b16643c4309c48e308a22cd7a8a1ef1fd
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-28
  short_excerpt: LogBox will treat certain errors from React as warnings, which will
    mean they don't display as an in-app error notification. Advanced users can change
    this behaviour by customising LogBox's warning filter using LogBoxData.setWarningFilter()
    .
  quote_hash: sha256:b03d90bb30944ee1582fbcc82c4e0ca8273513ba663f42021b65a95768e4a32b
- source_id: react-native-debugging
  url: https://reactnative.dev/docs/debugging
  final_url: https://reactnative.dev/docs/debugging
  source_type: official_doc
  captured_at: '2026-05-26T09:49:06.514472Z'
  section_anchor: root
  span_id: react-native-debugging-29
  short_excerpt: LogBoxData.setWarningFilter()
  quote_hash: sha256:0747fa33b2e45c00c532da3dad5fccb4247d8957c060077a4d66a9e5268a8f95
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# react-native-logbox-fatal-errors

## Failure Class
react-native/debugging

## Symptoms
- LogBox displays an undismissable fatal error because JavaScript cannot be executed due to a syntax or runtime error

## Fingerprints
- LogBox
- fatal error
- JavaScript syntax error
- not dismissable
- Fast Refresh

## First Checks
- Check the LogBox error message for the file and line of the fatal syntax error
- Check whether Fast Refresh will automatically resolve the error after fixing the syntax
- Check whether the fatal error is coming from React Native DevTools console logs rather than app code

## Do Not Patch Yet
- Do not use LogBox.ignoreAllLogs() to hide fatal errors; it is meant for suppressing warnings during demos
- Do not rely on LogBox as the sole debugging tool; open React Native DevTools Console for authoritative logs

## Evidence Needed
- Capture the LogBox error message and stack trace
- Confirm whether React Native DevTools Console shows the same or more detail

## Minimal Fix Scope
- The file and line identified by LogBox as the fatal error source
- The JavaScript module that fails to parse or execute

## Validation Ladder
- Fix the syntax error shown in LogBox
- Verify the Redbox/LogBox automatically dismisses after Fast Refresh or manual reload
- Run the app smoke test to verify functionality

## Regression Guard
- Add a build or lint check that catches the same class of syntax error before runtime

## Reviewer Notes
