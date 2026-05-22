---
id: next-invalid-dynamic-suspense
kind: debug-recipe
status: accepted
stack:
- react
- nextjs
failure_class: nextjs/dynamic-import
symptoms:
- Invalid usage of suspense option of next/dynamic
fingerprints:
- invalid usage of suspense option
- suspense true with ssr false
- suspense true with loading
- next dynamic React lazy
first_checks:
- 'Check next/dynamic options for suspense: true with ssr: false'
- 'Check next/dynamic options for suspense: true with loading'
- Check whether React 18 or newer is required for the Suspense path
do_not:
- 'Do not combine suspense: true with ssr: false'
- 'Do not provide loading when suspense: true uses the Suspense fallback'
evidence_needed:
- Find the next/dynamic call and its options object
- Capture the nearest Suspense boundary and fallback
- Confirm the React version used by the app
minimal_fix_scope:
- The next/dynamic import options for the affected component
- The Suspense boundary or loading fallback around that component
validation_ladder:
- Render the affected route in development
- Confirm the invalid next/dynamic warning is gone
- Run the route or component smoke test
regression_guard:
- Add a route/component test for the dynamic import loading state
evidence_refs:
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-1
  short_excerpt: Invalid Usage of `suspense` Option of `next/dynamic`
  quote_hash: sha256:7ff9510b8ed9ab44fb4d15be3391b3d3d86036d47497ef60989b5685649174f8
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-3
  short_excerpt: 'You are using { suspense: true } with React version older than 18.'
  quote_hash: sha256:a0b24e729e3180481c5ca22e6b634a32b9af21763c37b4a19ca5dbf862b16c6d
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-4
  short_excerpt: 'You are using { suspense: true, ssr: false } .'
  quote_hash: sha256:678a0b3dd5087382beaa810d00dad42bfa0e646f1603a1ef12d348901e7d60fa
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-5
  short_excerpt: 'You are using { suspense: true, loading } .'
  quote_hash: sha256:0a83b6f4b2dab88fc36fae6db1184f48fcdeb5fd05d1d36f0384d67185df4b4a
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-7
  short_excerpt: 'If you are using { suspense: true } with React version older than
    18'
  quote_hash: sha256:997102ccc1f9e151ba19b73544c0acef0201c1931f5a1d7fb116b22b8b7a9e14
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-8
  short_excerpt: '{ suspense: true }'
  quote_hash: sha256:e10258a808fae45c18ad12d46b8633c8433f2bf23c5586d71bf63002bc77a940
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-10
  short_excerpt: 'If upgrading React is not an option, remove { suspense: true } from
    next/dynamic usages.'
  quote_hash: sha256:d4fe47979447d6e8c4be0db50560e41867137d3eadcd9e23b1fc95ad5c68ecfa
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-11
  short_excerpt: 'If you are using { suspense: true, ssr: false }'
  quote_hash: sha256:d72e3169986cc9942e1d697461daec3ba14afe1d60d148cf0f5d5427a9564a51
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-12
  short_excerpt: '{ suspense: true, ssr: false }'
  quote_hash: sha256:eebb36e31dd22ef3cee7091efd5b910912dafdccefb7f78d2ddc4c1a242f6a8d
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-13
  short_excerpt: 'Next.js will use React.lazy when suspense is set to true. React
    18 or newer will always try to resolve the Suspense boundary on the server. This
    behavior can not be disabled, thus the ssr: false is ignored with suspense: true
    .'
  quote_hash: sha256:1f56bae4302a5d957013a90da4ab3067673f5d0f61f5a761b8908dc8100398aa
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-15
  short_excerpt: 'If rewriting the code is not an option, remove { suspense: true
    } from next/dynamic usages.'
  quote_hash: sha256:32847f0a129f0c606f5c3f826ffa8c42677a17e4fdf8b35b96592ed3534d9139
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-16
  short_excerpt: 'If you are using { suspense: true, loading }'
  quote_hash: sha256:24d1cfc9f13fc648caae310498e50252888219ddfff59a779086c9b6c70bf846
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-17
  short_excerpt: '{ suspense: true, loading }'
  quote_hash: sha256:247340365770080f14c8be5d9216f360ca76037fceb5c8f066598e6d63949130
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-18
  short_excerpt: Next.js will use React.lazy when suspense is set to true, when your
    dynamic-imported component is loading, React will use the closest suspense boundary's
    fallback.
  quote_hash: sha256:12c1528f567d5c018a684cfa50fbec162e1c5e1db8f71f67c72d4775fcb56427
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-19
  short_excerpt: You should remove loading from next/dynamic usages, and use <Suspense
    /> 's fallback prop.
  quote_hash: sha256:f357f0b60d29f821f37b186c013c5bfdfe559cfff8ace4ab5dc5f1712de6ee54
- source_id: next-invalid-dynamic-suspense
  url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  final_url: https://nextjs.org/docs/messages/invalid-dynamic-suspense
  source_type: official_error_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: next-invalid-dynamic-suspense-21
  short_excerpt: Dynamic Import Suspense Usage
  quote_hash: sha256:e593eed8eb41956263c751e1b5dec103a9b4cda6938a5f8bb8a25cd59014e54b
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# next-invalid-dynamic-suspense

## Failure Class
nextjs/dynamic-import

## Symptoms
- Invalid usage of suspense option of next/dynamic

## Fingerprints
- invalid usage of suspense option
- suspense true with ssr false
- suspense true with loading
- next dynamic React lazy

## First Checks
- Check next/dynamic options for suspense: true with ssr: false
- Check next/dynamic options for suspense: true with loading
- Check whether React 18 or newer is required for the Suspense path

## Do Not Patch Yet
- Do not combine suspense: true with ssr: false
- Do not provide loading when suspense: true uses the Suspense fallback

## Evidence Needed
- Find the next/dynamic call and its options object
- Capture the nearest Suspense boundary and fallback
- Confirm the React version used by the app

## Minimal Fix Scope
- The next/dynamic import options for the affected component
- The Suspense boundary or loading fallback around that component

## Validation Ladder
- Render the affected route in development
- Confirm the invalid next/dynamic warning is gone
- Run the route or component smoke test

## Regression Guard
- Add a route/component test for the dynamic import loading state

## Reviewer Notes
