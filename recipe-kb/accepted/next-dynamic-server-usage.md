---
id: next-dynamic-server-usage
kind: debug-recipe
status: accepted
stack:
- react
- nextjs
failure_class: nextjs/dynamic-rendering
symptoms:
- DynamicServerError or Dynamic Server Usage is thrown during static generation
fingerprints:
- DynamicServerError
- Dynamic Server Usage
- cookies or headers not bound to the same call stack
- static generation dynamic function
first_checks:
- Check whether cookies, headers, or another dynamic function is called outside its
  async context
- Check setTimeout, setInterval, or un-awaited promise boundaries around dynamic functions
- Check whether the route should be dynamic instead of statically generated
do_not:
- Do not catch and swallow DynamicServerError manually
- Do not move cookies or headers into delayed callbacks to satisfy static generation
evidence_needed:
- Identify the dynamic function call site
- Trace the async call stack between the route render and the dynamic function
- Decide whether the route is intended to be static or dynamic
minimal_fix_scope:
- The route, server component, or helper that reads dynamic request data
- The async boundary that loses request context
validation_ladder:
- Build or render the affected route locally
- Confirm the dynamic function is called in the same async context
- Run the route smoke or build test
regression_guard:
- Add a route-level test or build smoke that exercises the dynamic function path
evidence_refs:
- source_id: next-dynamic-server-error
  url: https://nextjs.org/docs/messages/dynamic-server-error
  final_url: https://nextjs.org/docs/messages/dynamic-server-error
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-dynamic-server-error-1
  short_excerpt: DynamicServerError - Dynamic Server Usage
  quote_hash: sha256:51f71ed45e5daa7555069b727f4658a624dc7725f4d4654399402635ba268c59
- source_id: next-dynamic-server-error
  url: https://nextjs.org/docs/messages/dynamic-server-error
  final_url: https://nextjs.org/docs/messages/dynamic-server-error
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-dynamic-server-error-4
  short_excerpt: While generating static pages, Next.js will throw a DynamicServerError
    if it detects usage of a dynamic function, and catch it to automatically opt the
    page into dynamic rendering. However, when it's uncaught, it will result in this
    build-time error.
  quote_hash: sha256:d0d17b9301b2c6f08b95f7d9fabc34f7e5cecf5eb5bdd346d5b45248f162a9cc
- source_id: next-dynamic-server-error
  url: https://nextjs.org/docs/messages/dynamic-server-error
  final_url: https://nextjs.org/docs/messages/dynamic-server-error
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-dynamic-server-error-6
  short_excerpt: Async Context is a way to pass data within the same call stack, even
    through asynchronous operations. This is very useful in Next.js, where functions
    like cookies or headers might be called from anywhere within a React component
    tree or other functions during React rendering.
  quote_hash: sha256:6179e049231eef733536987717395bcc74cbf34749a055deb18e9992afb3075c
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# next-dynamic-server-usage

## Failure Class
nextjs/dynamic-rendering

## Symptoms
- DynamicServerError or Dynamic Server Usage is thrown during static generation

## Fingerprints
- DynamicServerError
- Dynamic Server Usage
- cookies or headers not bound to the same call stack
- static generation dynamic function

## First Checks
- Check whether cookies, headers, or another dynamic function is called outside its async context
- Check setTimeout, setInterval, or un-awaited promise boundaries around dynamic functions
- Check whether the route should be dynamic instead of statically generated

## Do Not Patch Yet
- Do not catch and swallow DynamicServerError manually
- Do not move cookies or headers into delayed callbacks to satisfy static generation

## Evidence Needed
- Identify the dynamic function call site
- Trace the async call stack between the route render and the dynamic function
- Decide whether the route is intended to be static or dynamic

## Minimal Fix Scope
- The route, server component, or helper that reads dynamic request data
- The async boundary that loses request context

## Validation Ladder
- Build or render the affected route locally
- Confirm the dynamic function is called in the same async context
- Run the route smoke or build test

## Regression Guard
- Add a route-level test or build smoke that exercises the dynamic function path

## Reviewer Notes
