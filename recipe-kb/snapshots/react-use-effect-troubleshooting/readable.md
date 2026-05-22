- [react-use-effect-troubleshooting-1] useEffect

- [react-use-effect-troubleshooting-2] useEffect is a React Hook that lets you synchronize a component with an external system.

- [react-use-effect-troubleshooting-3] useEffect ( setup , dependencies ? )

- [react-use-effect-troubleshooting-4] Reference useEffect(setup, dependencies?)

- [react-use-effect-troubleshooting-5] useEffect(setup, dependencies?)

- [react-use-effect-troubleshooting-6] Usage Connecting to an external system Wrapping Effects in custom Hooks Controlling a non-React widget Fetching data with Effects Specifying reactive dependencies Updating state based on previous state from an Effect Removing unnecessary object dependencies Removing unnecessary function dependencies Reading the latest props and state from an Effect Displaying different content on the server and the client

- [react-use-effect-troubleshooting-7] Connecting to an external system

- [react-use-effect-troubleshooting-8] Wrapping Effects in custom Hooks

- [react-use-effect-troubleshooting-9] Controlling a non-React widget

- [react-use-effect-troubleshooting-10] Fetching data with Effects

- [react-use-effect-troubleshooting-11] Specifying reactive dependencies

- [react-use-effect-troubleshooting-12] Updating state based on previous state from an Effect

- [react-use-effect-troubleshooting-13] Removing unnecessary object dependencies

- [react-use-effect-troubleshooting-14] Removing unnecessary function dependencies

- [react-use-effect-troubleshooting-15] Reading the latest props and state from an Effect

- [react-use-effect-troubleshooting-16] Displaying different content on the server and the client

- [react-use-effect-troubleshooting-17] Troubleshooting My Effect runs twice when the component mounts My Effect runs after every re-render My Effect keeps re-running in an infinite cycle My cleanup logic runs even though my component didn’t unmount My Effect does something visual, and I see a flicker before it runs

- [react-use-effect-troubleshooting-18] My Effect runs twice when the component mounts

- [react-use-effect-troubleshooting-19] My Effect runs after every re-render

- [react-use-effect-troubleshooting-20] My Effect keeps re-running in an infinite cycle

- [react-use-effect-troubleshooting-21] My cleanup logic runs even though my component didn’t unmount

- [react-use-effect-troubleshooting-22] My Effect does something visual, and I see a flicker before it runs

- [react-use-effect-troubleshooting-23] Reference

- [react-use-effect-troubleshooting-24] Call useEffect at the top level of your component to declare an Effect:

- [react-use-effect-troubleshooting-25] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => { connection . disconnect ( ) ; } ; } , [ serverUrl , roomId ] ) ; // ... }

- [react-use-effect-troubleshooting-26] See more examples below.

- [react-use-effect-troubleshooting-27] setup : The function with your Effect’s logic. Your setup function may also optionally return a cleanup function. When your component commits , React will run your setup function. After every commit with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. After your component is removed from the DOM, React will run your cleanup function.

- [react-use-effect-troubleshooting-28] optional dependencies : The list of all reactive values referenced inside of the setup code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is configured for React , it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like [dep1, dep2, dep3] . React will compare each dependency with its previous value using the Object.is comparison. If you omit this argument, your Effect will re-run after every commit of the component. See the difference between passing an array of dependencies, an empty array, and no dependencies at all.

- [react-use-effect-troubleshooting-29] Object.is

- [react-use-effect-troubleshooting-30] useEffect returns undefined .

- [react-use-effect-troubleshooting-31] useEffect is a Hook, so you can only call it at the top level of your component or your own Hooks. You can’t call it inside loops or conditions. If you need that, extract a new component and move the state into it.

- [react-use-effect-troubleshooting-32] If you’re not trying to synchronize with some external system, you probably don’t need an Effect.

- [react-use-effect-troubleshooting-33] When Strict Mode is on, React will run one extra development-only setup+cleanup cycle before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, implement the cleanup function.

- [react-use-effect-troubleshooting-34] If some of your dependencies are objects or functions defined inside the component, there is a risk that they will cause the Effect to re-run more often than needed. To fix this, remove unnecessary object and function dependencies. You can also extract state updates and non-reactive logic outside of your Effect.

- [react-use-effect-troubleshooting-35] If your Effect wasn’t caused by an interaction (like a click), React will generally let the browser paint the updated screen first before running your Effect. If your Effect is doing something visual (for example, positioning a tooltip), and the delay is noticeable (for example, it flickers), replace useEffect with useLayoutEffect .

- [react-use-effect-troubleshooting-36] useLayoutEffect

- [react-use-effect-troubleshooting-37] If your Effect is caused by an interaction (like a click), React may run your Effect before the browser paints the updated screen . This ensures that the result of the Effect can be observed by the event system. Usually, this works as expected. However, if you must defer the work until after paint, such as an alert() , you can use setTimeout . See reactwg/react-18/128 for more information.

- [react-use-effect-troubleshooting-38] Even if your Effect was caused by an interaction (like a click), React may allow the browser to repaint the screen before processing the state updates inside your Effect. Usually, this works as expected. However, if you must block the browser from repainting the screen, you need to replace useEffect with useLayoutEffect .

- [react-use-effect-troubleshooting-39] Effects only run on the client. They don’t run during server rendering.

- [react-use-effect-troubleshooting-40] Usage

- [react-use-effect-troubleshooting-41] Some components need to stay connected to the network, some browser API, or a third-party library, while they are displayed on the page. These systems aren’t controlled by React, so they are called external.

- [react-use-effect-troubleshooting-42] To connect your component to some external system, call useEffect at the top level of your component:

- [react-use-effect-troubleshooting-43] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useEffect ( ( ) => { const connection = createConnection(serverUrl, roomId); connection.connect(); return ( ) => { connection.disconnect(); } ; } , [serverUrl, roomId] ) ; // ... }

- [react-use-effect-troubleshooting-44] You need to pass two arguments to useEffect :

- [react-use-effect-troubleshooting-45] A setup function with setup code that connects to that system. It should return a cleanup function with cleanup code that disconnects from that system.

- [react-use-effect-troubleshooting-46] It should return a cleanup function with cleanup code that disconnects from that system.

- [react-use-effect-troubleshooting-47] A list of dependencies including every value from your component used inside of those functions.

- [react-use-effect-troubleshooting-48] React calls your setup and cleanup functions whenever it’s necessary, which may happen multiple times:

- [react-use-effect-troubleshooting-49] Your setup code runs when your component is added to the page (mounts) .

- [react-use-effect-troubleshooting-50] After every commit of your component where the dependencies have changed: First, your cleanup code runs with the old props and state. Then, your setup code runs with the new props and state.

- [react-use-effect-troubleshooting-51] First, your cleanup code runs with the old props and state.

- [react-use-effect-troubleshooting-52] Then, your setup code runs with the new props and state.

- [react-use-effect-troubleshooting-53] Your cleanup code runs one final time after your component is removed from the page (unmounts).

- [react-use-effect-troubleshooting-54] Let’s illustrate this sequence for the example above.

- [react-use-effect-troubleshooting-55] When the ChatRoom component above gets added to the page, it will connect to the chat room with the initial serverUrl and roomId . If either serverUrl or roomId change as a result of a commit (say, if the user picks a different chat room in a dropdown), your Effect will disconnect from the previous room, and connect to the next one. When the ChatRoom component is removed from the page, your Effect will disconnect one last time.

- [react-use-effect-troubleshooting-56] To help you find bugs, in development React runs setup and cleanup one extra time before the setup . This is a stress-test that verifies your Effect’s logic is implemented correctly. If this causes visible issues, your cleanup function is missing some logic. The cleanup function should stop or undo whatever the setup function was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the setup being called once (as in production) and a setup → cleanup → setup sequence (as in development). See common solutions.

- [react-use-effect-troubleshooting-57] Try to write every Effect as an independent process and think about a single setup/cleanup cycle at a time. It shouldn’t matter whether your component is mounting, updating, or unmounting. When your cleanup logic correctly “mirrors” the setup logic, your Effect is resilient to running setup and cleanup as often as needed.

- [react-use-effect-troubleshooting-58] Note

- [react-use-effect-troubleshooting-59] An Effect lets you keep your component synchronized with some external system (like a chat service). Here, external system means any piece of code that’s not controlled by React, such as:

- [react-use-effect-troubleshooting-60] A timer managed with setInterval() and clearInterval() .

- [react-use-effect-troubleshooting-61] setInterval()

- [react-use-effect-troubleshooting-62] clearInterval()

- [react-use-effect-troubleshooting-63] An event subscription using window.addEventListener() and window.removeEventListener() .

- [react-use-effect-troubleshooting-64] window.addEventListener()

- [react-use-effect-troubleshooting-65] window.removeEventListener()

- [react-use-effect-troubleshooting-66] A third-party animation library with an API like animation.start() and animation.reset() .

- [react-use-effect-troubleshooting-67] animation.start()

- [react-use-effect-troubleshooting-68] animation.reset()

- [react-use-effect-troubleshooting-69] If you’re not connecting to any external system, you probably don’t need an Effect.

- [react-use-effect-troubleshooting-70] In this example, the ChatRoom component uses an Effect to stay connected to an external system defined in chat.js . Press “Open chat” to make the ChatRoom component appear. This sandbox runs in development mode, so there is an extra connect-and-disconnect cycle, as explained here. Try changing the roomId and serverUrl using the dropdown and the input, and see how the Effect re-connects to the chat. Press “Close chat” to see the Effect disconnect one last time.

- [react-use-effect-troubleshooting-71] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => { connection . disconnect ( ) ; } ; } , [ roomId , serverUrl ] ) ; return ( < > < label > Server URL: { ' ' } < input value = { serverUrl } onChange = { e => setServerUrl ( e . target . value ) } /> </ label > < h1 > Welcome to the { roomId } room! </ h1 > </ > ) ; } export default function App ( ) { const [ roomId , setRoomId ] = useState ( 'general' ) ; const [ show , setShow ] = useState ( false ) ; return ( < > < label > Choose the chat room: { ' ' } < select value = { roomId } onChange = { e => setRoomId ( e . target . value ) } > < option value = "general" > general </ option > < option value = "travel" > travel </ option > < option value = "music" > music </ option > </ select > </ label > < button onClick = { ( ) => setShow ( ! show ) } > { show ? 'Close chat' : 'Open chat' } </ button > { show && < hr /> } { show && < ChatRoom roomId = { roomId } /> } </ > ) ; }

- [react-use-effect-troubleshooting-72] Effects are an “escape hatch”: you use them when you need to “step outside React” and when there is no better built-in solution for your use case. If you find yourself often needing to manually write Effects, it’s usually a sign that you need to extract some custom Hooks for common behaviors your components rely on.

- [react-use-effect-troubleshooting-73] For example, this useChatRoom custom Hook “hides” the logic of your Effect behind a more declarative API:

- [react-use-effect-troubleshooting-74] function useChatRoom ( { serverUrl , roomId } ) { useEffect ( ( ) => { const options = { serverUrl : serverUrl , roomId : roomId } ; const connection = createConnection ( options ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ roomId , serverUrl ] ) ; }

- [react-use-effect-troubleshooting-75] Then you can use it from any component like this:

- [react-use-effect-troubleshooting-76] function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useChatRoom ( { roomId : roomId , serverUrl : serverUrl } ) ; // ...

- [react-use-effect-troubleshooting-77] There are also many excellent custom Hooks for every purpose available in the React ecosystem.

- [react-use-effect-troubleshooting-78] Learn more about wrapping Effects in custom Hooks.

- [react-use-effect-troubleshooting-79] useChatRoom

- [react-use-effect-troubleshooting-80] useWindowListener

- [react-use-effect-troubleshooting-81] useIntersectionObserver

- [react-use-effect-troubleshooting-82] This example is identical to one of the earlier examples, but the logic is extracted to a custom Hook.

- [react-use-effect-troubleshooting-83] import { useState } from 'react' ; import { useChatRoom } from './useChatRoom.js' ; function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useChatRoom ( { roomId : roomId , serverUrl : serverUrl } ) ; return ( < > < label > Server URL: { ' ' } < input value = { serverUrl } onChange = { e => setServerUrl ( e . target . value ) } /> </ label > < h1 > Welcome to the { roomId } room! </ h1 > </ > ) ; } export default function App ( ) { const [ roomId , setRoomId ] = useState ( 'general' ) ; const [ show , setShow ] = useState ( false ) ; return ( < > < label > Choose the chat room: { ' ' } < select value = { roomId } onChange = { e => setRoomId ( e . target . value ) } > < option value = "general" > general </ option > < option value = "travel" > travel </ option > < option value = "music" > music </ option > </ select > </ label > < button onClick = { ( ) => setShow ( ! show ) } > { show ? 'Close chat' : 'Open chat' } </ button > { show && < hr /> } { show && < ChatRoom roomId = { roomId } /> } </ > ) ; }

- [react-use-effect-troubleshooting-84] Sometimes, you want to keep an external system synchronized to some prop or state of your component.

- [react-use-effect-troubleshooting-85] For example, if you have a third-party map widget or a video player component written without React, you can use an Effect to call methods on it that make its state match the current state of your React component. This Effect creates an instance of a MapWidget class defined in map-widget.js . When you change the zoomLevel prop of the Map component, the Effect calls the setZoom() on the class instance to keep it synchronized:

- [react-use-effect-troubleshooting-86] import { useRef , useEffect } from 'react' ; import { MapWidget } from './map-widget.js' ; export default function Map ( { zoomLevel } ) { const containerRef = useRef ( null ) ; const mapRef = useRef ( null ) ; useEffect ( ( ) => { if ( mapRef . current === null ) { mapRef . current = new MapWidget ( containerRef . current ) ; } const map = mapRef . current ; map . setZoom ( zoomLevel ) ; } , [ zoomLevel ] ) ; return ( < div style = { { width : 200 , height : 200 } } ref = { containerRef } /> ) ; }

- [react-use-effect-troubleshooting-87] In this example, a cleanup function is not needed because the MapWidget class manages only the DOM node that was passed to it. After the Map React component is removed from the tree, both the DOM node and the MapWidget class instance will be automatically garbage-collected by the browser JavaScript engine.

- [react-use-effect-troubleshooting-88] You can use an Effect to fetch data for your component. Note that if you use a framework, using your framework’s data fetching mechanism will be a lot more efficient than writing Effects manually.

- [react-use-effect-troubleshooting-89] If you want to fetch data from an Effect manually, your code might look like this:

- [react-use-effect-troubleshooting-90] import { useState , useEffect } from 'react' ; import { fetchBio } from './api.js' ; export default function Page ( ) { const [ person , setPerson ] = useState ( 'Alice' ) ; const [ bio , setBio ] = useState ( null ) ; useEffect ( ( ) => { let ignore = false ; setBio ( null ) ; fetchBio ( person ) . then ( result => { if ( ! ignore ) { setBio ( result ) ; } } ) ; return ( ) => { ignore = true ; } ; } , [ person ] ) ; // ...

- [react-use-effect-troubleshooting-91] Note the ignore variable which is initialized to false , and is set to true during cleanup. This ensures your code doesn’t suffer from “race conditions”: network responses may arrive in a different order than you sent them.

- [react-use-effect-troubleshooting-92] import { useState , useEffect } from 'react' ; import { fetchBio } from './api.js' ; export default function Page ( ) { const [ person , setPerson ] = useState ( 'Alice' ) ; const [ bio , setBio ] = useState ( null ) ; useEffect ( ( ) => { let ignore = false ; setBio ( null ) ; fetchBio ( person ) . then ( result => { if ( ! ignore ) { setBio ( result ) ; } } ) ; return ( ) => { ignore = true ; } } , [ person ] ) ; return ( < > < select value = { person } onChange = { e => { setPerson ( e . target . value ) ; } } > < option value = "Alice" > Alice </ option > < option value = "Bob" > Bob </ option > < option value = "Taylor" > Taylor </ option > </ select > < hr /> < p > < i > { bio ?? 'Loading...' } </ i > </ p > </ > ) ; }

- [react-use-effect-troubleshooting-93] You can also rewrite using the async / await syntax, but you still need to provide a cleanup function:

- [react-use-effect-troubleshooting-94] async

- [react-use-effect-troubleshooting-95] await

- [react-use-effect-troubleshooting-96] import { useState , useEffect } from 'react' ; import { fetchBio } from './api.js' ; export default function Page ( ) { const [ person , setPerson ] = useState ( 'Alice' ) ; const [ bio , setBio ] = useState ( null ) ; useEffect ( ( ) => { async function startFetching ( ) { setBio ( null ) ; const result = await fetchBio ( person ) ; if ( ! ignore ) { setBio ( result ) ; } } let ignore = false ; startFetching ( ) ; return ( ) => { ignore = true ; } } , [ person ] ) ; return ( < > < select value = { person } onChange = { e => { setPerson ( e . target . value ) ; } } > < option value = "Alice" > Alice </ option > < option value = "Bob" > Bob </ option > < option value = "Taylor" > Taylor </ option > </ select > < hr /> < p > < i > { bio ?? 'Loading...' } </ i > </ p > </ > ) ; }

- [react-use-effect-troubleshooting-97] Writing data fetching directly in Effects gets repetitive and makes it difficult to add optimizations like caching and server rendering later. It’s easier to use a custom Hook—either your own or maintained by the community.

- [react-use-effect-troubleshooting-98] Writing fetch calls inside Effects is a popular way to fetch data , especially in fully client-side apps. This is, however, a very manual approach and it has significant downsides:

- [react-use-effect-troubleshooting-99] Effects don’t run on the server. This means that the initial server-rendered HTML will only include a loading state with no data. The client computer will have to download all JavaScript and render your app only to discover that now it needs to load the data. This is not very efficient.

- [react-use-effect-troubleshooting-100] Fetching directly in Effects makes it easy to create “network waterfalls”. You render the parent component, it fetches some data, renders the child components, and then they start fetching their data. If the network is not very fast, this is significantly slower than fetching all data in parallel.

- [react-use-effect-troubleshooting-101] Fetching directly in Effects usually means you don’t preload or cache data. For example, if the component unmounts and then mounts again, it would have to fetch the data again.

- [react-use-effect-troubleshooting-102] It’s not very ergonomic. There’s quite a bit of boilerplate code involved when writing fetch calls in a way that doesn’t suffer from bugs like race conditions.

- [react-use-effect-troubleshooting-103] This list of downsides is not specific to React. It applies to fetching data on mount with any library. Like with routing, data fetching is not trivial to do well, so we recommend the following approaches:

- [react-use-effect-troubleshooting-104] If you use a framework , use its built-in data fetching mechanism. Modern React frameworks have integrated data fetching mechanisms that are efficient and don’t suffer from the above pitfalls.

- [react-use-effect-troubleshooting-105] Otherwise, consider using or building a client-side cache. Popular open source solutions include TanStack Query , useSWR , and React Router 6.4+. You can build your own solution too, in which case you would use Effects under the hood but also add logic for deduplicating requests, caching responses, and avoiding network waterfalls (by preloading data or hoisting data requirements to routes).

- [react-use-effect-troubleshooting-106] You can continue fetching data directly in Effects if neither of these approaches suit you.

- [react-use-effect-troubleshooting-107] Notice that you can’t “choose” the dependencies of your Effect. Every reactive value used by your Effect’s code must be declared as a dependency. Your Effect’s dependency list is determined by the surrounding code:

- [react-use-effect-troubleshooting-108] function ChatRoom ( { roomId } ) { // This is a reactive value const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; // This is a reactive value too useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; // This Effect reads these reactive values connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ serverUrl , roomId ] ) ; // ✅ So you must specify them as dependencies of your Effect // ... }

- [react-use-effect-troubleshooting-109] If either serverUrl or roomId change, your Effect will reconnect to the chat using the new values.

- [react-use-effect-troubleshooting-110] Reactive values include props and all variables and functions declared directly inside of your component. Since roomId and serverUrl are reactive values, you can’t remove them from the dependencies. If you try to omit them and your linter is correctly configured for React, the linter will flag this as a mistake you need to fix:

- [react-use-effect-troubleshooting-111] function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ ] ) ; // 🔴 React Hook useEffect has missing dependencies: 'roomId' and 'serverUrl' // ... }

- [react-use-effect-troubleshooting-112] To remove a dependency, you need to “prove” to the linter that it doesn’t need to be a dependency. For example, you can move serverUrl out of your component to prove that it’s not reactive and won’t change on re-renders:

- [react-use-effect-troubleshooting-113] const serverUrl = 'https://localhost:1234' ; // Not a reactive value anymore function ChatRoom ( { roomId } ) { useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ roomId ] ) ; // ✅ All dependencies declared // ... }

- [react-use-effect-troubleshooting-114] Now that serverUrl is not a reactive value (and can’t change on a re-render), it doesn’t need to be a dependency. If your Effect’s code doesn’t use any reactive values, its dependency list should be empty ( [] ):

- [react-use-effect-troubleshooting-115] []

- [react-use-effect-troubleshooting-116] const serverUrl = 'https://localhost:1234' ; // Not a reactive value anymore const roomId = 'music' ; // Not a reactive value anymore function ChatRoom ( ) { useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ ] ) ; // ✅ All dependencies declared // ... }

- [react-use-effect-troubleshooting-117] An Effect with empty dependencies doesn’t re-run when any of your component’s props or state change.

- [react-use-effect-troubleshooting-118] Pitfall

- [react-use-effect-troubleshooting-119] If you have an existing codebase, you might have some Effects that suppress the linter like this:

- [react-use-effect-troubleshooting-120] useEffect ( ( ) => { // ... // 🔴 Avoid suppressing the linter like this: // eslint-ignore-next-line react-hooks/exhaustive-deps } , [ ] ) ;

- [react-use-effect-troubleshooting-121] When dependencies don’t match the code, there is a high risk of introducing bugs. By suppressing the linter, you “lie” to React about the values your Effect depends on. Instead, prove they’re unnecessary.

- [react-use-effect-troubleshooting-122] If you specify the dependencies, your Effect runs after the initial commit and after commits with changed dependencies.

- [react-use-effect-troubleshooting-123] useEffect ( ( ) => { // ... } , [ a , b ] ) ; // Runs again if a or b are different

- [react-use-effect-troubleshooting-124] In the below example, serverUrl and roomId are reactive values, so they both must be specified as dependencies. As a result, selecting a different room in the dropdown or editing the server URL input causes the chat to re-connect. However, since message isn’t used in the Effect (and so it isn’t a dependency), editing the message doesn’t re-connect to the chat.

- [react-use-effect-troubleshooting-125] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; function ChatRoom ( { roomId } ) { const [ serverUrl , setServerUrl ] = useState ( 'https://localhost:1234' ) ; const [ message , setMessage ] = useState ( '' ) ; useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => { connection . disconnect ( ) ; } ; } , [ serverUrl , roomId ] ) ; return ( < > < label > Server URL: { ' ' } < input value = { serverUrl } onChange = { e => setServerUrl ( e . target . value ) } /> </ label > < h1 > Welcome to the { roomId } room! </ h1 > < label > Your message: { ' ' } < input value = { message } onChange = { e => setMessage ( e . target . value ) } /> </ label > </ > ) ; } export default function App ( ) { const [ show , setShow ] = useState ( false ) ; const [ roomId , setRoomId ] = useState ( 'general' ) ; return ( < > < label > Choose the chat room: { ' ' } < select value = { roomId } onChange = { e => setRoomId ( e . target . value ) } > < option value = "general" > general </ option > < option value = "travel" > travel </ option > < option value = "music" > music </ option > </ select > < button onClick = { ( ) => setShow ( ! show ) } > { show ? 'Close chat' : 'Open chat' } </ button > </ label > { show && < hr /> } { show && < ChatRoom roomId = { roomId } /> } </ > ) ; }

- [react-use-effect-troubleshooting-126] When you want to update state based on previous state from an Effect, you might run into a problem:

- [react-use-effect-troubleshooting-127] function Counter ( ) { const [ count , setCount ] = useState ( 0 ) ; useEffect ( ( ) => { const intervalId = setInterval ( ( ) => { setCount ( count + 1 ) ; // You want to increment the counter every second... } , 1000 ) return ( ) => clearInterval ( intervalId ) ; } , [ count ] ) ; // 🚩 ... but specifying `count` as a dependency always resets the interval. // ... }

- [react-use-effect-troubleshooting-128] Since count is a reactive value, it must be specified in the list of dependencies. However, that causes the Effect to cleanup and setup again every time the count changes. This is not ideal.

- [react-use-effect-troubleshooting-129] To fix this, pass the c => c + 1 state updater to setCount :

- [react-use-effect-troubleshooting-130] c => c + 1

- [react-use-effect-troubleshooting-131] import { useState , useEffect } from 'react' ; export default function Counter ( ) { const [ count , setCount ] = useState ( 0 ) ; useEffect ( ( ) => { const intervalId = setInterval ( ( ) => { setCount ( c => c + 1 ) ; // ✅ Pass a state updater } , 1000 ) ; return ( ) => clearInterval ( intervalId ) ; } , [ ] ) ; // ✅ Now count is not a dependency return < h1 > { count } </ h1 > ; }

- [react-use-effect-troubleshooting-132] Now that you’re passing c => c + 1 instead of count + 1 , your Effect no longer needs to depend on count . As a result of this fix, it won’t need to cleanup and setup the interval again every time the count changes.

- [react-use-effect-troubleshooting-133] count

- [react-use-effect-troubleshooting-134] If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every commit because the options object is different for every render:

- [react-use-effect-troubleshooting-135] const serverUrl = 'https://localhost:1234' ; function ChatRoom ( { roomId } ) { const [ message , setMessage ] = useState ( '' ) ; const options = { // 🚩 This object is created from scratch on every re-render serverUrl : serverUrl , roomId : roomId } ; useEffect ( ( ) => { const connection = createConnection ( options ) ; // It's used inside the Effect connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ options ] ) ; // 🚩 As a result, these dependencies are always different on a commit // ...

- [react-use-effect-troubleshooting-136] Avoid using an object created during rendering as a dependency. Instead, create the object inside the Effect:

- [react-use-effect-troubleshooting-137] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; const serverUrl = 'https://localhost:1234' ; function ChatRoom ( { roomId } ) { const [ message , setMessage ] = useState ( '' ) ; useEffect ( ( ) => { const options = { serverUrl : serverUrl , roomId : roomId } ; const connection = createConnection ( options ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ roomId ] ) ; return ( < > < h1 > Welcome to the { roomId } room! </ h1 > < input value = { message } onChange = { e => setMessage ( e . target . value ) } /> </ > ) ; } export default function App ( ) { const [ roomId , setRoomId ] = useState ( 'general' ) ; return ( < > < label > Choose the chat room: { ' ' } < select value = { roomId } onChange = { e => setRoomId ( e . target . value ) } > < option value = "general" > general </ option > < option value = "travel" > travel </ option > < option value = "music" > music </ option > </ select > </ label > < hr /> < ChatRoom roomId = { roomId } /> </ > ) ; }

- [react-use-effect-troubleshooting-138] Now that you create the options object inside the Effect, the Effect itself only depends on the roomId string.

- [react-use-effect-troubleshooting-139] With this fix, typing into the input doesn’t reconnect the chat. Unlike an object which gets re-created, a string like roomId doesn’t change unless you set it to another value. Read more about removing dependencies.

- [react-use-effect-troubleshooting-140] If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every commit because the createOptions function is different for every render:

- [react-use-effect-troubleshooting-141] function ChatRoom ( { roomId } ) { const [ message , setMessage ] = useState ( '' ) ; function createOptions ( ) { // 🚩 This function is created from scratch on every re-render return { serverUrl : serverUrl , roomId : roomId } ; } useEffect ( ( ) => { const options = createOptions ( ) ; // It's used inside the Effect const connection = createConnection ( ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ createOptions ] ) ; // 🚩 As a result, these dependencies are always different on a commit // ...

- [react-use-effect-troubleshooting-142] By itself, creating a function from scratch on every re-render is not a problem. You don’t need to optimize that. However, if you use it as a dependency of your Effect, it will cause your Effect to re-run after every commit.

- [react-use-effect-troubleshooting-143] Avoid using a function created during rendering as a dependency. Instead, declare it inside the Effect:

- [react-use-effect-troubleshooting-144] import { useState , useEffect } from 'react' ; import { createConnection } from './chat.js' ; const serverUrl = 'https://localhost:1234' ; function ChatRoom ( { roomId } ) { const [ message , setMessage ] = useState ( '' ) ; useEffect ( ( ) => { function createOptions ( ) { return { serverUrl : serverUrl , roomId : roomId } ; } const options = createOptions ( ) ; const connection = createConnection ( options ) ; connection . connect ( ) ; return ( ) => connection . disconnect ( ) ; } , [ roomId ] ) ; return ( < > < h1 > Welcome to the { roomId } room! </ h1 > < input value = { message } onChange = { e => setMessage ( e . target . value ) } /> </ > ) ; } export default function App ( ) { const [ roomId , setRoomId ] = useState ( 'general' ) ; return ( < > < label > Choose the chat room: { ' ' } < select value = { roomId } onChange = { e => setRoomId ( e . target . value ) } > < option value = "general" > general </ option > < option value = "travel" > travel </ option > < option value = "music" > music </ option > </ select > </ label > < hr /> < ChatRoom roomId = { roomId } /> </ > ) ; }

- [react-use-effect-troubleshooting-145] Now that you define the createOptions function inside the Effect, the Effect itself only depends on the roomId string. With this fix, typing into the input doesn’t reconnect the chat. Unlike a function which gets re-created, a string like roomId doesn’t change unless you set it to another value. Read more about removing dependencies.

- [react-use-effect-troubleshooting-146] By default, when you read a reactive value from an Effect, you have to add it as a dependency. This ensures that your Effect “reacts” to every change of that value. For most dependencies, that’s the behavior you want.

- [react-use-effect-troubleshooting-147] However, sometimes you’ll want to read the latest props and state from an Effect without “reacting” to them. For example, imagine you want to log the number of the items in the shopping cart for every page visit:

- [react-use-effect-troubleshooting-148] function Page ( { url , shoppingCart } ) { useEffect ( ( ) => { logVisit ( url , shoppingCart . length ) ; } , [ url , shoppingCart ] ) ; // ✅ All dependencies declared // ... }

- [react-use-effect-troubleshooting-149] What if you want to log a new page visit after every url change, but not if only the shoppingCart changes? You can’t exclude shoppingCart from dependencies without breaking the reactivity rules. However, you can express that you don’t want a piece of code to “react” to changes even though it is called from inside an Effect. Declare an Effect Event with the useEffectEvent Hook, and move the code reading shoppingCart inside of it:

- [react-use-effect-troubleshooting-150] url

- [react-use-effect-troubleshooting-151] shoppingCart

- [react-use-effect-troubleshooting-152] useEffectEvent

- [react-use-effect-troubleshooting-153] function Page ( { url , shoppingCart } ) { const onVisit = useEffectEvent ( visitedUrl => { logVisit ( visitedUrl , shoppingCart . length ) } ) ; useEffect ( ( ) => { onVisit ( url ) ; } , [ url ] ) ; // ✅ All dependencies declared // ... }

- [react-use-effect-troubleshooting-154] Effect Events are not reactive and must always be omitted from dependencies of your Effect. This is what lets you put non-reactive code (where you can read the latest value of some props and state) inside of them. By reading shoppingCart inside of onVisit , you ensure that shoppingCart won’t re-run your Effect.

- [react-use-effect-troubleshooting-155] Read more about how Effect Events let you separate reactive and non-reactive code.

- [react-use-effect-troubleshooting-156] If your app uses server rendering (either directly or via a framework ), your component will render in two different environments. On the server, it will render to produce the initial HTML. On the client, React will run the rendering code again so that it can attach your event handlers to that HTML. This is why, for hydration to work, your initial render output must be identical on the client and the server.

- [react-use-effect-troubleshooting-157] In rare cases, you might need to display different content on the client. For example, if your app reads some data from localStorage , it can’t possibly do that on the server. Here is how you could implement this:

- [react-use-effect-troubleshooting-158] localStorage

- [react-use-effect-troubleshooting-159] function MyComponent ( ) { const [ didMount , setDidMount ] = useState ( false ) ; useEffect ( ( ) => { setDidMount ( true ) ; } , [ ] ) ; if ( didMount ) { // ... return client-only JSX ... } else { // ... return initial JSX ... } }

- [react-use-effect-troubleshooting-160] While the app is loading, the user will see the initial render output. Then, when it’s loaded and hydrated, your Effect will run and set didMount to true , triggering a re-render. This will switch to the client-only render output. Effects don’t run on the server, so this is why didMount was false during the initial server render.

- [react-use-effect-troubleshooting-161] Use this pattern sparingly. Keep in mind that users with a slow connection will see the initial content for quite a bit of time—potentially, many seconds—so you don’t want to make jarring changes to your component’s appearance. In many cases, you can avoid the need for this by conditionally showing different things with CSS.

- [react-use-effect-troubleshooting-162] Troubleshooting

- [react-use-effect-troubleshooting-163] When Strict Mode is on, in development, React runs setup and cleanup one extra time before the actual setup.

- [react-use-effect-troubleshooting-164] This is a stress-test that verifies your Effect’s logic is implemented correctly. If this causes visible issues, your cleanup function is missing some logic. The cleanup function should stop or undo whatever the setup function was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the setup being called once (as in production) and a setup → cleanup → setup sequence (as in development).

- [react-use-effect-troubleshooting-165] Read more about how this helps find bugs and how to fix your logic.

- [react-use-effect-troubleshooting-166] First, check that you haven’t forgotten to specify the dependency array:

- [react-use-effect-troubleshooting-167] useEffect ( ( ) => { // ... } ) ; // 🚩 No dependency array: re-runs after every commit!

- [react-use-effect-troubleshooting-168] If you’ve specified the dependency array but your Effect still re-runs in a loop, it’s because one of your dependencies is different on every re-render.

- [react-use-effect-troubleshooting-169] You can debug this problem by manually logging your dependencies to the console:

- [react-use-effect-troubleshooting-170] useEffect ( ( ) => { // .. } , [ serverUrl , roomId ] ) ; console . log ( [ serverUrl , roomId ] ) ;

- [react-use-effect-troubleshooting-171] You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as temp1 and the second one got saved as temp2 , you can then use the browser console to check whether each dependency in both arrays is the same:

- [react-use-effect-troubleshooting-172] Object . is ( temp1 [ 0 ] , temp2 [ 0 ] ) ; // Is the first dependency the same between the arrays? Object . is ( temp1 [ 1 ] , temp2 [ 1 ] ) ; // Is the second dependency the same between the arrays? Object . is ( temp1 [ 2 ] , temp2 [ 2 ] ) ; // ... and so on for every dependency ...

- [react-use-effect-troubleshooting-173] When you find the dependency that is different on every re-render, you can usually fix it in one of these ways:

- [react-use-effect-troubleshooting-174] As a last resort (if these methods didn’t help), wrap its creation with useMemo or useCallback (for functions).

- [react-use-effect-troubleshooting-175] useMemo

- [react-use-effect-troubleshooting-176] useCallback

- [react-use-effect-troubleshooting-177] If your Effect runs in an infinite cycle, these two things must be true:

- [react-use-effect-troubleshooting-178] Your Effect is updating some state.

- [react-use-effect-troubleshooting-179] That state leads to a re-render, which causes the Effect’s dependencies to change.

- [react-use-effect-troubleshooting-180] Before you start fixing the problem, ask yourself whether your Effect is connecting to some external system (like DOM, network, a third-party widget, and so on). Why does your Effect need to set state? Does it synchronize with that external system? Or are you trying to manage your application’s data flow with it?

- [react-use-effect-troubleshooting-181] If there is no external system, consider whether removing the Effect altogether would simplify your logic.

- [react-use-effect-troubleshooting-182] If you’re genuinely synchronizing with some external system, think about why and under what conditions your Effect should update the state. Has something changed that affects your component’s visual output? If you need to keep track of some data that isn’t used by rendering, a ref (which doesn’t trigger re-renders) might be more appropriate. Verify your Effect doesn’t update the state (and trigger re-renders) more than needed.

- [react-use-effect-troubleshooting-183] Finally, if your Effect is updating the state at the right time, but there is still a loop, it’s because that state update leads to one of the Effect’s dependencies changing. Read how to debug dependency changes.

- [react-use-effect-troubleshooting-184] The cleanup function runs not only during unmount, but before every re-render with changed dependencies. Additionally, in development, React runs setup+cleanup one extra time immediately after component mounts.

- [react-use-effect-troubleshooting-185] If you have cleanup code without corresponding setup code, it’s usually a code smell:

- [react-use-effect-troubleshooting-186] useEffect ( ( ) => { // 🔴 Avoid: Cleanup logic without corresponding setup logic return ( ) => { doSomething ( ) ; } ; } , [ ] ) ;

- [react-use-effect-troubleshooting-187] Your cleanup logic should be “symmetrical” to the setup logic, and should stop or undo whatever setup did:

- [react-use-effect-troubleshooting-188] useEffect ( ( ) => { const connection = createConnection ( serverUrl , roomId ) ; connection . connect ( ) ; return ( ) => { connection . disconnect ( ) ; } ; } , [ serverUrl , roomId ] ) ;

- [react-use-effect-troubleshooting-189] Learn how the Effect lifecycle is different from the component’s lifecycle.

- [react-use-effect-troubleshooting-190] If your Effect must block the browser from painting the screen, replace useEffect with useLayoutEffect . Note that this shouldn’t be needed for the vast majority of Effects. You’ll only need this if it’s crucial to run your Effect before the browser paint: for example, to measure and position a tooltip before the user sees it.
