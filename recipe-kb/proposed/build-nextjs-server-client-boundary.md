---
id: build-nextjs-server-client-boundary
kind: build-recipe
status: proposed
stack:
- react
- nextjs
trigger:
  file_pattern: app/**/*.{ts,tsx}
  code_signals:
  - useState
  - useEffect
  - useReducer
  - useContext
  description: 在 Next.js App Router 的 Server Component 中使用了 React hooks
correct_pattern:
- 需要 client interactivity 的组件必须在文件顶部声明 'use client'
- Server Component 只能使用 async/await、server actions、fetch 等服务端 API
- 将 Client Component 放在组件树的叶子节点，最小化客户端 bundle
- 数据获取优先在 Server Component 中完成，通过 props 传递给 Client Component
decision_context:
- condition: 组件需要 useState / useEffect 等 hooks
  recommendation: 标记为 Client Component ('use client')
- condition: 组件只需要一次性数据获取
  recommendation: 保持 Server Component，使用 async function + fetch
- condition: 组件需要事件处理（onClick, onChange）
  recommendation: 标记为 Client Component
- condition: 组件只做静态渲染，无交互
  recommendation: 保持 Server Component（默认）
constraints:
- Server Component 不能使用 React hooks (useState, useEffect, useReducer, useContext)
- Server Component 不能使用 browser-only API (window, document, localStorage)
- Server Component 不能使用事件处理器 (onClick, onChange, onSubmit)
- '''use client'' 声明必须在文件顶部，在所有 import 之前'
do_not:
- 不要在未标记 'use client' 的 app/ 组件中使用 React hooks
- 不要把整个页面标记为 'use client' 只为了一个小交互——拆分出 Client Component
- 不要在 Server Component 中 import 使用了 hooks 的库而不标记 'use client'
defaults:
- app/ 下的组件默认是 Server Component
- 只在需要 client interactivity 的最小子树标记 'use client'
validation:
- next build 成功，无 server component hooks error
- next dev 无 'useState is not a function' 或类似 warning
- 检查 bundle analyzer 确认 Client Component 没有包含不必要的服务端代码
related_debug_recipes:
- react-invalid-hook-call
evidence_refs:
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-1
  short_excerpt: Server and Client Components
  quote_hash: sha256:5565afdafca1d83819793d570cd76797dacd74e0cb39e9c906d278c854cf777d
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-2
  short_excerpt: By default, layouts and pages are Server Components , which lets
    you fetch data and render parts of your UI on the server, optionally cache the
    result, and stream it to the client. When you need interactivity or browser APIs,
    you can use Client Components to layer in functionality.
  quote_hash: sha256:7d6c2b0a1e837ec2a3933270a2f3c38f716a8babb297968ca39c1ff3cf12c294
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-3
  short_excerpt: This page explains how Server and Client Components work in Next.js
    and when to use them, with examples of how to compose them together in your application.
  quote_hash: sha256:fb2e229e43cc7a6459e92d598f305a553fa67a26cee69fea13ed2e61e1482149
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-4
  short_excerpt: When to use Server and Client Components?
  quote_hash: sha256:e5f5c751f08c82a9c47dc57e2e3dc02a1ac4f1d726f6b31475232e39a73b9e30
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-5
  short_excerpt: The client and server environments have different capabilities. Server
    and Client components allow you to run logic in each environment depending on
    your use case.
  quote_hash: sha256:5139ab6cdd2b9e11124b2d596a1c15320b9fb49970d6ca9c21f76b812a93d291
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-6
  short_excerpt: 'Use Client Components when you need:'
  quote_hash: sha256:87b655304c54f12e6f02d7dcdb841c0bcf09f83c39ca6d9fab77230eaaf4bc5f
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-8
  short_excerpt: Lifecycle logic . E.g. useEffect .
  quote_hash: sha256:b60b067b369814ca52df284199c1edbe0e9630500918ea92f814d6504bfac9f2
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-11
  short_excerpt: 'Use Server Components when you need:'
  quote_hash: sha256:8066152e2017bc2f822aff3e5d0f9d08f9f0fa209827ae15ad36294e145ceb0c
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-16
  short_excerpt: For example, the <Page> component is a Server Component that fetches
    data about a post, and passes it as props to the <LikeButton> which handles client-side
    interactivity.
  quote_hash: sha256:9355aa15385b226a2394bc424b56a833e048dec84278dc7650c1aef808635824
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-18
  short_excerpt: '''use client'' import { useState } from ''react'' export default
    function LikeButton ({ likes } : { likes : number }) { // ... }'
  quote_hash: sha256:58537d4774f2c6184572aa2c1cd7eada24b7bf407588142857c5472019277c71
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-19
  short_excerpt: How do Server and Client Components work in Next.js?
  quote_hash: sha256:ee87d9942d66068008b4009f85bafcde8537a7b20a1a7b30beed6cddb853ba76
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-22
  short_excerpt: Server Components are rendered into a special data format called
    the React Server Component Payload (RSC Payload).
  quote_hash: sha256:b41bb9742693b84da720851b24937fe04d433363c6b0c1d5c0ff0a66d50a16d0
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-23
  short_excerpt: Client Components and the RSC Payload are used to prerender HTML.
  quote_hash: sha256:88dd806f43a3c6369ac573b22ea93d28dc6452259c0bd705d248697a0ef8421d
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-25
  short_excerpt: 'The RSC Payload is a compact binary representation of the rendered
    React Server Components tree. It''s used by React on the client to update the
    browser''s DOM. The RSC Payload contains:'
  quote_hash: sha256:324b604ea965381ca2626a071df5f0f39334cfec85a4aaa569f58772b4b6485d
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-26
  short_excerpt: The rendered result of Server Components
  quote_hash: sha256:09ef9284b9e28547c9b125d962c36b58779d960d9d10083942af91c0e3abadff
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-27
  short_excerpt: Placeholders for where Client Components should be rendered and references
    to their JavaScript files
  quote_hash: sha256:77b8066e0b8c2deb3207c944fda634b4806871a3ae11c0b216f4b00677820a29
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-33
  short_excerpt: JavaScript is used to hydrate Client Components and make the application
    interactive.
  quote_hash: sha256:178a5f7850db282b8636d86d59966b152c7f822f3418af46cdd0074f35097d5e
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-38
  short_excerpt: Client Components are rendered entirely on the client, without the
    server-rendered HTML.
  quote_hash: sha256:5d61457610c3a7e784d3d73a30a6874c797760bd460e86ae8cc5d5fcee7b5c32
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-40
  short_excerpt: Using Client Components
  quote_hash: sha256:be8c796d5680334608e405856e548c0f33299acccb6dc9cadc5067c2ddbf1e36
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-41
  short_excerpt: You can create a Client Component by adding the "use client" directive
    at the top of the file, above your imports.
  quote_hash: sha256:5405e104a3e29bfb5d2c235a161dbe3483321a985a9d533d42befeaedaa24700
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-42
  short_excerpt: '"use client"'
  quote_hash: sha256:66eefa5f11f9135fcb21ad285b4fe7d8f32ff20e3f34db40e3a16276d81ba9c2
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-43
  short_excerpt: '''use client'' import { useState } from ''react'' export default
    function Counter () { const [ count , setCount ] = useState ( 0 ) return ( < div
    > < p >{count} likes</ p > < button onClick = {() => setCount (count + 1 )}>Click
    me</ button > </ div > ) }'
  quote_hash: sha256:acd446883789dedf5c79a2c7ebede379df480aca92406b5b10bd986bb736d353
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-44
  short_excerpt: '"use client" is used to declare a boundary between the Server and
    Client module graphs (trees).'
  quote_hash: sha256:54e5bed079d70237e3e7628eebac34e1fa404d4ca7dfacb9d486b6714732fedf
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-45
  short_excerpt: Once a file is marked with "use client" , all of its imports and
    the components it directly renders are included in the client bundle . This means
    you don’t need to add the directive to every component that is intended for the
    client.
  quote_hash: sha256:fcbb7fb15b8c0f4846a38a86391f006ccde460967ad1ab7db8fbe661213fe959
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-46
  short_excerpt: This behavior applies to components that are part of the Client Component’s
    module graph , which includes the modules it imports and the components it renders
    directly. It does not apply to Server Components passed as children or other props.
    Those components are not imported into the Client Component’s module graph. They
    are rendered on the server and passed to the Client Component as rendered output.
  quote_hash: sha256:088f650e135ce29e27aafa0ac7157bb75279e4d60307093de0948e33a53a3731
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-47
  short_excerpt: See Interleaving Server and Client Components for how Server and
    Client Components can be combined.
  quote_hash: sha256:bb8c57f40899bf307386be5f5cd632d1fdc7816fbd624da0eff1d94153a37df3
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-49
  short_excerpt: To reduce the size of your client JavaScript bundles, add 'use client'
    to specific interactive components instead of marking large parts of your UI as
    Client Components.
  quote_hash: sha256:017d6258c51c03974bebdba5dd7e266ef30938ebd0f6c0e2cf49da3a9d0368ff
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-52
  short_excerpt: '''use client'' export default function Search () { // ... }'
  quote_hash: sha256:06799c87e8ee5e6dd5daa4160b262bc1a545fdc255f797706104ea90b7b1b28b
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-53
  short_excerpt: Passing data from Server to Client Components
  quote_hash: sha256:ea78252571390cfa86c9984c615df17a166062e7a45f514c58a31bb3f864895e
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-54
  short_excerpt: You can pass data from Server Components to Client Components using
    props.
  quote_hash: sha256:12de549a732c0783887543b477bb28bae797b2678fb41f0886982325763c226c
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-56
  short_excerpt: '''use client'' export default function LikeButton ({ likes } : {
    likes : number }) { // ... }'
  quote_hash: sha256:23594efaa73ffb1397511816cf778aacc5b01f79411de4c29d5a6a94937008e4
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-59
  short_excerpt: 'Good to know : Props passed to Client Components need to be serializable
    by React.'
  quote_hash: sha256:916416578b2084c9a988861c31bd4f6bb88e2d0967ed9b453555a607e25476fb
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-60
  short_excerpt: Interleaving Server and Client Components
  quote_hash: sha256:09f6d4c896a4c6a1e2cbf7b22d008bfa9479109d333be71fee6338e34869659f
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-61
  short_excerpt: You can pass Server Components as a prop to a Client Component. This
    allows you to visually nest server-rendered UI within Client components.
  quote_hash: sha256:723ba3a3e164537267b774f6874e099569bdac23aeb93b774d47f67121bbbc54
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-63
  short_excerpt: '''use client'' export default function Modal ({ children } : { children
    : React . ReactNode }) { return < div >{children}</ div > }'
  quote_hash: sha256:78c44e3b845b36dc53035a8afc50119ddaf21902cd5403a1e3dae4154bc2a0e5
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-66
  short_excerpt: In this pattern, Server Components are rendered on the server ahead
    of time, even when passed as props to Client Components. The React Server Component
    Payload contains the rendered result of those Server Components, plus placeholders
    for where Client Components should be rendered and references to their JavaScript
    files.
  quote_hash: sha256:17d008d4dcdb5ae8ef5658defa77ac02861f7c7ab7e003943ee0f7d1c6bcb391
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-68
  short_excerpt: React context is commonly used to share global state like the current
    theme. However, React context is not supported in Server Components.
  quote_hash: sha256:258aefc193672512d763db2e84a986730e56498dc7ecc07d0147e0cb57a2d172
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-70
  short_excerpt: '''use client'' import { createContext } from ''react'' export const
    ThemeContext = createContext ({}) export default function ThemeProvider ({ children
    , } : { children : React . ReactNode }) { return < ThemeContext.Provider value
    = "dark" >{children}</ ThemeContext.Provider > }'
  quote_hash: sha256:30556d2ce083f13c1680a6023ca209b0c7d3d0186d6cdde80cd9372b8c796370
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-73
  short_excerpt: Your Server Component will now be able to directly render your provider,
    and all other Client Components throughout your app will be able to consume this
    context.
  quote_hash: sha256:7f3a454f6998ddbe275a056451e18004d4412017cbcf8ad4a1a29599ba8bbb0c
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-74
  short_excerpt: 'Good to know : You should render providers as deep as possible in
    the tree – notice how ThemeProvider only wraps {children} instead of the entire
    <html> document. This makes it easier for Next.js to optimize the static parts
    of your Server Components.'
  quote_hash: sha256:f1efa825271e05806d0a50b0f11e27267b941270dd7b520fd2b75d088f35b361
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-77
  short_excerpt: For example, the <Carousel /> can be imported from the acme-carousel
    package. This component uses useState , but it doesn't yet have the "use client"
    directive.
  quote_hash: sha256:83aee805f6934f81a39e10c38e7c3f0c1faf7820a3b94b32db1cb34c756e6519
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-79
  short_excerpt: '''use client'' import { useState } from ''react'' import { Carousel
    } from ''acme-carousel'' export default function Gallery () { const [ isOpen ,
    setIsOpen ] = useState ( false ) return ( < div > < button onClick = {() => setIsOpen
    ( true )}>View pictures</ button > { /* Works, since Carousel is used within a
    Client Component */ } {isOpen && < Carousel />} </ div > ) }'
  quote_hash: sha256:1a164df5a4626f76272c34735fc7ff2708cb1e2483b0b3b65d000f4e3fcbcc0e
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-81
  short_excerpt: 'To fix this, you can wrap third-party components that rely on client-only
    features in your own Client Components:'
  quote_hash: sha256:a8cef14895ade3fb0385057c131adfdea4f386118778cf70b5408128c47d61cb
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-82
  short_excerpt: '''use client'' import { Carousel } from ''acme-carousel'' export
    default Carousel'
  quote_hash: sha256:349adc1643ce1c0758ff12d5c7a1a5324e74de0553141f1caa01a68e68a1c9d8
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-86
  short_excerpt: If you’re building a component library, add the "use client" directive
    to entry points that rely on client-only features. This lets your users import
    components into Server Components without needing to create wrappers.
  quote_hash: sha256:ca8fb927c4961502cf27f90e4174b4602c30af9fa5fa5703265f2ddfbab4c398
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-87
  short_excerpt: It's worth noting some bundlers might strip out "use client" directives.
    You can find an example of how to configure esbuild to include the "use client"
    directive in the React Wrap Balancer and Vercel Analytics repositories.
  quote_hash: sha256:4ddd6fb65e1037c4f7dd43afd463ba553ede764ead56bbf331cff741ac5cb242
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-89
  short_excerpt: 'JavaScript modules can be shared between both Server and Client
    Components modules. This means it''s possible to accidentally import server-only
    code into the client. For example, consider the following function:'
  quote_hash: sha256:3b3c727fa7eeb79af2f9602aa6abff75e2c9554423023c5ee74cc21df51bf357
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-94
  short_excerpt: To prevent accidental usage in Client Components, you can use the
    server-only package .
  quote_hash: sha256:e27edb1453e194080e0e324801b7bfb171fca958cae76da2b1e68f851159acc0
- source_id: nextjs-rendering-server-components
  url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  final_url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  source_type: official_guide
  captured_at: '2026-05-25T10:00:00Z'
  section_anchor: root
  span_id: nextjs-rendering-server-components-107
  short_excerpt: use client
  quote_hash: sha256:f8014271a069d8d16f4d603e948c4beae952cea43611dca0968a36c582cda5b2
review: []
maintenance:
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-nextjs-server-client-boundary

## Trigger
**在 Next.js App Router 的 Server Component 中使用了 React hooks**
- file pattern: `app/**/*.{ts,tsx}`
- code signal: `useState`
- code signal: `useEffect`
- code signal: `useReducer`
- code signal: `useContext`

## Correct Pattern
- 需要 client interactivity 的组件必须在文件顶部声明 'use client'
- Server Component 只能使用 async/await、server actions、fetch 等服务端 API
- 将 Client Component 放在组件树的叶子节点，最小化客户端 bundle
- 数据获取优先在 Server Component 中完成，通过 props 传递给 Client Component

## Decision Context
- **组件需要 useState / useEffect 等 hooks** → 标记为 Client Component ('use client')
- **组件只需要一次性数据获取** → 保持 Server Component，使用 async function + fetch
- **组件需要事件处理（onClick, onChange）** → 标记为 Client Component
- **组件只做静态渲染，无交互** → 保持 Server Component（默认）

## Constraints
- Server Component 不能使用 React hooks (useState, useEffect, useReducer, useContext)
- Server Component 不能使用 browser-only API (window, document, localStorage)
- Server Component 不能使用事件处理器 (onClick, onChange, onSubmit)
- 'use client' 声明必须在文件顶部，在所有 import 之前

## Do Not
- 不要在未标记 'use client' 的 app/ 组件中使用 React hooks
- 不要把整个页面标记为 'use client' 只为了一个小交互——拆分出 Client Component
- 不要在 Server Component 中 import 使用了 hooks 的库而不标记 'use client'

## Defaults
- app/ 下的组件默认是 Server Component
- 只在需要 client interactivity 的最小子树标记 'use client'

## Validation
- next build 成功，无 server component hooks error
- next dev 无 'useState is not a function' 或类似 warning
- 检查 bundle analyzer 确认 Client Component 没有包含不必要的服务端代码

## Related Debug Recipes
- react-invalid-hook-call

## Reviewer Notes
