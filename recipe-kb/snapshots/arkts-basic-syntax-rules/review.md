# 快照人审：arkts-basic-syntax-rules

## 快照质量检查
- 来源 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/introduction-to-arkts.md
- 最终 URL: https://raw.githubusercontent.com/openharmony/docs/master/zh-cn/application-dev/quick-start/introduction-to-arkts.md
- 来源类型: language_doc
- 采集时间: 2026-05-26T12:26:11.870151Z
- HTTP 状态: 200
- 内容哈希: sha256:3ceb35802af8f03c66d625c7f4c83189febc996d75cf099820ccc2229167353f
- 技术栈: harmonyos, arkts
- 抽取段落数: 44

## QA 闸门
- 状态: 通过
- sections_non_empty: 通过；抽取段落数: 44
- section_count_within_bounds: 通过；期望范围: 1-500
- expected_hints_matched: 通过；命中 1/10 条 expected_failure_hints

## 预期线索命中
- `arkts-no-any`：未找到直接段落命中
- `arkts-no-untyped-obj-literals`：未找到直接段落命中
- `arkts-no-prop-reassignment`：未找到直接段落命中
- `arkts-no-delete`：未找到直接段落命中
- `arkts-no-proto`：未找到直接段落命中
- `arkts-no-attrs-functions`：未找到直接段落命中
- `arkts-no-multi-declare`：未找到直接段落命中
- `arkts-no-try-catch-with-types`：未找到直接段落命中
- `arkts-no-comma-op`：未找到直接段落命中
- `arkts-no-function-constructors`
  - [arkts-basic-syntax-rules-38] ### 导入 **静态导入** 导入声明用于导入从其他模块导出的实体，并在当前模块中提供其绑定。导入声明由两部分组成： * 导入路径，用于指定导入的模块； * 导入绑定，用于定义导入的模块中的可用实体集和使用形式（限定或不限定使用）。 导入绑定可以有几种形式。 假设模块的路径为“./utils”，并且导出了实体“X”和“Y”。 导入绑定`* as A`表示绑定名称“A”，通过`A.name`可访问从导入路径指定的模块导出的所有实体...

## 段落样例
- [arkts-basic-syntax-rules-1] # ArkTS语言介绍 <!--Kit: ArkTS--> <!--Subsystem: ArkCompiler--> <!--Owner: @LeechyLiang--> <!--Designer: @qyhuo32--> <!--Tester: @kirl75; @zsw_zhushiwei--> <!--Adviser: @zhang_yixin13--> ArkTS是一种设计用于构建高性能应用的编程语言。它在继承TypeS...
- [arkts-basic-syntax-rules-2] ### 声明 ArkTS通过声明引入变量、常量、类型和函数。 **变量声明** 使用关键字`let`声明的变量可以在程序执行期间具有不同的值。 ```typescript let hi: string = 'hello'; hi = 'hello, world'; ``` **常量声明** 使用关键字`const`声明的常量为只读类型，只能被赋值一次。 ```typescript const hello: string = 'he...
- [arkts-basic-syntax-rules-3] ### 类型 **基本类型和引用类型** 基本数据类型包括`number`、`string`等简单类型，它们可以准确地表示单一的数据类型。对基本类型的存储和访问都是直接的，比较时直接比较其值。 引用类型包括对象、数组和函数等复杂数据结构。这些类型通过引用访问数据，对象和数组可以包含多个值或键值对，函数则可以封装可执行的代码逻辑。引用类型在内存中通过指针访问数据，修改引用会影响原始数据。 **`number`类型** ArkTS提供...
- [arkts-basic-syntax-rules-4] ### 运算符 **赋值运算符** 赋值运算符`=`，使用方式如`x=y`。 复合赋值运算符将赋值与运算符组合在一起，例如：`a += b` 等价于 `a = a + b`， 其中的 `+=` 即为复合赋值运算符 复合赋值运算符包括：`+=`、`-=`、`*=`、`/=`、`%=`、`<<=`、`>>=`、`>>>=`、`&=`、`|=`、`^=`。 **比较运算符** | 运算符| 说明 | | -------- | -----...
- [arkts-basic-syntax-rules-5] ### 语句 **`If`语句** `if`语句用于需要根据逻辑条件执行不同语句的场景。当逻辑条件为真时，执行对应的一组语句，否则执行另一组语句（如果有的话）。 `else`部分也可以包含`if`语句。 `if`语句如下所示： ```typescript if (condition1) { // 语句1 } else if (condition2) { // 语句2 } else { // else语句 } ``` 条件表达式可以...
- [arkts-basic-syntax-rules-6] ### 函数声明 函数声明引入一个函数，包含其名称、参数列表、返回类型和函数体。 以下示例是一个简单的函数和它的语法语义说明： 1.参数类型标注：x: string, y: string 显式声明参数类型为字符串类型。 2.返回值类型：: string 指定函数返回值为字符串类型。 ```typescript function add(x: string, y: string): string { let z: string =...
- [arkts-basic-syntax-rules-7] ### 可选参数 可选参数的格式可为`name?: Type`。 ```typescript function hello(name?: string) { if (name == undefined) { console.info('Hello!'); } else { console.info(`Hello, ${name}!`); } } ``` 可选参数的另一种形式为设置的参数默认值。如果在函数调用中这个参数被省略了，则会...
- [arkts-basic-syntax-rules-8] ### Rest参数 函数的最后一个参数可以是rest参数，格式为`...restArgs`。rest参数允许函数接收一个由剩余实参组成的数组，类型为任意指定类型，用于处理不定数量的参数输入。 ```typescript function sum(...numbers: number[]): number { let res = 0; for (let n of numbers) res += n; return res; } s...

## 审阅决策
- [ ] 批准用于 recipe 生成
- [ ] 需要改进抽取过滤
- [ ] 拒绝该 source

## 审阅备注
-
