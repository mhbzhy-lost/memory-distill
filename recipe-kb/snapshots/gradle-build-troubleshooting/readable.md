- [gradle-build-troubleshooting-1] Troubleshooting builds

- [gradle-build-troubleshooting-2] The following is a collection of common issues and suggestions for addressing them. You can get other tips and search the Gradle forums and StackOverflow #gradle answers.

- [gradle-build-troubleshooting-3] Troubleshooting the installation

- [gradle-build-troubleshooting-4] If you followed the installation instructions , and aren’t able to execute your Gradle build, here are some tips that may help.

- [gradle-build-troubleshooting-5] If you installed Gradle outside of just invoking the Gradle Wrapper , you can check your Gradle installation by running gradle --version in a terminal.

- [gradle-build-troubleshooting-6] You should see something like this:

- [gradle-build-troubleshooting-7] $ ./gradlew --version

- [gradle-build-troubleshooting-8] ------------------------------------------------------------ Gradle {gradleVersion} ------------------------------------------------------------ Build time: 2025-05-13 06:56:13 UTC Revision: 3c890746756262d3778e12eaa5155d661d7cbdf2 Kotlin: 2.1.21 Groovy: 4.0.28 Ant: Apache Ant(TM) version 1.10.15 compiled on August 25 2024 Launcher JVM: 22.0.1 (Oracle Corporation 22.0.1+8-16) Daemon JVM: Compatible with Java 17, any vendor, nativeImageCapable=false (from gradle/gradle-daemon-jvm.properties) OS: Mac OS X 15.5 aarch64

- [gradle-build-troubleshooting-9] If not, here are some things you might see instead.

- [gradle-build-troubleshooting-10] Command not found: gradle

- [gradle-build-troubleshooting-11] If you get "command not found: gradle", you must ensure that Gradle is correctly added to your PATH .

- [gradle-build-troubleshooting-12] JAVA_HOME is set to an invalid directory

- [gradle-build-troubleshooting-13] If you get an error like:

- [gradle-build-troubleshooting-14] ERROR: JAVA_HOME is set to an invalid directory

- [gradle-build-troubleshooting-15] Set the JAVA_HOME variable in your environment to match the location of your Java installation:

- [gradle-build-troubleshooting-16] $ export JAVA_HOME=/Users/user/Library/Java/JavaVirtualMachines/corretto-22.0.1/Contents/Home $ echo $JAVA_HOME

- [gradle-build-troubleshooting-17] /Users/user/Library/Java/JavaVirtualMachines/corretto-22.0.1/Contents/Home

- [gradle-build-troubleshooting-18] You must ensure that a Java Development Kit version 17 or higher is properly installed , the JAVA_HOME environment variable is set, and Java is added to your PATH .

- [gradle-build-troubleshooting-19] Permission denied

- [gradle-build-troubleshooting-20] If you get "permission denied", that means that Gradle likely exists in the correct place, but it is not executable. You can fix this using chmod +x path/to/executable on *nix-based systems.

- [gradle-build-troubleshooting-21] Other installation failures

- [gradle-build-troubleshooting-22] If gradle —-version works, but all of your builds fail with the same error, it is possible that one of your Gradle build configuration scripts is broken.

- [gradle-build-troubleshooting-23] You can verify the problem with Gradle scripts by running gradle help , which executes configuration scripts but no Gradle tasks. If the error persists, it means the build configuration is problematic. If not, the problem exists when executing one or more requested tasks (Gradle executes configuration scripts first, followed by build steps).

- [gradle-build-troubleshooting-24] Debugging dependency resolution

- [gradle-build-troubleshooting-25] You can see a dependency tree and see which resolved dependency versions differed from what was requested by clicking the Dependencies view and using the search functionality, specifying the resolution reason.

- [gradle-build-troubleshooting-26] The actual Build Scan with filtering criteria is available for exploration.

- [gradle-build-troubleshooting-27] Troubleshooting slow builds

- [gradle-build-troubleshooting-28] For build performance issues (including "slow sync time"), see improving the Performance of Gradle Builds .

- [gradle-build-troubleshooting-29] Android developers should watch a presentation by the Android SDK Tools team about Speeding Up Your Android Gradle Builds . Many tips are also covered in the Android Studio user guide on optimizing build speed .

- [gradle-build-troubleshooting-30] Debugging build logic

- [gradle-build-troubleshooting-31] Attaching a debugger to your build

- [gradle-build-troubleshooting-32] You can set breakpoints and debug buildSrc and standalone plugins in your Gradle build itself by setting the org.gradle.debug property to "true" and then attaching a remote debugger to port 5005. You can change the port number by setting the org.gradle.debug.port property to the desired port number.

- [gradle-build-troubleshooting-33] buildSrc

- [gradle-build-troubleshooting-34] To attach the debugger remotely via the network, you must set the org.gradle.debug.host property to the machine’s IP address or * (listen on all interfaces).

- [gradle-build-troubleshooting-35] $ ./gradlew help -Dorg.gradle.debug=true

- [gradle-build-troubleshooting-36] Using the Kotlin DSL, you can debug the build scripts themselves.

- [gradle-build-troubleshooting-37] The following video demonstrates how to debug an example build using IntelliJ IDEA.

- [gradle-build-troubleshooting-38] Adding and changing logging

- [gradle-build-troubleshooting-39] In addition to controlling logging verbosity , you can also control display of task outcomes (e.g. "UP-TO-DATE") in lifecycle logging using the --console=verbose flag .

- [gradle-build-troubleshooting-40] --console=verbose

- [gradle-build-troubleshooting-41] You can also replace much of Gradle’s logging with your own by registering various event listeners. One example of a custom event logger is explained in the logging documentation . You can also control logging from external tools , making them more verbose to debug their execution.

- [gradle-build-troubleshooting-42] $ GRADLE_USER_HOME /daemon/9.5.1/

- [gradle-build-troubleshooting-43] Task executed when it should have been UP-TO-DATE

- [gradle-build-troubleshooting-44] --info logs explain why a task was executed, though a Build Scan does this in a searchable, visual way by going to the Timeline view and clicking on the task you want to inspect.

- [gradle-build-troubleshooting-45] You can learn what the task outcomes mean from this listing .

- [gradle-build-troubleshooting-46] Debugging IDE integration

- [gradle-build-troubleshooting-47] Many infrequent errors within IDEs can be solved by "refreshing" Gradle. See also more documentation on working with Gradle in IntelliJ IDEA and in Eclipse .

- [gradle-build-troubleshooting-48] Refreshing IntelliJ IDEA

- [gradle-build-troubleshooting-49] From the main menu, go to View > Tool Windows > Gradle . Then click on the Refresh icon.

- [gradle-build-troubleshooting-50] Refreshing Eclipse (using Buildship)

- [gradle-build-troubleshooting-51] If you’re using Buildship for the Eclipse IDE, you can re-synchronize your Gradle build by opening the "Gradle Tasks" view and clicking the "Refresh" icon, or by executing the Gradle > Refresh Gradle Project command from the context menu while editing a Gradle script.

- [gradle-build-troubleshooting-52] Troubleshooting daemon connection issues

- [gradle-build-troubleshooting-53] If your Gradle build fails before running any tasks, you may be encountering network configuration problems. When Gradle is unable to communicate with the Gradle daemon process, the build will immediately fail with a message similar to this:

- [gradle-build-troubleshooting-54] $ ./gradlew help

- [gradle-build-troubleshooting-55] Starting a Gradle Daemon, 1 stopped Daemon could not be reused, use --status for details FAILURE: Build failed with an exception. * What went wrong: A new daemon was started but could not be connected to: pid=DaemonInfo{pid=55913, address=[7fb34c82-1907-4c32-afda-888c9b6e2279 port:42751, addresses:[/127.0.0.1]], state=Busy, ...

- [gradle-build-troubleshooting-56] This can occur when network address translation (NAT) masquerade is used. When NAT masquerade is enabled, connections that should be considered local to the machine are masked to appear from external IP addresses. Gradle refuses to connect to any external IP address as a security precaution.

- [gradle-build-troubleshooting-57] The solution to this problem is to adjust your network configuration such that local connections are not modified to appear as from external addresses.

- [gradle-build-troubleshooting-58] You can monitor the detected network setup and the connection requests in the daemon log file ( $ GRADLE_USER_HOME /daemon/<Gradle version>/daemon-<PID>.out.log ).

- [gradle-build-troubleshooting-59] 2021-08-12T12:01:50.755+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding IP addresses for network interface enp0s3 2021-08-12T12:01:50.759+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Is this a loopback interface? false 2021-08-12T12:01:50.769+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding remote address /fe80:0:0:0:85ba:3f3e:1b88:c0e1%enp0s3 2021-08-12T12:01:50.770+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding remote address /10.0.2.15 2021-08-12T12:01:50.770+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding IP addresses for network interface lo 2021-08-12T12:01:50.771+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Is this a loopback interface? true 2021-08-12T12:01:50.771+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding loopback address /0:0:0:0:0:0:0:1%lo 2021-08-12T12:01:50.771+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.InetAddresses] Adding loopback address /127.0.0.1 2021-08-12T12:01:50.775+0200 [DEBUG] [org.gradle.internal.remote.internal.inet.TcpIncomingConnector] Listening on [7fb34c82-1907-4c32-afda-888c9b6e2279 port:42751, addresses:[localhost/127.0.0.1]]. ... 2021-08-12T12:01:50.797+0200 [INFO] [org.gradle.launcher.daemon.server.DaemonRegistryUpdater] Advertising the daemon address to the clients: [7fb34c82-1907-4c32-afda-888c9b6e2279 port:42751, addresses:[localhost/127.0.0.1]] ... 2021-08-12T12:01:50.923+0200 [ERROR] [org.gradle.internal.remote.internal.inet.TcpIncomingConnector] Cannot accept connection from remote address /10.0.2.15.

- [gradle-build-troubleshooting-60] Getting additional help

- [gradle-build-troubleshooting-61] If you didn’t find a fix for your issue here, please reach out to the Gradle community on the help forum or search relevant developer resources using help.gradle.org .

- [gradle-build-troubleshooting-62] If you believe you’ve found a bug in Gradle, please file an issue on GitHub.
