from dataclasses import dataclass, field

from recipe_importer.models import DecisionOption, TriggerSpec


@dataclass(frozen=True)
class BuildRecipeTemplate:
    source_id: str
    build_label: str
    recipe_id: str
    stack: list[str]
    trigger: TriggerSpec
    correct_pattern: list[str]
    decision_context: list[DecisionOption]
    constraints: list[str]
    do_not: list[str]
    defaults: list[str]
    validation: list[str]
    related_debug_recipes: list[str]
    match_terms: list[str] = field(default_factory=list)


BUILD_RECIPE_TEMPLATES: tuple[BuildRecipeTemplate, ...] = (
    BuildRecipeTemplate(
        source_id="nextjs-rendering-server-components",
        build_label="nextjs server client boundary",
        recipe_id="build-nextjs-server-client-boundary",
        stack=["react", "nextjs"],
        trigger=TriggerSpec(
            file_pattern="app/**/*.{ts,tsx}",
            code_signals=["useState", "useEffect", "useReducer", "useContext"],
            description="在 Next.js App Router 的 Server Component 中使用了 React hooks",
        ),
        correct_pattern=[
            "需要 client interactivity 的组件必须在文件顶部声明 'use client'",
            "Server Component 只能使用 async/await、server actions、fetch 等服务端 API",
            "将 Client Component 放在组件树的叶子节点，最小化客户端 bundle",
            "数据获取优先在 Server Component 中完成，通过 props 传递给 Client Component",
        ],
        decision_context=[
            DecisionOption(
                condition="组件需要 useState / useEffect 等 hooks",
                recommendation="标记为 Client Component ('use client')",
            ),
            DecisionOption(
                condition="组件只需要一次性数据获取",
                recommendation="保持 Server Component，使用 async function + fetch",
            ),
            DecisionOption(
                condition="组件需要事件处理（onClick, onChange）",
                recommendation="标记为 Client Component",
            ),
            DecisionOption(
                condition="组件只做静态渲染，无交互",
                recommendation="保持 Server Component（默认）",
            ),
        ],
        constraints=[
            "Server Component 不能使用 React hooks (useState, useEffect, useReducer, useContext)",
            "Server Component 不能使用 browser-only API (window, document, localStorage)",
            "Server Component 不能使用事件处理器 (onClick, onChange, onSubmit)",
            "'use client' 声明必须在文件顶部，在所有 import 之前",
        ],
        do_not=[
            "不要在未标记 'use client' 的 app/ 组件中使用 React hooks",
            "不要把整个页面标记为 'use client' 只为了一个小交互——拆分出 Client Component",
            "不要在 Server Component 中 import 使用了 hooks 的库而不标记 'use client'",
        ],
        defaults=[
            "app/ 下的组件默认是 Server Component",
            "只在需要 client interactivity 的最小子树标记 'use client'",
        ],
        validation=[
            "next build 成功，无 server component hooks error",
            "next dev 无 'useState is not a function' 或类似 warning",
            "检查 bundle analyzer 确认 Client Component 没有包含不必要的服务端代码",
        ],
        related_debug_recipes=["react-invalid-hook-call"],
        match_terms=[
            "Server Components",
            "Client Components",
            "use client",
            "useState",
            "useEffect",
            "interactivity",
            "server-side rendering",
        ],
    ),
)


BUILD_TEMPLATES_BY_SOURCE: dict[str, BuildRecipeTemplate] = {
    template.source_id: template for template in BUILD_RECIPE_TEMPLATES
}

BUILD_TEMPLATES_BY_LABEL: dict[str, BuildRecipeTemplate] = {
    template.build_label: template for template in BUILD_RECIPE_TEMPLATES
}
