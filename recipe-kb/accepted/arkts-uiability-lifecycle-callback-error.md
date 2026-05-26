---
id: arkts-uiability-lifecycle-callback-error
kind: debug-recipe
status: accepted
stack:
- harmonyos
- arkts
failure_class: harmonyos/ability-lifecycle
symptoms:
- UIAbility lifecycle callback invoked at unexpected time — onCreate, onWindowStageCreate,
  onForeground, onBackground, onDestroy sequence is violated
fingerprints:
- UIAbility lifecycle
- onCreate
- onWindowStageCreate
- onForeground
- onBackground
- onDestroy
- lifecycle callback sequence
first_checks:
- Check whether window operation code is placed in onWindowStageCreate (not onCreate),
  where WindowStage is not yet available
- Check whether global data initialization is placed in onCreate and per-window UI
  logic in onWindowStageCreate
- Check whether background-to-foreground transition logic is correctly placed in onForeground,
  not in onWindowStageCreate
do_not:
- Do not access WindowStage in onCreate; it is only available in onWindowStageCreate
- Do not perform long-running synchronous work in onWindowStageCreate; use async operations
  and await windowStage.loadContent
evidence_needed:
- Capture the lifecycle log sequence showing which callback fired and in what order
- Identify the code that depends on WindowStage or context availability
minimal_fix_scope:
- The lifecycle callback method where the misordered operation is placed
- The operation that depends on WindowStage or context readiness
validation_ladder:
- Move the operation to the correct lifecycle callback and verify no exception or
  null context
- 'Verify the lifecycle log sequence matches: onCreate → onWindowStageCreate → onForeground
  → onBackground → onDestroy'
- Run the ability integration test covering the lifecycle transition
regression_guard:
- Add an ability lifecycle test asserting callback order and WindowStage availability
evidence_refs:
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-1
  short_excerpt: '# UIAbility组件生命周期 <!--Kit: Ability Kit--> <!--Subsystem: Ability-->
    <!--Owner: @wendel; @Luobniz21--> <!--Designer: @wendel--> <!--Tester: @lixueqing513-->
    <!--Adviser: @huipeizi-->'
  quote_hash: sha256:89cf45143f71e4227784508c5f321a66f5bb86850c2438d47b44ea1ec1f988d7
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
  span_id: openharmony-stage-model-lifecycle-5
  short_excerpt: '### onWindowStageCreate() [UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)实例创建完成之后，在进入前台之前，系统会创建一个[WindowStage](../../application-dev/windowmanager/application-window-stage.md)。WindowStage创建完成后会进入[onWindowStageCreate()](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onwindowstagecreate)回调，开发者可以在该回调中进行UI加载、WindowStage的事件订阅。
    在onWindowStageCreate()回调中通过[loadContent()](../reference/apis-arkui/arkts-apis-window-Window.md#loadcontent9)方法设置应用要加载的页面，并根据需要调用[on(''windowStageEvent'')](../reference/apis-arkui/arkts-apis-window-WindowStage.md#onwindowstageevent9)方法'
  quote_hash: sha256:91c36d9b8c2c08134a6cf0520dae9bffaa19afab58c80c85a660ffc25509492c
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-6
  short_excerpt: '### onForeground() 在[UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)切换至前台时且UIAbility的UI可见之前，系统触发[onForeground](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onforeground)回调。开发者可以在该回调中申请系统需要的资源，或者重新申请在`onBackground()`中释放的资源。系统回调该方法后，UIAbility实例进入前台状态，即UIAbility实例可以与用户交互的状态。UIAbility实例会一直处于这个状态，直到被某些动作打断（例如屏幕关闭、用户跳转到其他UIAbility）。
    例如，应用已获得地理位置权限。在UI显示之前，开发者可以在`onForeground()`回调中开启定位功能，从而获取到当前的位置信息。 ```ts import
    { UIAbility } from ''@kit.AbilityKit''; export default class EntryAbility extends
    UIAbility { // ... onForeground(): void { // 申请系统需要的资源，或者重新申请在on'
  quote_hash: sha256:d4387485d9a0d0cf4d4c4ce95b1672e00802b04d7cb6920b97e9cc5fe4120dd9
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-7
  short_excerpt: '### onBackground() 在[UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)的UI完全不可见之后，系统触发[onBackground](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onbackground)回调，将UIAbility实例切换至后台状态。开发者可以在该回调中释放UI不可见时的无用资源，例如停止定位功能，以节省系统的资源消耗。
    `onBackground()`执行时间较短，无法提供足够的时间做一些耗时动作。请勿在该方法中执行保存用户数据或执行数据库事务等耗时操作。 ```ts import
    { UIAbility } from ''@kit.AbilityKit''; export default class EntryAbility extends
    UIAbility { // ... onBackground(): void { // 释放UI不可见时无用的资源 } // ... } ```'
  quote_hash: sha256:420d51eba6812acc53b2aabc17482899893420568356b74949e757411e152b41
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-8
  short_excerpt: '### onWindowStageWillDestroy() 在[UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)实例销毁之前，系统触发[onWindowStageWillDestroy()](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onwindowstagewilldestroy12)回调。该回调在WindowStage销毁前执行，此时WindowStage可以使用。开发者可以在该回调中释放通过WindowStage获取的资源、注销WindowStage事件订阅等。
    ```ts import { UIAbility } from ''@kit.AbilityKit''; import { window } from ''@kit.ArkUI'';
    import { BusinessError } from ''@kit.BasicServicesKit''; import { hilog } from
    ''@kit.PerformanceAnalysisKit''; const DOMAIN_NUMBER: number = 0xFF00; export
    default class EntryAbility ex'
  quote_hash: sha256:f32e35c6db868abab2c635f4f993c881aaf4fd068ee2e29cbd498c1c8e3fb101
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-9
  short_excerpt: '### onWindowStageDestroy() 在[UIAbility](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md)实例销毁之前，系统触发[onWindowStageDestroy()](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onwindowstagedestroy)回调，开发者可以在该回调中释放UI资源。该回调在WindowStage销毁后执行，此时WindowStage不可以使用。
    ```ts import { UIAbility } from ''@kit.AbilityKit''; import { window } from ''@kit.ArkUI'';
    export default class EntryAbility extends UIAbility { // ... onWindowStageCreate(windowStage:
    window.WindowStage): void { // 加载UI资源 } onWindowStageDestroy() { // 释放UI资源 } }
    ```'
  quote_hash: sha256:25c47a1fb9cc843a86aac1814287c8665056438ba945cff42840dd454ab82f04
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
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-11
  short_excerpt: '### onNewWant() 当应用的UIAbility实例已创建，再次调用方法启动该UIAbility实例时，系统触发该UIAbility的[onNewWant()](../reference/apis-ability-kit/js-apis-app-ability-uiAbility.md#onnewwant)回调。开发者可以在该回调中更新要加载的资源和数据等，用于后续的UI展示。
    ```ts import { AbilityConstant, UIAbility, Want } from ''@kit.AbilityKit''; export
    default class EntryAbility extends UIAbility { // ... onNewWant(want: Want, launchParam:
    AbilityConstant.LaunchParam) { // 更新资源、数据 } } ```'
  quote_hash: sha256:489449a31a31138f554923a7d4db5c5d282d03181834007e183053c05e97dbaa
- source_id: openharmony-stage-model-lifecycle
  url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  final_url: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/application-models/uiability-lifecycle.md
  source_type: official_doc
  captured_at: '2026-05-26T12:26:11.870151Z'
  section_anchor: root
  span_id: openharmony-stage-model-lifecycle-12
  short_excerpt: '## 相关实例 针对UIAbility生命周期，有以下相关实例可供参考： - [UIAbility和自定义组件生命周期（ArkTS）（API9）](https://gitcode.com/openharmony/codelabs/blob/master/Ability/UIAbilityLifeCycle/README.md)'
  quote_hash: sha256:ef4b03ed4d9c790843e8f96db6bc5808b77d554dbdfbd331a6e630748280e46e
review: []
maintenance:
  state: accepted
  stale_reason: []
  stale_detected_at: null
---

<!-- generated-from-frontmatter: do not edit semantic sections -->

# arkts-uiability-lifecycle-callback-error

## Failure Class
harmonyos/ability-lifecycle

## Symptoms
- UIAbility lifecycle callback invoked at unexpected time — onCreate, onWindowStageCreate, onForeground, onBackground, onDestroy sequence is violated

## Fingerprints
- UIAbility lifecycle
- onCreate
- onWindowStageCreate
- onForeground
- onBackground
- onDestroy
- lifecycle callback sequence

## First Checks
- Check whether window operation code is placed in onWindowStageCreate (not onCreate), where WindowStage is not yet available
- Check whether global data initialization is placed in onCreate and per-window UI logic in onWindowStageCreate
- Check whether background-to-foreground transition logic is correctly placed in onForeground, not in onWindowStageCreate

## Do Not Patch Yet
- Do not access WindowStage in onCreate; it is only available in onWindowStageCreate
- Do not perform long-running synchronous work in onWindowStageCreate; use async operations and await windowStage.loadContent

## Evidence Needed
- Capture the lifecycle log sequence showing which callback fired and in what order
- Identify the code that depends on WindowStage or context availability

## Minimal Fix Scope
- The lifecycle callback method where the misordered operation is placed
- The operation that depends on WindowStage or context readiness

## Validation Ladder
- Move the operation to the correct lifecycle callback and verify no exception or null context
- Verify the lifecycle log sequence matches: onCreate → onWindowStageCreate → onForeground → onBackground → onDestroy
- Run the ability integration test covering the lifecycle transition

## Regression Guard
- Add an ability lifecycle test asserting callback order and WindowStage availability

## Reviewer Notes
