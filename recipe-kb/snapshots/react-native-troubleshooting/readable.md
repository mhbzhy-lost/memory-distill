- [react-native-troubleshooting-1] These are some common issues you may run into while setting up React Native. If you encounter something that is not listed here, try searching for the issue in GitHub .

- [react-native-troubleshooting-2] Port already in use ​

- [react-native-troubleshooting-3] The Metro bundler runs on port 8081. If another process is already using that port, you can either terminate that process, or change the port that the bundler uses.

- [react-native-troubleshooting-4] Run the following command to find the id for the process that is listening on port 8081:

- [react-native-troubleshooting-5] sudo lsof -i :8081

- [react-native-troubleshooting-6] Then run the following to terminate the process:

- [react-native-troubleshooting-7] kill -9 < PID >

- [react-native-troubleshooting-8] On Windows you can find the process using port 8081 using Resource Monitor and stop it using Task Manager.

- [react-native-troubleshooting-9] You can configure the bundler to use a port other than 8081 by using the port parameter, from the root of your project run:

- [react-native-troubleshooting-10] npm

- [react-native-troubleshooting-11] Yarn

- [react-native-troubleshooting-12] npm start -- --port = 8088

- [react-native-troubleshooting-13] You will also need to update your applications to load the JavaScript bundle from the new port. If running on device from Xcode, you can do this by updating occurrences of 8081 to your chosen port in the ios/__App_Name__.xcodeproj/project.pbxproj file.

- [react-native-troubleshooting-14] NPM locking error ​

- [react-native-troubleshooting-15] If you encounter an error such as npm WARN locking Error: EACCES while using the React Native CLI, try running the following:

- [react-native-troubleshooting-16] sudo chown -R $USER ~/.npm sudo chown -R $USER /usr/local/lib/node_modules

- [react-native-troubleshooting-17] Missing libraries for React ​

- [react-native-troubleshooting-18] If you added React Native manually to your project, make sure you have included all the relevant dependencies that you are using, like RCTText.xcodeproj , RCTImage.xcodeproj . Next, the binaries built by these dependencies have to be linked to your app binary. Use the Linked Frameworks and Binaries section in the Xcode project settings. More detailed steps are here: Linking Libraries .

- [react-native-troubleshooting-19] If you are using CocoaPods, verify that you have added React along with the subspecs to the Podfile . For example, if you were using the <Text /> , <Image /> and fetch() APIs, you would need to add these in your Podfile :

- [react-native-troubleshooting-20] pod 'React' , : path => '../node_modules/react-native' , : subspecs => [ 'RCTText' , 'RCTImage' , 'RCTNetwork' , 'RCTWebSocket' , ]

- [react-native-troubleshooting-21] Next, make sure you have run pod install and that a Pods/ directory has been created in your project with React installed. CocoaPods will instruct you to use the generated .xcworkspace file henceforth to be able to use these installed dependencies.

- [react-native-troubleshooting-22] There is a CocoaPods plugin called cocoapods-fix-react-native which handles any potential post-fixing of the source code due to differences when using a dependency manager.

- [react-native-troubleshooting-23] In the project's build settings, User Search Header Paths and Header Search Paths are two configs that specify where Xcode should look for #import header files specified in the code. For Pods, CocoaPods uses a default array of specific folders to look in. Verify that this particular config is not overwritten, and that none of the folders configured are too large. If one of the folders is a large folder, Xcode will attempt to recursively search the entire directory and throw above error at some point.

- [react-native-troubleshooting-24] To revert the User Search Header Paths and Header Search Paths build settings to their defaults set by CocoaPods - select the entry in the Build Settings panel, and hit delete. It will remove the custom override and return to the CocoaPod defaults.

- [react-native-troubleshooting-25] No transports available ​

- [react-native-troubleshooting-26] React Native implements a polyfill for WebSockets. These polyfills are initialized as part of the react-native module that you include in your application through import React from 'react' . If you load another module that requires WebSockets, such as Firebase , be sure to load/require it after react-native:

- [react-native-troubleshooting-27] import React from 'react' ; import Firebase from 'firebase' ;

- [react-native-troubleshooting-28] Shell Command Unresponsive Exception ​

- [react-native-troubleshooting-29] If you encounter a ShellCommandUnresponsiveException exception such as:

- [react-native-troubleshooting-30] Execution failed for task ':app:installDebug' . com . android . builder . testing . api . DeviceException : com . android . ddmlib . ShellCommandUnresponsiveException

- [react-native-troubleshooting-31] Restart the ADB server by running the following commands in your terminal:

- [react-native-troubleshooting-32] adb kill - server adb start - server

- [react-native-troubleshooting-33] Unable to start react-native package manager (on Linux) ​

- [react-native-troubleshooting-34] Case 1: Error "code":"ENOSPC","errno":"ENOSPC" ​

- [react-native-troubleshooting-35] Issue caused by the number of directories inotify (used by watchman on Linux) can monitor. To solve it, run this command in your terminal window

- [react-native-troubleshooting-36] echo fs.inotify.max_user_watches = 582222 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

- [react-native-troubleshooting-37] Error: spawnSync ./gradlew EACCES ​

- [react-native-troubleshooting-38] If you run into issue where executing npm run android or yarn android on macOS throws the above error, try to run sudo chmod +x android/gradlew command to make gradlew files into executable.
