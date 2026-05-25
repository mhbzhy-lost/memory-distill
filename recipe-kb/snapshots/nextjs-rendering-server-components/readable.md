- [nextjs-rendering-server-components-1] Server and Client Components

- [nextjs-rendering-server-components-2] By default, layouts and pages are Server Components , which lets you fetch data and render parts of your UI on the server, optionally cache the result, and stream it to the client. When you need interactivity or browser APIs, you can use Client Components to layer in functionality.

- [nextjs-rendering-server-components-3] This page explains how Server and Client Components work in Next.js and when to use them, with examples of how to compose them together in your application.

- [nextjs-rendering-server-components-4] When to use Server and Client Components?

- [nextjs-rendering-server-components-5] The client and server environments have different capabilities. Server and Client components allow you to run logic in each environment depending on your use case.

- [nextjs-rendering-server-components-6] Use Client Components when you need:

- [nextjs-rendering-server-components-7] State and event handlers . E.g. onClick , onChange .

- [nextjs-rendering-server-components-8] Lifecycle logic . E.g. useEffect .

- [nextjs-rendering-server-components-9] Browser-only APIs. E.g. localStorage , window , Navigator.geolocation , etc.

- [nextjs-rendering-server-components-10] Custom hooks .

- [nextjs-rendering-server-components-11] Use Server Components when you need:

- [nextjs-rendering-server-components-12] Fetch data from databases or APIs close to the source.

- [nextjs-rendering-server-components-13] Use API keys, tokens, and other secrets without exposing them to the client.

- [nextjs-rendering-server-components-14] Reduce the amount of JavaScript sent to the browser.

- [nextjs-rendering-server-components-15] Improve the First Contentful Paint (FCP) , and stream content progressively to the client.

- [nextjs-rendering-server-components-16] For example, the <Page> component is a Server Component that fetches data about a post, and passes it as props to the <LikeButton> which handles client-side interactivity.

- [nextjs-rendering-server-components-17] import LikeButton from '@/app/ui/like-button' import { getPost } from '@/lib/data' export default async function Page ({ params , } : { params : Promise <{ id : string }> }) { const { id } = await params const post = await getPost (id) return ( < div > < main > < h1 >{ post .title}</ h1 > { /* ... */ } < LikeButton likes = { post .likes} /> </ main > </ div > ) }

- [nextjs-rendering-server-components-18] 'use client' import { useState } from 'react' export default function LikeButton ({ likes } : { likes : number }) { // ... }

- [nextjs-rendering-server-components-19] How do Server and Client Components work in Next.js?

- [nextjs-rendering-server-components-20] On the server

- [nextjs-rendering-server-components-21] On the server, Next.js uses React's APIs to orchestrate rendering. The rendering work is split into chunks, by individual route segments ( layouts and pages ):

- [nextjs-rendering-server-components-22] Server Components are rendered into a special data format called the React Server Component Payload (RSC Payload).

- [nextjs-rendering-server-components-23] Client Components and the RSC Payload are used to prerender HTML.

- [nextjs-rendering-server-components-24] What is the React Server Component Payload (RSC)?

- [nextjs-rendering-server-components-25] The RSC Payload is a compact binary representation of the rendered React Server Components tree. It's used by React on the client to update the browser's DOM. The RSC Payload contains:

- [nextjs-rendering-server-components-26] The rendered result of Server Components

- [nextjs-rendering-server-components-27] Placeholders for where Client Components should be rendered and references to their JavaScript files

- [nextjs-rendering-server-components-28] Any props passed from a Server Component to a Client Component

- [nextjs-rendering-server-components-29] On the client (first load)

- [nextjs-rendering-server-components-30] Then, on the client:

- [nextjs-rendering-server-components-31] HTML is used to immediately show a fast non-interactive preview of the route to the user.

- [nextjs-rendering-server-components-32] RSC Payload is used to reconcile the Client and Server Component trees.

- [nextjs-rendering-server-components-33] JavaScript is used to hydrate Client Components and make the application interactive.

- [nextjs-rendering-server-components-34] What is hydration?

- [nextjs-rendering-server-components-35] Hydration is React's process for attaching event handlers to the DOM, to make the static HTML interactive.

- [nextjs-rendering-server-components-36] On subsequent navigations:

- [nextjs-rendering-server-components-37] The RSC Payload is prefetched and cached for instant navigation.

- [nextjs-rendering-server-components-38] Client Components are rendered entirely on the client, without the server-rendered HTML.

- [nextjs-rendering-server-components-39] Examples

- [nextjs-rendering-server-components-40] Using Client Components

- [nextjs-rendering-server-components-41] You can create a Client Component by adding the "use client" directive at the top of the file, above your imports.

- [nextjs-rendering-server-components-42] "use client"

- [nextjs-rendering-server-components-43] 'use client' import { useState } from 'react' export default function Counter () { const [ count , setCount ] = useState ( 0 ) return ( < div > < p >{count} likes</ p > < button onClick = {() => setCount (count + 1 )}>Click me</ button > </ div > ) }

- [nextjs-rendering-server-components-44] "use client" is used to declare a boundary between the Server and Client module graphs (trees).

- [nextjs-rendering-server-components-45] Once a file is marked with "use client" , all of its imports and the components it directly renders are included in the client bundle . This means you don’t need to add the directive to every component that is intended for the client.

- [nextjs-rendering-server-components-46] This behavior applies to components that are part of the Client Component’s module graph , which includes the modules it imports and the components it renders directly. It does not apply to Server Components passed as children or other props. Those components are not imported into the Client Component’s module graph. They are rendered on the server and passed to the Client Component as rendered output.

- [nextjs-rendering-server-components-47] See Interleaving Server and Client Components for how Server and Client Components can be combined.

- [nextjs-rendering-server-components-48] Reducing JS bundle size

- [nextjs-rendering-server-components-49] To reduce the size of your client JavaScript bundles, add 'use client' to specific interactive components instead of marking large parts of your UI as Client Components.

- [nextjs-rendering-server-components-50] For example, the <Layout> component contains mostly static elements like a logo and navigation links, but includes an interactive search bar. <Search /> is interactive and needs to be a Client Component, however, the rest of the layout can remain a Server Component.

- [nextjs-rendering-server-components-51] // Client Component import Search from './search' // Server Component import Logo from './logo' // Layout is a Server Component by default export default function Layout ({ children } : { children : React . ReactNode }) { return ( <> < nav > < Logo /> < Search /> </ nav > < main >{children}</ main > </> ) }

- [nextjs-rendering-server-components-52] 'use client' export default function Search () { // ... }

- [nextjs-rendering-server-components-53] Passing data from Server to Client Components

- [nextjs-rendering-server-components-54] You can pass data from Server Components to Client Components using props.

- [nextjs-rendering-server-components-55] import LikeButton from '@/app/ui/like-button' import { getPost } from '@/lib/data' export default async function Page ({ params , } : { params : Promise <{ id : string }> }) { const { id } = await params const post = await getPost (id) return < LikeButton likes = { post .likes} /> }

- [nextjs-rendering-server-components-56] 'use client' export default function LikeButton ({ likes } : { likes : number }) { // ... }

- [nextjs-rendering-server-components-57] Alternatively, you can stream data from a Server Component to a Client Component with the use API . See an example .

- [nextjs-rendering-server-components-58] use

- [nextjs-rendering-server-components-59] Good to know : Props passed to Client Components need to be serializable by React.

- [nextjs-rendering-server-components-60] Interleaving Server and Client Components

- [nextjs-rendering-server-components-61] You can pass Server Components as a prop to a Client Component. This allows you to visually nest server-rendered UI within Client components.

- [nextjs-rendering-server-components-62] A common pattern is to use children to create a slot in a <ClientComponent> . For example, a <Cart> component that fetches data on the server, inside a <Modal> component that uses client state to toggle visibility.

- [nextjs-rendering-server-components-63] 'use client' export default function Modal ({ children } : { children : React . ReactNode }) { return < div >{children}</ div > }

- [nextjs-rendering-server-components-64] Then, in a parent Server Component (e.g. <Page> ), you can pass a <Cart> as the child of the <Modal> :

- [nextjs-rendering-server-components-65] import Modal from './ui/modal' import Cart from './ui/cart' export default function Page () { return ( < Modal > < Cart /> </ Modal > ) }

- [nextjs-rendering-server-components-66] In this pattern, Server Components are rendered on the server ahead of time, even when passed as props to Client Components. The React Server Component Payload contains the rendered result of those Server Components, plus placeholders for where Client Components should be rendered and references to their JavaScript files.

- [nextjs-rendering-server-components-67] Context providers

- [nextjs-rendering-server-components-68] React context is commonly used to share global state like the current theme. However, React context is not supported in Server Components.

- [nextjs-rendering-server-components-69] To use context, create a Client Component that accepts children :

- [nextjs-rendering-server-components-70] 'use client' import { createContext } from 'react' export const ThemeContext = createContext ({}) export default function ThemeProvider ({ children , } : { children : React . ReactNode }) { return < ThemeContext.Provider value = "dark" >{children}</ ThemeContext.Provider > }

- [nextjs-rendering-server-components-71] Then, import it into a Server Component (e.g. layout ):

- [nextjs-rendering-server-components-72] import ThemeProvider from './theme-provider' export default function RootLayout ({ children , } : { children : React . ReactNode }) { return ( < html > < body > < ThemeProvider >{children}</ ThemeProvider > </ body > </ html > ) }

- [nextjs-rendering-server-components-73] Your Server Component will now be able to directly render your provider, and all other Client Components throughout your app will be able to consume this context.

- [nextjs-rendering-server-components-74] Good to know : You should render providers as deep as possible in the tree – notice how ThemeProvider only wraps {children} instead of the entire <html> document. This makes it easier for Next.js to optimize the static parts of your Server Components.

- [nextjs-rendering-server-components-75] Third-party components

- [nextjs-rendering-server-components-76] When using a third-party component that relies on client-only features, you can wrap it in a Client Component to ensure it works as expected.

- [nextjs-rendering-server-components-77] For example, the <Carousel /> can be imported from the acme-carousel package. This component uses useState , but it doesn't yet have the "use client" directive.

- [nextjs-rendering-server-components-78] If you use <Carousel /> within a Client Component, it will work as expected:

- [nextjs-rendering-server-components-79] 'use client' import { useState } from 'react' import { Carousel } from 'acme-carousel' export default function Gallery () { const [ isOpen , setIsOpen ] = useState ( false ) return ( < div > < button onClick = {() => setIsOpen ( true )}>View pictures</ button > { /* Works, since Carousel is used within a Client Component */ } {isOpen && < Carousel />} </ div > ) }

- [nextjs-rendering-server-components-80] However, if you try to use it directly within a Server Component, you'll see an error. This is because Next.js doesn't know <Carousel /> is using client-only features.

- [nextjs-rendering-server-components-81] To fix this, you can wrap third-party components that rely on client-only features in your own Client Components:

- [nextjs-rendering-server-components-82] 'use client' import { Carousel } from 'acme-carousel' export default Carousel

- [nextjs-rendering-server-components-83] Now, you can use <Carousel /> directly within a Server Component:

- [nextjs-rendering-server-components-84] import Carousel from './carousel' export default function Page () { return ( < div > < p >View pictures</ p > { /* Works, since Carousel is a Client Component */ } < Carousel /> </ div > ) }

- [nextjs-rendering-server-components-85] Advice for Library Authors

- [nextjs-rendering-server-components-86] If you’re building a component library, add the "use client" directive to entry points that rely on client-only features. This lets your users import components into Server Components without needing to create wrappers.

- [nextjs-rendering-server-components-87] It's worth noting some bundlers might strip out "use client" directives. You can find an example of how to configure esbuild to include the "use client" directive in the React Wrap Balancer and Vercel Analytics repositories.

- [nextjs-rendering-server-components-88] Preventing environment poisoning

- [nextjs-rendering-server-components-89] JavaScript modules can be shared between both Server and Client Components modules. This means it's possible to accidentally import server-only code into the client. For example, consider the following function:

- [nextjs-rendering-server-components-90] export async function getData () { const res = await fetch ( 'https://external-service.com/data' , { headers : { authorization : process . env . API_KEY , } , }) return res .json () }

- [nextjs-rendering-server-components-91] This function contains an API_KEY that should never be exposed to the client.

- [nextjs-rendering-server-components-92] In Next.js, only environment variables prefixed with NEXT_PUBLIC_ are included in the client bundle. If variables are not prefixed, Next.js replaces them with an empty string.

- [nextjs-rendering-server-components-93] As a result, even though getData() can be imported and executed on the client, it won't work as expected.

- [nextjs-rendering-server-components-94] To prevent accidental usage in Client Components, you can use the server-only package .

- [nextjs-rendering-server-components-95] server-only

- [nextjs-rendering-server-components-96] Then, import the package into a file that contains server-only code:

- [nextjs-rendering-server-components-97] import 'server-only' export async function getData () { const res = await fetch ( 'https://external-service.com/data' , { headers : { authorization : process . env . API_KEY , } , }) return res .json () }

- [nextjs-rendering-server-components-98] Now, if you try to import the module into a Client Component, there will be a build-time error.

- [nextjs-rendering-server-components-99] The corresponding client-only package can be used to mark modules that contain client-only logic like code that accesses the window object.

- [nextjs-rendering-server-components-100] client-only

- [nextjs-rendering-server-components-101] In Next.js, installing server-only or client-only is optional . However, if your linting rules flag extraneous dependencies, you may install them to avoid issues.

- [nextjs-rendering-server-components-102] pnpm add server-only

- [nextjs-rendering-server-components-103] Next.js handles server-only and client-only imports internally to provide clearer error messages when a module is used in the wrong environment. The contents of these packages from NPM are not used by Next.js.

- [nextjs-rendering-server-components-104] Next.js also provides its own type declarations for server-only and client-only , for TypeScript configurations where noUncheckedSideEffectImports is active.

- [nextjs-rendering-server-components-105] noUncheckedSideEffectImports

- [nextjs-rendering-server-components-106] Next Steps

- [nextjs-rendering-server-components-107] use client

- [nextjs-rendering-server-components-108] Was this helpful?
