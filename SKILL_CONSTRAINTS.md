# Interactive Mindmap Editor Skill Constraints

本文件是 `interactive-mindmap-editor` 的执行约束和验收清单。Skill 在创建、修改、导入、导出或修复思维导图前后，都应以本文件为准，并以仓库中实际存在的脚本和 HTML 行为为最终依据。

## 1. 能力清单

### 1.1 已实现能力

- 文本或 Markdown 提纲转换为思维导图 JSON。
- 思维导图 JSON 转换为普通 Markdown 提纲。
- 文本或 JSON 导出为现代 XMind `.xmind` 文件。
- 现代 XMind `content.json` 导入；必要时兼容基础 `content.xml`。
- 生成或修复独立 HTML 思维导图。
- HTML 双击编辑标题和副标题，标题编辑器最多保留两行。
- 右键编辑、增加子节点、批注和删除节点。
- 节点折叠/展开，折叠触发区域限制在右侧箭头或手柄。
- 多级节点新增、编辑、删除和递归添加子节点。
- 节点文本按字符宽度换行，编辑节点不能遮挡其他节点。
- 右键拖动画布；左键用于选择、编辑和节点拖拽，不负责整页平移。
- 节点拖拽、同级排序、重新挂接、根目录挂接和自由标题。
- 折叠状态、编号状态和必要的视图状态持久化。
- 全部自动编号、重编全部编号、取消全部编号，保留在右键菜单。
- HTML 全屏展示和全屏退出；全屏时顶部悬停显示退出按钮。
- 导入/导出 JSON、普通 Markdown 和 XMind 的统一下载流程。
- Markmap 预览作为 HTML 中的预览层，必须有失败回退，不得影响普通编辑模式。
- 使用插件模板生成独立离线 Markmap HTML。
- Markmap Markdown 与思维导图 JSON 双向脚本转换。

### 1.2 当前已提供的 Markmap 文件

以下文件构成可复用的 Markmap 实现：

```text
skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py
skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py
skills/interactive-mindmap-editor/scripts/render_markmap_html.py
runtime/markmap-preview.js
runtime/markmap-preview.css
runtime/markmap-assets.js
templates/interactive-mindmap.html
```

普通 Markdown 转换脚本仍然可用：

```text
skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py
skills/interactive-mindmap-editor/scripts/mindmap_data_to_markdown.py
```

HTML 内嵌 Markmap 预览、普通 Markdown 转换和独立 Markmap 转换脚本是三个不同能力，不能互相替代。

### 1.3 计划能力的标记规则

- 文档中写“已实现”前，必须能在仓库或生成的 HTML 中找到对应实现。
- 依赖资产、模板和运行时必须一起发布；不能只添加一个转换脚本而遗漏浏览器渲染能力。
- 不能把 Markmap 预览等同于 Markmap Markdown 导入/导出脚本。
- 用户要求未实现能力时，先说明缺口，再提出实现方案或补齐实现，不得静默模拟成功。

## 2. 数据模型约束

节点至少应保持以下字段语义：

```js
{
  id, title, sub, type, color, children, collapsed
}
```

可选扩展字段包括 `note`、`free`、`freePosition`、`freeNodes` 和编号状态。修改数据时必须：

- 保证所有节点 `id` 唯一。
- 保留已有标题、副标题、批注和子节点。
- 不把自由标题错误地塞回普通树，除非用户明确要求。
- 不创建循环父子关系。
- 修改结构后同步连接线、折叠状态、编号和持久化数据。

## 3. 交互约束

- 标题区域点击、双击不能创建新行或触发展开/折叠。
- 标题和副标题都进入同一个两行编辑器。
- 重复双击编辑中的节点时复用现有编辑器，不重复插入输入框。
- 右键只打开上下文菜单，不触发折叠或画布平移。
- 折叠/展开只由右侧箭头或手柄触发。
- 新增子节点只展开接收节点，不展开无关分支。
- 每个非根节点都可以继续新增子节点。
- 普通拖拽松开后才提交层级变更；拖拽过程中只显示预览。
- 远离父节点时显示自由标题预览和虚线关系，不提前修改数据。
- 靠近合法目标时显示吸附预览，松开后才正式挂接。
- 拖到根目录时必须成为根的直接子节点，并按释放位置排序。
- 编辑、添加、删除、拖拽和折叠后不得自动居中；只做必要的局部布局调整。
- 全屏、Markmap 预览、普通编辑三种状态切换后，数据和视图状态不能丢失。

## 4. HTML 生成约束

每个生成或修改的 HTML 至少应检查：

- 节点 DOM、SVG 连接线和数据树来自同一份数据。
- 标题最多约 30 个字符宽度后换行，不使用截断总长度代替换行。
- 编辑节点有更高层级，输入框和副标题不会互相遮挡。
- 工具按钮在窄窗口、全屏和 Markmap 预览中不重叠。
- 次要工具可收纳到菜单，但编号功能保留在右键菜单。
- 全屏按钮采用进入/退出同一按钮，状态随 `fullscreenchange` 更新。
- 关闭或重建 Markmap 时清理计时器、观察器、过渡动画和旧实例。
- 创建 Markmap 前检查 SVG 宽高为有限数字，避免 `translate(NaN,NaN)`。
- Markmap 渲染失败时显示可用的本地树形回退，不阻塞普通模式。
- 文件导出遵循当前下载目录策略，并在下一次导出时默认回到上次位置。

## 5. 性能与稳定性清单

性能目标是“编辑响应稳定、布局范围可控”，不是盲目追求动画速度。

- 普通标题编辑时输入响应应保持即时，不因每次输入触发全量重复初始化。
- 布局流程应尽量采用 `measure -> layout -> assign -> renderEdges`，避免重复测量。
- 不在每次编辑、拖拽、折叠或窗口变化后无条件 `fitView()`。
- 拖拽和指针移动中的布局更新应使用节流或 `requestAnimationFrame`。
- 事件监听器、ResizeObserver、定时器和 Markmap 实例必须在销毁时清理。
- 节点更新不能产生重复 DOM、重复输入框或重复 SVG 连接线。
- JSON/Markdown/XMind 导入失败时不得清空现有数据，应保留原页面并显示错误。
- 大树渲染时避免对每个节点重复执行全树递归；能局部更新时优先局部更新。
- 所有坐标、宽高、缩放值和 SVG transform 写入前必须经过有限数字校验。
- 本地 `file://` 打开时不能依赖必须通过跨源请求加载的资源；外部库必须内嵌或提供回退。
- Edge 和 Chrome 至少各验证一次 Markmap 进入、折叠、关闭和再次打开流程。

## 6. 执行前检查清单

- [ ] 明确用户要求的是创建、修改、转换、预览还是修复。
- [ ] 检查目标 HTML、数据模型和现有交互，不凭文档假设实现存在。
- [ ] 检查需要调用的脚本文件确实存在。
- [ ] 记录当前输出文件、版本和 Git 工作区状态。
- [ ] 明确是否允许修改源插件、生成 HTML、提交或推送。
- [ ] 对涉及 Markmap 的请求先确认是预览，还是独立 Markdown 转换。

## 7. 执行后验收清单

- [ ] 修改后的脚本路径与文档命令一致。
- [ ] Python 脚本至少通过 `python -m py_compile` 或等价语法检查。
- [ ] HTML JavaScript 通过语法检查，且未产生重复事件绑定。
- [ ] 生成数据可以被 HTML 加载，节点 id 没有重复。
- [ ] 标题/副标题编辑、换行、折叠、右键菜单和递归新增均可操作。
- [ ] 拖拽到同级、根目录、其他节点和自由区域的结果符合预期。
- [ ] 编号开启时，新增、删除、排序、改父节点和导入后编号正确。
- [ ] 全屏进入、顶部退出、Esc 退出和再次打开状态正确。
- [ ] Markmap 预览失败时仍能使用回退视图，控制台无 `NaN` 坐标错误。
- [ ] JSON、Markdown、XMind 导出流程能完成下载或明确报告浏览器限制。
- [ ] Chrome 和 Edge 的本地 HTML 打开效果均已检查，或明确记录未验证项。
- [ ] 只把实际完成的能力写入 CHANGELOG；未实现项继续标记为缺失。

## 8. 交付报告最低内容

完成任务时应报告：

- 实际修改的文件。
- 已实现、未实现和未验证的能力。
- 执行过的检查命令及结果。
- 是否修改了生成的 HTML。
- 是否创建 commit 或推送远程仓库。
