---
id: build-react-effect-dependency-rerun-loop
kind: build-recipe
status: proposed
stack:
- react
trigger:
  file_pattern: ''
  code_signals: []
  description: 代码可能触发 react/effect-lifecycle 类故障（Effect keeps re-running in an infinite
    cycle or runs twice on mount）
correct_pattern: []
decision_context: []
constraints:
- Do not remove dependencies from the array to hide the loop
- Do not disable Strict Mode before proving cleanup mirrors setup
do_not:
- Do not remove dependencies from the array to hide the loop
- Do not disable Strict Mode before proving cleanup mirrors setup
defaults: []
validation:
- Log or inspect dependency identity across two renders
- Run the component in development Strict Mode
- Run the focused component or hook test
related_debug_recipes:
- react-effect-dependency-rerun-loop
evidence_refs:
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-17
  short_excerpt: Troubleshooting My Effect runs twice when the component mounts My
    Effect runs after every re-render My Effect keeps re-running in an infinite cycle
    My cleanup logic runs even though my component didn’t unmount My Effect does something
    visual, and I see a flicker before it runs
  quote_hash: sha256:377f35de0b7e1e7940d08bc854470fc7817ae1b73df587eb49b8a170fb95bcaf
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-18
  short_excerpt: My Effect runs twice when the component mounts
  quote_hash: sha256:0b2e22a49911772c690b37047b2e872f7ab036a61e95f8228ed14c44c5209f3f
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-20
  short_excerpt: My Effect keeps re-running in an infinite cycle
  quote_hash: sha256:18cd1215da445f391bbf52d5f54190f92bf1cd432b7e5f97f570124132841933
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-27
  short_excerpt: 'setup : The function with your Effect’s logic. Your setup function
    may also optionally return a cleanup function. When your component commits , React
    will run your setup function. After every commit with changed dependencies, React
    will first run the cleanup function (if you provided it) with the old values,
    and then run your setup function with the new values. After your component is
    removed from the DOM, React will run your cleanup function.'
  quote_hash: sha256:529215f8c9725d7b5543613798dbcb3490bb76ecc04a861dc676bf333c5358aa
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-33
  short_excerpt: When Strict Mode is on, React will run one extra development-only
    setup+cleanup cycle before the first real setup. This is a stress-test that ensures
    that your cleanup logic “mirrors” your setup logic and that it stops or undoes
    whatever the setup is doing. If this causes a problem, implement the cleanup function.
  quote_hash: sha256:4ccd35a6bd24771f4e93b6e9d488f6cee5f7fb41c55987e797f24bf7d6008703
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-45
  short_excerpt: A setup function with setup code that connects to that system. It
    should return a cleanup function with cleanup code that disconnects from that
    system.
  quote_hash: sha256:685d336e0b472fc9c9327ccb95e139dc9198c6788a37ae2a5406869a635ee3f7
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-46
  short_excerpt: It should return a cleanup function with cleanup code that disconnects
    from that system.
  quote_hash: sha256:0cc6a1da5e9809b502afadee5b7a72408c1f531225adaa5e0bb0f5d4e2c282bf
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-48
  short_excerpt: 'React calls your setup and cleanup functions whenever it’s necessary,
    which may happen multiple times:'
  quote_hash: sha256:c29521fae23df5eb1db0cf8aad71abdd5af0c575c7c85c804e08876e2e84b91b
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-56
  short_excerpt: To help you find bugs, in development React runs setup and cleanup
    one extra time before the setup . This is a stress-test that verifies your Effect’s
    logic is implemented correctly. If this causes visible issues, your cleanup function
    is missing some logic. The cleanup function should stop or undo whatever the setup
    function was doing. The rule of thumb is that the user shouldn’t be able to distinguish
    between the setup being called once (as in production) and a setup → cleanup →
    setup sequence (as in development). See common solutions.
  quote_hash: sha256:68b0164431e94d8208ba43b57255346881f68fad15a7527006f6e2ef3182cd94
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-87
  short_excerpt: In this example, a cleanup function is not needed because the MapWidget
    class manages only the DOM node that was passed to it. After the Map React component
    is removed from the tree, both the DOM node and the MapWidget class instance will
    be automatically garbage-collected by the browser JavaScript engine.
  quote_hash: sha256:a56d61db947298c7e1910aabc78de623be6801047ab29b866722338004fe0be9
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-93
  short_excerpt: 'You can also rewrite using the async / await syntax, but you still
    need to provide a cleanup function:'
  quote_hash: sha256:ceccd35d0b7a26c7343acd3b014ab711ada0906f85234c7147d59bd180543945
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-164
  short_excerpt: This is a stress-test that verifies your Effect’s logic is implemented
    correctly. If this causes visible issues, your cleanup function is missing some
    logic. The cleanup function should stop or undo whatever the setup function was
    doing. The rule of thumb is that the user shouldn’t be able to distinguish between
    the setup being called once (as in production) and a setup → cleanup → setup sequence
    (as in development).
  quote_hash: sha256:6e22935eb1b9ace9ee06556bdb8b616d8551e1f3b494e0623255e6811797c279
- source_id: react-use-effect-troubleshooting
  url: https://react.dev/reference/react/useEffect
  final_url: https://react.dev/reference/react/useEffect
  source_type: official_doc
  captured_at: '2026-05-21T09:50:51.121768Z'
  section_anchor: root
  span_id: react-use-effect-troubleshooting-184
  short_excerpt: The cleanup function runs not only during unmount, but before every
    re-render with changed dependencies. Additionally, in development, React runs
    setup+cleanup one extra time immediately after component mounts.
  quote_hash: sha256:b0d2f37fdd99bb54c0c31df16255f4ee583f07fc99c4495d9e3e9a9054d58e3e
review: []
maintenance:
  state: proposed
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# build-react-effect-dependency-rerun-loop

## Trigger
**代码可能触发 react/effect-lifecycle 类故障（Effect keeps re-running in an infinite cycle or runs twice on mount）**

## Correct Pattern


## Constraints
- Do not remove dependencies from the array to hide the loop
- Do not disable Strict Mode before proving cleanup mirrors setup

## Do Not
- Do not remove dependencies from the array to hide the loop
- Do not disable Strict Mode before proving cleanup mirrors setup

## Validation
- Log or inspect dependency identity across two renders
- Run the component in development Strict Mode
- Run the focused component or hook test

## Related Debug Recipes
- react-effect-dependency-rerun-loop

## Reviewer Notes
