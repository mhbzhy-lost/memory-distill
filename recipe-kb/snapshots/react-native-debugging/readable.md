- [react-native-debugging-1] Debugging features, such as the Dev Menu, LogBox, and React Native DevTools are disabled in release (production) builds.

- [react-native-debugging-2] React Native provides an in-app developer menu providing access to debugging features. You can access the Dev Menu by shaking your device or via keyboard shortcuts:

- [react-native-debugging-3] iOS Simulator: Ctrl + Cmd ⌘ + Z (or Device > Shake)

- [react-native-debugging-4] Android emulators: Cmd ⌘ + M (macOS) or Ctrl + M (Windows and Linux)

- [react-native-debugging-5] Alternative (Android): adb shell input keyevent 82 .

- [react-native-debugging-6] Opening DevTools ​

- [react-native-debugging-7] React Native DevTools is our built-in debugger for React Native. It allows you to inspect and understand how your JavaScript code is running, similar to a web browser.

- [react-native-debugging-8] To open DevTools, either:

- [react-native-debugging-9] Select "Open DevTools" in the Dev Menu.

- [react-native-debugging-10] Press j from the CLI.

- [react-native-debugging-11] On first launch, DevTools will open to a welcome panel, along with an open console drawer where you can view logs and interact with the JavaScript runtime. From the top of the window, you can navigate to other panels, including the integrated React Components Inspector and Profiler.

- [react-native-debugging-12] Learn more in our React Native DevTools guide .

- [react-native-debugging-13] LogBox ​

- [react-native-debugging-14] LogBox is an in-app tool that displays when warnings or errors are logged by your app.

- [react-native-debugging-15] Fatal Errors ​

- [react-native-debugging-16] When an unrecoverable error occurs, such as a JavaScript syntax error, LogBox will open with the location of the error. In this state, LogBox is not dismissable since your code cannot be executed. LogBox will automatically dismiss once the syntax error is fixed — either via Fast Refresh or after a manual reload.

- [react-native-debugging-17] Console Errors and Warnings ​

- [react-native-debugging-18] Console errors and warnings are displayed as on-screen notifications with a red or yellow badge.

- [react-native-debugging-19] Errors will display with a notification count. Tap the notification to see an expanded view and to paginate through other logs.

- [react-native-debugging-20] Warnings will display a notification banner without details, prompting you to open React Native DevTools.

- [react-native-debugging-21] When React Native DevTools is open, all errors except fatal errors will be hidden to LogBox. We recommend using the Console panel within React Native DevTools as a source of truth, due to various LogBox options which can hide or adjust the level of certain logs.

- [react-native-debugging-22] LogBox can be configured via the LogBox API.

- [react-native-debugging-23] import { LogBox } from 'react-native' ;

- [react-native-debugging-24] LogBox notifications can be disabled using LogBox.ignoreAllLogs() . This can be useful in situations such as giving product demos.

- [react-native-debugging-25] LogBox . ignoreAllLogs ( ) ;

- [react-native-debugging-26] Notifications can be disabled on a per-log basis via LogBox.ignoreLogs() . This can be useful for noisy warnings or those that cannot be fixed, e.g. in a third-party dependency.

- [react-native-debugging-27] LogBox . ignoreLogs ( [ // Exact message 'Warning: componentWillReceiveProps has been renamed' , // Substring or regex match / GraphQL error : . * / , ] ) ;

- [react-native-debugging-28] LogBox will treat certain errors from React as warnings, which will mean they don't display as an in-app error notification. Advanced users can change this behaviour by customising LogBox's warning filter using LogBoxData.setWarningFilter() .

- [react-native-debugging-29] LogBoxData.setWarningFilter()

- [react-native-debugging-30] Performance Monitor ​

- [react-native-debugging-31] On Android and iOS, an in-app performance overlay can be toggled during development by selecting "Perf Monitor" in the Dev Menu. Learn more about this feature here .

- [react-native-debugging-32] The Performance Monitor runs in-app and is a guide. We recommend investigating the native tooling under Android Studio and Xcode for accurate performance measurements.
