# 快照人审：arkts-migration-guide

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
- 最终 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/typescript-to-arkts-migration-guide.md
- 来源类型: official_error_doc
- 采集时间: 2026-05-26T12:26:11.870151Z
- HTTP 状态: 200
- 内容哈希: sha256:c8907a4c47694cf35f71fc61f0c763ba60abf547cda015893eb17ea67dbda389
- 技术栈: harmonyos, arkts
- 抽取段落数: 84

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 84
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 7/10 条 expected_failure_hints

## 预期线索命中
- `arkts-no-any`
  - [arkts-migration-guide-13] ### 使用具体的类型而非`any`或`unknown` **规则：**`arkts-no-any-unknown` **级别：错误** **错误码：10605008** ArkTS不支持`any`和`unknown`类型。显式指定具体类型。 **TypeScript** ```typescript let value1: any value1 = true; value1 = 42; let value2: unknown va...
- `arkts-no-var`
  - [arkts-migration-guide-12] ### 使用`let`而非`var` **规则：**`arkts-no-var` **级别：错误** **错误码：10605005** `let`关键字可以在块级作用域中声明变量，帮助程序员避免错误。因此，ArkTS不支持`var`，请使用`let`声明变量。 **TypeScript** ```typescript function f(shouldInitialize: boolean) { if (shouldInitial...
- `arkts-no-untyped-obj-literals`
  - [arkts-migration-guide-27] ### 需要显式标注对象字面量的类型 **规则：**`arkts-no-untyped-obj-literals` **级别：错误** **错误码：10605038** 在 ArkTS 中，需要显式标注对象字面量的类型，否则将导致编译时错误。在某些场景下，编译器可以根据上下文推断出字面量的类型。 在以下上下文中不支持使用字面量初始化类和接口： * 初始化具有`any`、`Object`或`object`类型的任何对象 * 初始化带...
- `arkts-no-struct-initialized`：未找到直接段落命中
- `arkts-no-delete`
  - [arkts-migration-guide-37] ### 不支持`delete`运算符 **规则：**`arkts-no-delete` **级别：错误** **错误码：10605059** 在ArkTS中，对象布局于编译时确定，运行时不可更改，因此删除属性的操作无意义。 **TypeScript** ```typescript class Point { x?: number = 0.0 y?: number = 0.0 } let p = new Point(); delet...
- `arkts-no-in-operator`：未找到直接段落命中
- `arkts-no-instanceof`
  - [arkts-migration-guide-34] ### 类型转换仅支持`as T`语法 **规则：**`arkts-as-casts` **级别：错误** **错误码：10605053** 在ArkTS中，`as`关键字是类型转换的唯一语法，错误的类型转换会导致编译时错误或者运行时抛出`ClassCastException`异常。ArkTS不支持使用`<type>`语法进行类型转换。 需要将`primitive`类型（如`number`或`boolean`）转换为引用类型时，请...
  - [arkts-migration-guide-39] ### 部分支持`instanceof`运算符 **规则：**`arkts-instanceof-ref-types` **级别：错误** **错误码：10605065** TypeScript中，`instanceof`运算符的左操作数类型必须为`any`类型、对象类型或类型参数，否则结果为`false`。ArkTS中，`instanceof`运算符的左操作数类型必须为引用类型（如对象、数组或函数），否则会发生编译时错误。此外，...
  - [arkts-migration-guide-40] ### 不支持`in`运算符 **规则：**`arkts-no-in` **级别：错误** **错误码：10605066** 在ArkTS中，对象布局在编译时已知且运行时无法修改，因此不支持`in`运算符。需要检查类成员是否存在时，使用`instanceof`代替。 **TypeScript** ```typescript class Person { name: string = '' } let p = new Person(...
- `arkts-no-comma-op`
  - [arkts-migration-guide-42] ### 逗号运算符`,`仅用在`for`循环语句中 **规则：**`arkts-no-comma-outside-loops` **级别：错误** **错误码：10605071** 在ArkTS中，逗号运算符仅适用于`for`循环语句，用于明确执行顺序。 >**注意：** 这与声明变量和函数参数传递时使用的逗号分隔符不同。 **TypeScript** ```typescript for (let i = 0, j = 0; i...
- `arkts-no-bitwise`：未找到直接段落命中
- `arkts-no-untyped-destructuring`
  - [arkts-migration-guide-27] ### 需要显式标注对象字面量的类型 **规则：**`arkts-no-untyped-obj-literals` **级别：错误** **错误码：10605038** 在 ArkTS 中，需要显式标注对象字面量的类型，否则将导致编译时错误。在某些场景下，编译器可以根据上下文推断出字面量的类型。 在以下上下文中不支持使用字面量初始化类和接口： * 初始化具有`any`、`Object`或`object`类型的任何对象 * 初始化带...

## 段落样例
- [arkts-migration-guide-1] # 从TypeScript到ArkTS的适配规则 <!--Kit: ArkTS--> <!--Subsystem: ArkCompiler--> <!--Owner: @husenlin--> <!--Designer: @qyhuo32--> <!--Tester: @kirl75; @zsw_zhushiwei--> <!--Adviser: @zhang_yixin13--> ArkTS规范约束了TypeScript（简称T...
- [arkts-migration-guide-2] ## 概述 本节罗列了ArkTS不支持或部分支持的TypeScript特性。完整的列表以及详细的代码示例和重构建议，请参考[约束说明](#约束说明)。更多案例请参考[适配指导案例](arkts-more-cases.md)。
- [arkts-migration-guide-3] ### 强制使用静态类型 静态类型是ArkTS的重要特性之一。当程序使用静态类型时，所有类型在编译时已知，这有助于开发者理解代码中的数据结构。编译器可以提前验证代码的正确性，减少运行时的类型检查，从而提升性能。 基于上述考虑，ArkTS中禁止使用`any`类型。 **示例** ```typescript // 不支持： let res: any = some_api_function('hello', 'world'); // 支...
- [arkts-migration-guide-4] ### 禁止在运行时变更对象布局 为实现最佳性能，ArkTS要求在程序执行期间不能更改对象的布局。换句话说，ArkTS禁止以下行为： - 向对象中添加新的属性或方法。 - 从对象中删除已有的属性或方法。 - 将任意类型的值赋值给对象属性。 TypeScript编译器已经禁止了许多此类操作。然而，有些操作还是有可能绕过编译器的，例如，使用`as any`转换对象的类型，或者在编译TS代码时关闭严格类型检查的配置，或者在代码中通过`@...
- [arkts-migration-guide-5] ### 限制运算符的语义 为获得更好的性能并鼓励开发者编写更清晰的代码，ArkTS限制了一些运算符的语义。详细的语义限制，请参考[约束说明](#约束说明)。 **示例** ```typescript // 一元运算符`+`只能作用于数值类型： let t = +42; // 合法运算 let s = +'42'; // 编译时错误 ``` 使用额外的语义重载语言运算符会增加语言规范的复杂度，而且，开发者还被迫牢记所有可能的例外情况...
- [arkts-migration-guide-6] ### 不支持 structural typing 假设两个不相关的类`T`和`U`都拥有相同的`public`API： ```typescript class T { public name: string = '' public greet(): void { console.info('Hello, ' + this.name); } } class U { public name: string = '' public g...
- [arkts-migration-guide-8] ### 对象的属性名必须是合法的标识符 **规则：**`arkts-identifiers-as-prop-names` **级别：错误** **错误码：10605001** 在ArkTS中，对象的属性名不能为数字或字符串。例外：ArkTS支持属性名为字符串字面量和枚举中的字符串值。通过属性名访问类的属性，通过数值索引访问数组元素。 **TypeScript** ```typescript var x = { 'name': 'x...
- [arkts-migration-guide-9] ### 不支持`Symbol()`API **规则：**`arkts-no-symbol` **级别：错误** **错误码：10605002** 在ArkTS中，对象布局在编译时确定，不可在运行时更改，因此不支持`Symbol()` API。该API在静态类型语言中通常没有实际意义。 ArkTS只支持`Symbol.iterator`。

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
