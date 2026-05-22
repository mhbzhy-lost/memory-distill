- [vite-troubleshooting-1] Troubleshooting ​

- [vite-troubleshooting-2] See Rollup's troubleshooting guide for more information too.

- [vite-troubleshooting-3] If the suggestions here don't work, please try posting questions on GitHub Discussions or in the #help channel of Vite Land Discord .

- [vite-troubleshooting-4] CLI ​

- [vite-troubleshooting-5] Error: Cannot find module 'C:\foo\bar&baz\vite\bin\vite.js' ​

- [vite-troubleshooting-6] The path to your project folder may include & , which doesn't work with npm on Windows ( npm/cmd-shim#45 ).

- [vite-troubleshooting-7] You will need to either:

- [vite-troubleshooting-8] Switch to another package manager (e.g. pnpm , yarn )

- [vite-troubleshooting-9] Remove & from the path to your project

- [vite-troubleshooting-10] Config ​

- [vite-troubleshooting-11] This package is ESM only ​

- [vite-troubleshooting-12] When importing an ESM only package by require , the following error happens.

- [vite-troubleshooting-13] Failed to resolve "foo". This package is ESM only but it was tried to load by require .

- [vite-troubleshooting-14] Error [ERR_REQUIRE_ESM]: require() of ES Module /path/to/dependency.js from /path/to/vite.config.js not supported. Instead change the require of index.js in /path/to/vite.config.js to a dynamic import() which is available in all CommonJS modules.

- [vite-troubleshooting-15] In Node.js <=22, ESM files cannot be loaded by require by default.

- [vite-troubleshooting-16] require

- [vite-troubleshooting-17] While it may work using --experimental-require-module , or Node.js >22, or in other runtimes, we still recommend converting your config to ESM by either:

- [vite-troubleshooting-18] --experimental-require-module

- [vite-troubleshooting-19] adding "type": "module" to the nearest package.json

- [vite-troubleshooting-20] renaming vite.config.js / vite.config.ts to vite.config.mjs / vite.config.mts

- [vite-troubleshooting-21] Dev Server ​

- [vite-troubleshooting-22] Requests are stalled forever ​

- [vite-troubleshooting-23] If you are using Linux, file descriptor limits and inotify limits may be causing the issue. As Vite does not bundle most of the files, browsers may request many files which require many file descriptors, going over the limit.

- [vite-troubleshooting-24] To solve this:

- [vite-troubleshooting-25] Increase file descriptor limit by ulimit shell # Check current limit $ ulimit -Sn # Change limit (temporary) $ ulimit -Sn 10000 # You might need to change the hard limit too # Restart your browser

- [vite-troubleshooting-26] Increase file descriptor limit by ulimit

- [vite-troubleshooting-27] # Check current limit $ ulimit -Sn # Change limit (temporary) $ ulimit -Sn 10000 # You might need to change the hard limit too # Restart your browser

- [vite-troubleshooting-28] Increase the following inotify related limits by sysctl shell # Check current limits $ sysctl fs.inotify # Change limits (temporary) $ sudo sysctl fs.inotify.max_queued_events= 16384 $ sudo sysctl fs.inotify.max_user_instances= 8192 $ sudo sysctl fs.inotify.max_user_watches= 524288

- [vite-troubleshooting-29] Increase the following inotify related limits by sysctl

- [vite-troubleshooting-30] # Check current limits $ sysctl fs.inotify # Change limits (temporary) $ sudo sysctl fs.inotify.max_queued_events= 16384 $ sudo sysctl fs.inotify.max_user_instances= 8192 $ sudo sysctl fs.inotify.max_user_watches= 524288

- [vite-troubleshooting-31] If the above steps don't work, you can try adding DefaultLimitNOFILE=65536 as an un-commented config to the following files:

- [vite-troubleshooting-32] /etc/systemd/system.conf

- [vite-troubleshooting-33] /etc/systemd/user.conf

- [vite-troubleshooting-34] For Ubuntu Linux, you may need to add the line * - nofile 65536 to the file /etc/security/limits.conf instead of updating systemd config files.

- [vite-troubleshooting-35] Note that these settings persist but a restart is required .

- [vite-troubleshooting-36] Alternatively, if the server is running inside a VS Code devcontainer, the request may appear to be stalled. To fix this issue, see Dev Containers / VS Code Port Forwarding .

- [vite-troubleshooting-37] Vite crashes with ENOSPC error ​

- [vite-troubleshooting-38] If you see an error like this on Linux:

- [vite-troubleshooting-39] Error: ENOSPC: System limit for number of file watchers reached

- [vite-troubleshooting-40] This happens when you have too many files in your project directory (e.g., many images or assets) and exceed the system's file watcher limit. Linux has a default limit of around 8,192-10,000 file watchers.

- [vite-troubleshooting-41] To solve this, you can:

- [vite-troubleshooting-42] Increase the system file watcher limit: shell # Check current limit $ cat /proc/sys/fs/inotify/max_user_watches # Increase limit (temporary) $ sudo sysctl fs.inotify.max_user_watches= 524288 # Make it permanent - add to /etc/sysctl.conf (or edit if it already exists) $ echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf $ sudo sysctl -p

- [vite-troubleshooting-43] Increase the system file watcher limit:

- [vite-troubleshooting-44] # Check current limit $ cat /proc/sys/fs/inotify/max_user_watches # Increase limit (temporary) $ sudo sysctl fs.inotify.max_user_watches= 524288 # Make it permanent - add to /etc/sysctl.conf (or edit if it already exists) $ echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf $ sudo sysctl -p

- [vite-troubleshooting-45] Exclude directories with many files from file watching using server.watch.ignored

- [vite-troubleshooting-46] server.watch.ignored

- [vite-troubleshooting-47] Use polling instead of file system events with server.watch.usePolling . Note that polling uses more CPU resources

- [vite-troubleshooting-48] server.watch.usePolling

- [vite-troubleshooting-49] Network requests stop loading ​

- [vite-troubleshooting-50] When using a self-signed SSL certificate, Chrome ignores all caching directives and reloads the content. Vite relies on these caching directives.

- [vite-troubleshooting-51] To resolve the problem use a trusted SSL cert.

- [vite-troubleshooting-52] See: Cache problems , Chrome issue

- [vite-troubleshooting-53] You can install a trusted cert via the CLI with this command:

- [vite-troubleshooting-54] security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain-db your-cert.cer

- [vite-troubleshooting-55] Or, by importing it into the Keychain Access app and updating the trust of your cert to "Always Trust."

- [vite-troubleshooting-56] 431 Request Header Fields Too Large ​

- [vite-troubleshooting-57] When the server / WebSocket server receives a large HTTP header, the request will be dropped and the following warning will be shown.

- [vite-troubleshooting-58] Server responded with status code 431. See https://vite.dev/guide/troubleshooting.html#_431-request-header-fields-too-large .

- [vite-troubleshooting-59] This is because Node.js limits request header size to mitigate CVE-2018-12121 .

- [vite-troubleshooting-60] To avoid this, try to reduce your request header size. For example, if the cookie is long, delete it. Or you can use --max-http-header-size to change max header size.

- [vite-troubleshooting-61] --max-http-header-size

- [vite-troubleshooting-62] Dev Containers / VS Code Port Forwarding ​

- [vite-troubleshooting-63] If you are using a Dev Container or port forwarding feature in VS Code, you may need to set the server.host option to 127.0.0.1 in the config to make it work.

- [vite-troubleshooting-64] server.host

- [vite-troubleshooting-65] This is because the port forwarding feature in VS Code does not support IPv6 .

- [vite-troubleshooting-66] See #16522 for more details.

- [vite-troubleshooting-67] HMR ​

- [vite-troubleshooting-68] Vite detects a file change but the HMR is not working ​

- [vite-troubleshooting-69] You may be importing a file with a different case. For example, src/foo.js exists and src/bar.js contains:

- [vite-troubleshooting-70] import './Foo.js' // should be './foo.js'

- [vite-troubleshooting-71] Related issue: #964

- [vite-troubleshooting-72] Vite does not detect a file change ​

- [vite-troubleshooting-73] If you are running Vite with WSL2, Vite cannot watch file changes in some conditions. See server.watch option .

- [vite-troubleshooting-74] server.watch

- [vite-troubleshooting-75] A full reload happens instead of HMR ​

- [vite-troubleshooting-76] If HMR is not handled by Vite or a plugin, a full reload will happen as it's the only way to refresh the state.

- [vite-troubleshooting-77] If HMR is handled but it is within a circular dependency, a full reload will also happen to recover the execution order. To solve this, try breaking the loop. You can run vite --debug hmr to log the circular dependency path if a file change triggered it.

- [vite-troubleshooting-78] Build ​

- [vite-troubleshooting-79] Built file does not work because of CORS error ​

- [vite-troubleshooting-80] If the HTML file output was opened with file protocol, the scripts won't run with the following error.

- [vite-troubleshooting-81] Access to script at 'file:///foo/bar.js' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: http, data, isolated-app, chrome-extension, chrome, https, chrome-untrusted.

- [vite-troubleshooting-82] Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at file:///foo/bar.js. (Reason: CORS request not http).

- [vite-troubleshooting-83] See Reason: CORS request not HTTP - HTTP | MDN for more information about why this happens.

- [vite-troubleshooting-84] You will need to access the file with http protocol. The easiest way to achieve this is to run npx vite preview .

- [vite-troubleshooting-85] No such file or directory error due to case sensitivity ​

- [vite-troubleshooting-86] If you encounter errors like ENOENT: no such file or directory or Module not found , this often occurs when your project was developed on a case-insensitive filesystem (Windows / macOS) but built on a case-sensitive one (Linux). Please make sure that the imports have the correct casing.

- [vite-troubleshooting-87] Failed to fetch dynamically imported module error ​

- [vite-troubleshooting-88] TypeError: Failed to fetch dynamically imported module

- [vite-troubleshooting-89] This error occurs in several cases:

- [vite-troubleshooting-90] Version skew

- [vite-troubleshooting-91] Poor network conditions

- [vite-troubleshooting-92] Browser extensions blocking requests

- [vite-troubleshooting-93] When you deploy a new version of your application, the HTML file and the JS files still reference old chunk names that were deleted in the new deployment. This happens when:

- [vite-troubleshooting-94] Users have an old version of your app cached in their browser

- [vite-troubleshooting-95] You deploy a new version with different chunk names (due to code changes)

- [vite-troubleshooting-96] The cached HTML tries to load chunks that no longer exist

- [vite-troubleshooting-97] If you are using a framework, refer to their documentation first as it may have a built-in solution for this problem.

- [vite-troubleshooting-98] To resolve this, you can:

- [vite-troubleshooting-99] Keep old chunks temporarily : Consider keeping the previous deployment's chunks for a period to allow cached users to transition smoothly.

- [vite-troubleshooting-100] Use a service worker : Implement a service worker that will prefetch all the assets and cache them.

- [vite-troubleshooting-101] Prefetch the dynamic chunks : Note that this does not help if your HTML file is cached by the browser due to Cache-Control headers.

- [vite-troubleshooting-102] Implement a graceful fallback : Implement error handling for dynamic imports to reload the page when chunks are missing. See Load Error Handling for more details.

- [vite-troubleshooting-103] This error may occur in unstable network environments. For example, when the request fails due to network errors or server downtime.

- [vite-troubleshooting-104] Note that you cannot retry the dynamic import due to browser limitations ( whatwg/html#6768 ).

- [vite-troubleshooting-105] The error may also occur if the browser extensions (like ad-blockers) are blocking that request.

- [vite-troubleshooting-106] It might be possible to work around by selecting a different chunk name by build.rolldownOptions.output.chunkFileNames , as these extensions often block requests based on file names (e.g. names containing ad , track ).

- [vite-troubleshooting-107] build.rolldownOptions.output.chunkFileNames

- [vite-troubleshooting-108] Optimized Dependencies ​

- [vite-troubleshooting-109] Outdated pre-bundled deps when linking to a local package ​

- [vite-troubleshooting-110] The hash key used to invalidate optimized dependencies depends on the package lock contents, the patches applied to dependencies, and the options in the Vite config file that affects the bundling of node modules. This means that Vite will detect when a dependency is overridden using a feature as npm overrides , and re-bundle your dependencies on the next server start. Vite won't invalidate the dependencies when you use a feature like npm link . In case you link or unlink a dependency, you'll need to force re-optimization on the next server start by using vite --force . We recommend using overrides instead, which are supported now by every package manager (see also pnpm overrides and yarn resolutions ).

- [vite-troubleshooting-111] Performance Bottlenecks ​

- [vite-troubleshooting-112] If you suffer any application performance bottlenecks resulting in slow load times, you can start the built-in Node.js inspector with your Vite dev server or when building your application to create the CPU profile:

- [vite-troubleshooting-113] vite --profile --open

- [vite-troubleshooting-114] vite build --profile

- [vite-troubleshooting-115] Vite Dev Server

- [vite-troubleshooting-116] Once your application is opened in the browser, just await finish loading it and then go back to the terminal and press p key (will stop the Node.js inspector) then press q key to stop the dev server.

- [vite-troubleshooting-117] Node.js inspector will generate vite-profile-0.cpuprofile in the root folder, go to https://www.speedscope.app/ , and upload the CPU profile using the BROWSE button to inspect the result.

- [vite-troubleshooting-118] You can install vite-plugin-inspect , which lets you inspect the intermediate state of Vite plugins and can also help you to identify which plugins or middlewares are the bottleneck in your applications. The plugin can be used in both dev and build modes. Check the readme file for more details.

- [vite-troubleshooting-119] Others ​

- [vite-troubleshooting-120] Module externalized for browser compatibility ​

- [vite-troubleshooting-121] When you use a Node.js module in the browser, Vite will output the following warning.

- [vite-troubleshooting-122] Module "fs" has been externalized for browser compatibility. Cannot access "fs.readFile" in client code.

- [vite-troubleshooting-123] This is because Vite does not automatically polyfill Node.js modules.

- [vite-troubleshooting-124] We recommend avoiding Node.js modules for browser code to reduce the bundle size, although you can add polyfills manually. If the module is imported from a third-party library (that's meant to be used in the browser), it's advised to report the issue to the respective library.

- [vite-troubleshooting-125] Syntax Error / Type Error happens ​

- [vite-troubleshooting-126] Vite cannot handle and does not support code that only runs on non-strict mode (sloppy mode). This is because Vite uses ESM and it is always strict mode inside ESM.

- [vite-troubleshooting-127] For example, you might see these errors.

- [vite-troubleshooting-128] [ERROR] With statements cannot be used with the "esm" output format due to strict mode

- [vite-troubleshooting-129] TypeError: Cannot create property 'foo' on boolean 'false'

- [vite-troubleshooting-130] If these codes are used inside dependencies, you could use patch-package (or yarn patch or pnpm patch ) for an escape hatch.

- [vite-troubleshooting-131] patch-package

- [vite-troubleshooting-132] yarn patch

- [vite-troubleshooting-133] pnpm patch

- [vite-troubleshooting-134] Browser extensions ​

- [vite-troubleshooting-135] Some browser extensions (like ad-blockers) may prevent the Vite client from sending requests to the Vite dev server. You may see a white screen without logged errors in this case. You may also see the following error:

- [vite-troubleshooting-136] Try disabling extensions if you have this issue.

- [vite-troubleshooting-137] Cross drive links on Windows ​

- [vite-troubleshooting-138] If there's a cross drive links in your project on Windows, Vite may not work.

- [vite-troubleshooting-139] An example of cross drive links are:

- [vite-troubleshooting-140] a virtual drive linked to a folder by subst command

- [vite-troubleshooting-141] a symlink/junction to a different drive by mklink command (e.g. Yarn global cache)

- [vite-troubleshooting-142] Related issue: #10802

- [vite-troubleshooting-143] Default import unexpectedly returns an object ​

- [vite-troubleshooting-144] The default import returns the module.exports object for CJS modules, while you may expect it to return the module.exports.default value.

- [vite-troubleshooting-145] This may cause errors like:

- [vite-troubleshooting-146] Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: object.

- [vite-troubleshooting-147] foo is not a function

- [vite-troubleshooting-148] See Rolldown's docs about this problem for more details: Ambiguous default import from CJS modules - Bundling CJS | Rolldown .

- [vite-troubleshooting-149] default
