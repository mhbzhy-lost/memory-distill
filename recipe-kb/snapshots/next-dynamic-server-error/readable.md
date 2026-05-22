- [next-dynamic-server-error-1] DynamicServerError - Dynamic Server Usage

- [next-dynamic-server-error-2] Why This Message Occurred

- [next-dynamic-server-error-3] You attempted to use a Next.js function that depends on Async Context (such as headers or cookies from next/headers ) but it was not bound to the same call stack as the function that ran it (e.g., calling cookies() inside of a setTimeout or setInterval ).

- [next-dynamic-server-error-4] While generating static pages, Next.js will throw a DynamicServerError if it detects usage of a dynamic function, and catch it to automatically opt the page into dynamic rendering. However, when it's uncaught, it will result in this build-time error.

- [next-dynamic-server-error-5] What is Async Context?

- [next-dynamic-server-error-6] Async Context is a way to pass data within the same call stack, even through asynchronous operations. This is very useful in Next.js, where functions like cookies or headers might be called from anywhere within a React component tree or other functions during React rendering.

- [next-dynamic-server-error-7] Scenarios that can cause this to happen

- [next-dynamic-server-error-8] The function was called inside of a setTimeout or setInterval , causing the value to be read outside of the call stack that the context was bound to.

- [next-dynamic-server-error-9] The function was called after an async operation, but the promise wasn't awaited. This can cause the function to be called after the async operation has completed, resulting in a new execution context and loss of the original async context.

- [next-dynamic-server-error-10] Example of Incorrect Usage

- [next-dynamic-server-error-11] import { cookies } from 'next/headers' async function getCookieData () { return new Promise ((resolve) => setTimeout ( async () => { // cookies will be called outside of the async context, causing a build-time error const cookieStore = await cookies () resolve ( cookieStore .getAll ()) } , 1000 ) ) } export default async function Page () { const cookieData = await getCookieData () return < div >Hello World</ div > }

- [next-dynamic-server-error-12] Possible Ways to Fix It

- [next-dynamic-server-error-13] Manage Execution Contexts Correctly: JavaScript operations like setTimeout , setInterval , event handlers, and Promises create new execution contexts. You need to maintain the async context when using these operations. Some strategies include:

- [next-dynamic-server-error-14] Invoke the function that depends on the async context outside of the function that creates a new execution context.

- [next-dynamic-server-error-15] Ensure that you await Promises that invoke a function that depends on async context, otherwise the function may be called after the async operation has completed.

- [next-dynamic-server-error-16] Example of Correct Usage

- [next-dynamic-server-error-17] import { cookies } from 'next/headers' async function getCookieData () { const cookieStore = await cookies () const cookieData = cookieStore .getAll () return new Promise ((resolve) => setTimeout (() => { resolve (cookieData) } , 1000 ) ) } export default async function Page () { const cookieData = await getCookieData () return < div >Hello World</ div > }

- [next-dynamic-server-error-18] Was this helpful?
