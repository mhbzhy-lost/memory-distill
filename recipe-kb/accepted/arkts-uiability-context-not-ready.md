---
id: arkts-uiability-context-not-ready
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/ability-lifecycle
symptoms:
- Accessing UIAbilityContext returns null or throws because context is accessed before
  onCreate initializes it
fingerprints:
- UIAbilityContext
- Context is null
- context not ready
- getContext
- context 为空
first_checks:
- Check whether context is accessed in a member initializer, constructor, or static
  field before onCreate
- Check whether getContext() is called on a component that has not yet been attached
  to an AbilityStage
- Check whether the context is passed through a closure that captures a stale null
  reference
do_not:
- Do not cache UIAbilityContext in a module-level variable before onCreate completes
- Do not pass context to child components via property assignment before the context
  is initialized in onCreate
evidence_needed:
- Capture the stack trace showing context is null at the call site
- Identify the lifecycle stage when the null context is accessed
minimal_fix_scope:
- The context access site and the lifecycle callback it is in
- The state initialization order in the UIAbility subclass
validation_ladder:
- Move context access to onCreate or a later callback and verify no null reference
- Verify child components receive context only after it is initialized
- Run the ability lifecycle test covering context availability
regression_guard:
- Add an ability test asserting context is non-null from onCreate onwards
evidence_refs:
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-2
  short_excerpt: '## 概述 当用户在执行应用启动、应用前后台切换、应用退出等操作时，系统会触发相关应用组件的生命周期回调。其中，UIAbility组件的核心生命周期回调包括[onCreate](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#oncreate)、[onForeground](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onforeground)、[onBackground](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onbackground)、[onDestroy](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#ondestroy)。作为一种包含UI的应用组件，UIAbility的生命周期不可避免地与[WindowStage](../../application-dev/windowmanager/application-window-stage.md)的生命周期存在关联关系。
    UIAbility的生命周期示意图如下所示。 ![UIAbility-Life-Cyc'
  quote_hash: sha256:c9144b92c2c140625d768cf96f1cac8b1efeb5414177127e1265d827e1cb45ea
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-3
  short_excerpt: '## 生命周期回调 > **说明：** > > - 生命周期回调是在应用主线程执行，为了确保应用性能，建议在生命周期回调中，仅执行必要的轻量级操作。对于耗时任务，推荐采用异步处理或交由子线程执行，避免阻塞主线程。
    > - 如果需要感知UIAbility生命周期变化，开发者可以使用[ApplicationContext注册接口](../reference/apis-ability-kit/js-apis-inner-application-applicationContext.md#applicationcontextonabilitylifecycle)监听UIAbility生命周期变化。详见[监听UIAbility生命周期变化](./application-context-stage.md#监听uiability生命周期变化)。'
  quote_hash: sha256:7b261a53f53b8656a87963e08f7fe74ea145babbedbc8c04367fcd88dfb85299
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-4
  short_excerpt: '### onCreate() 在首次创建UIAbility实例时，系统触发[onCreate()](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#oncreate)回调。开发者可以在该回调中执行UIAbility整个生命周期中仅发生一次的启动逻辑。
    ```ts import { AbilityConstant, UIAbility, Want } from ''@kit.AbilityKit''; export
    default class EntryAbility extends UIAbility { onCreate(want: Want, launchParam:
    AbilityConstant.LaunchParam): void { // 执行UIAbility整个生命周期中仅发生一次的业务逻辑 } // ...
    } ```'
  quote_hash: sha256:b5121e11878a486700a19c58cdd0b7b987c4d729d896e9ee1cae9e6a2da051d8
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-10
  short_excerpt: '### onDestroy() 在[UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)实例销毁之前，系统触发[onDestroy](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#ondestroy)回调。该回调是UIAbility接收到的最后一个生命周期回调，开发者可以在onDestroy()回调中进行系统资源的释放、数据的保存等操作。
    例如，开发者调用[terminateSelf()](../reference/apis-ability-kit/js-apis-inner-application-uiAbilityContext.md#terminateself)方法通知系统停止当前UIAbility实例时，系统会触发onDestroy()回调。
    <!--RP1-->再比如，用户在最近任务列表中上滑关闭UIAbility实例时，系统会触发onDestroy()回调。<!--RP1End--> ```ts
    import { UIAbility } from ''@kit.AbilityKit''; export default class EntryAbility
    extends UIAbility { // '
  quote_hash: sha256:a249e53ef43ea25144dd679c60e9c9d14aaedd9b30865edb0f8f3f919b6eb4be
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-uiability-context-not-ready

## Failure Class
harmonyos/ability-lifecycle

## Symptoms
- Accessing UIAbilityContext returns null or throws because context is accessed before onCreate initializes it

## Fingerprints
- UIAbilityContext
- Context is null
- context not ready
- getContext
- context 为空

## First Checks
- Check whether context is accessed in a member initializer, constructor, or static field before onCreate
- Check whether getContext() is called on a component that has not yet been attached to an AbilityStage
- Check whether the context is passed through a closure that captures a stale null reference

## Do Not Patch Yet
- Do not cache UIAbilityContext in a module-level variable before onCreate completes
- Do not pass context to child components via property assignment before the context is initialized in onCreate

## Evidence Needed
- Capture the stack trace showing context is null at the call site
- Identify the lifecycle stage when the null context is accessed

## Minimal Fix Scope
- The context access site and the lifecycle callback it is in
- The state initialization order in the UIAbility subclass

## Validation Ladder
- Move context access to onCreate or a later callback and verify no null reference
- Verify child components receive context only after it is initialized
- Run the ability lifecycle test covering context availability

## Regression Guard
- Add an ability test asserting context is non-null from onCreate onwards

## Reviewer Notes
