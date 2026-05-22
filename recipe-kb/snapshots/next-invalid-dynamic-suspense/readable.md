- [next-invalid-dynamic-suspense-1] Invalid Usage of `suspense` Option of `next/dynamic`

- [next-invalid-dynamic-suspense-2] Why This Error Occurred

- [next-invalid-dynamic-suspense-3] You are using { suspense: true } with React version older than 18.

- [next-invalid-dynamic-suspense-4] You are using { suspense: true, ssr: false } .

- [next-invalid-dynamic-suspense-5] You are using { suspense: true, loading } .

- [next-invalid-dynamic-suspense-6] Possible Ways to Fix It

- [next-invalid-dynamic-suspense-7] If you are using { suspense: true } with React version older than 18

- [next-invalid-dynamic-suspense-8] { suspense: true }

- [next-invalid-dynamic-suspense-9] You can try upgrading to React 18 or newer

- [next-invalid-dynamic-suspense-10] If upgrading React is not an option, remove { suspense: true } from next/dynamic usages.

- [next-invalid-dynamic-suspense-11] If you are using { suspense: true, ssr: false }

- [next-invalid-dynamic-suspense-12] { suspense: true, ssr: false }

- [next-invalid-dynamic-suspense-13] Next.js will use React.lazy when suspense is set to true. React 18 or newer will always try to resolve the Suspense boundary on the server. This behavior can not be disabled, thus the ssr: false is ignored with suspense: true .

- [next-invalid-dynamic-suspense-14] You should write code that works in both client-side and server-side.

- [next-invalid-dynamic-suspense-15] If rewriting the code is not an option, remove { suspense: true } from next/dynamic usages.

- [next-invalid-dynamic-suspense-16] If you are using { suspense: true, loading }

- [next-invalid-dynamic-suspense-17] { suspense: true, loading }

- [next-invalid-dynamic-suspense-18] Next.js will use React.lazy when suspense is set to true, when your dynamic-imported component is loading, React will use the closest suspense boundary's fallback.

- [next-invalid-dynamic-suspense-19] You should remove loading from next/dynamic usages, and use <Suspense /> 's fallback prop.

- [next-invalid-dynamic-suspense-20] Useful Links

- [next-invalid-dynamic-suspense-21] Dynamic Import Suspense Usage

- [next-invalid-dynamic-suspense-22] Was this helpful?
