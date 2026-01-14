# 上下文基础 - 中级场景层

## 在01_basic基础上扩展

**已掌握**：常见场景下的上下文应用模式

**本层目标**：处理复杂任务中的上下文管理和优化

---

## 复杂场景处理

### 场景1：多轮对话上下文管理

**挑战**：长对话导致上下文爆炸、遗忘

**问题模式**：
```
第1轮：讨论需求（5K tokens）
第2轮：设计方案（添加8K tokens）
第3轮：实现代码（添加15K tokens）
第4轮：调试问题（添加10K tokens）
总计：38K tokens ⚠️ 接近限制，AI开始遗忘早期内容
```

**解决方案：智能上下文压缩**

**策略1：摘要压缩**
```python
# 每10轮对话
if token_count > 20000:
    # 提取关键决策和结论
    summary = extract_key_decisions(conversation_history)

    # 创建压缩版本
    compressed_context = {
        "original_request": original_request,
        "key_decisions": summary.decisions,
        "current_state": current_state,
        "recent_messages": last_5_messages
    }

    # 替换旧上下文
    conversation_history = compressed_context
```

**策略2：分层存储**
```yaml
short_term_memory:
  scope: 最近5轮对话
  purpose: 保持对话连续性

medium_term_memory:
  scope: 关键决策和结论
  purpose: 避免重复讨论

long_term_memory:
  scope: 项目文档、代码库
  purpose: 持久化知识
```

**策略3：主动清理**
```python
# 检测可以安全丢弃的内容
cleanup_candidates = [
    "已解决的临时错误信息",
    "探索性讨论的失败分支",
    "过期的中间结果",
    "已被替代的方案"
]
```

**实践案例**：

**场景**：重构一个大型模块（50个文件）

**第1阶段：理解现状**
```
上下文：模块概述、架构图、关键接口
大小：3K tokens
```

**第2阶段：设计方案**
```
上下文：设计文档、接口变更、风险评估
大小：5K tokens
```

**第3阶段：分批实施**
```
Batch 1: 重构核心类（10个文件）
上下文：核心类代码、测试用例
大小：8K tokens

保存进展：已完成文件清单、设计决策记录

Batch 2: 重构辅助类（10个文件）
上下文：辅助类代码、已完成清单
大小：6K tokens

...（重复5批）
```

**结果**：
- 每批保持在10K tokens以内
- 进展可追踪
- 避免上下文爆炸

### 场景2：多文件项目分析

**挑战**：大型项目包含数百个文件，无法一次性加载

**解决方案：分层分析策略**

**Layer 1：项目概览**
```yaml
context:
  - README.md（项目介绍）
  - package.json（依赖关系）
  - 目录结构（文件组织）
token_count: ~2K
action: 理解项目架构和关键组件
```

**Layer 2：模块分析**
```yaml
context:
  - 模块README
  - 主要接口定义
  - 关键类列表
token_count: ~3K per module
action: 深入理解每个模块
```

**Layer 3：代码级分析**
```yaml
context:
  - 具体文件代码
  - 相关测试
  - 文档注释
token_count: ~5K per file
action: 详细分析实现细节
```

**智能选择算法**：
```python
def select_files_for_context(task, project_structure):
    # Step 1: 根据任务类型识别相关模块
    relevant_modules = identify_modules(task, project_structure)

    # Step 2: 在每个模块中识别关键文件
    critical_files = []
    for module in relevant_modules:
        scores = score_file_relevance(task, module.files)
        critical_files.extend(top_k(scores, k=5))

    # Step 3: 估算token数量
    estimated_tokens = estimate_tokens(critical_files)

    # Step 4: 如果超限，进一步过滤
    if estimated_tokens > MAX_TOKENS:
        critical_files = filter_by_priority(critical_files, task)

    return critical_files
```

**实践案例**：

**任务**：在Node.js项目中添加新的API端点

**分析**：
1. 项目结构显示：`routes/`目录包含所有路由
2. 任务相关：需要添加`routes/users.js`
3. 依赖分析：需要`controllers/userController.js`、`models/User.js`
4. 最终选择：
   ```yaml
   selected_files:
     - routes/index.js（理解路由注册）
     - routes/users.js（类似实现作为参考）
     - controllers/userController.js（业务逻辑）
     - models/User.js（数据模型）
   token_count: ~4K
   ```

### 场景3：跨会话上下文传递

**挑战**：需要在新会话中恢复之前的工作状态

**解决方案：会话状态快照**

**快照内容**：
```yaml
session_snapshot:
  metadata:
    session_id: "session-2024-001"
    timestamp: "2024-12-26T10:30:00Z"
    task: "实现用户认证功能"

  context_summary:
    current_state: "已完成注册接口，正在实现登录"
    progress: 60%
    completed_steps:
      - "设计User模型"
      - "实现注册接口"
      - "编写单元测试"
    pending_steps:
      - "实现登录接口"
      - "添加JWT中间件"
      - "集成测试"

  key_decisions:
    - "使用bcrypt进行密码哈希"
    - "JWT有效期设为7天"
    - "使用Passport.js进行认证"

  file_states:
    important_files:
      - path: "models/User.js"
        status: "已完成"
        notes: "包含验证逻辑"

      - path: "routes/auth.js"
        status: "进行中"
        notes: "注册已完成，登录待实现"

  references:
    documentation: ["API设计文档"]
    examples: ["类似的认证实现"]
    issues: ["相关问题链接"]
```

**快照使用**：
```python
# 在新会话中恢复
def restore_session(snapshot_path):
    snapshot = load_snapshot(snapshot_path)

    # 恢复上下文
    context = build_context_from_snapshot(snapshot)

    # 提示用户
    print(f"恢复会话：{snapshot.metadata.task}")
    print(f"当前进度：{snapshot.context_summary.progress}%")
    print(f"下一步：{snapshot.context_summary.pending_steps[0]}")

    return context
```

### 场景4：动态上下文组装

**挑战**：任务类型多样，需要灵活的上下文策略

**解决方案：基于任务类型的上下文模板**

**模板库**：

**模板1：Bug修复模板**
```yaml
bug_fix_template:
  required_sections:
    - 错误描述和复现步骤
    - 完整堆栈跟踪
    - 相关代码（调用链）
    - 最近改动（git diff）
    - 环境信息

  optional_sections:
    - 类似历史问题
    - 相关测试用例
    - 性能profiling数据

  token_budget: 10000
  priority: "堆栈跟踪 > 相关代码 > 最近改动"
```

**模板2：性能优化模板**
```yaml
performance_template:
  required_sections:
    - 性能目标和基准
    - profiling数据
    - 瓶颈识别
    - 优化方案对比

  optional_sections:
    - 系统架构图
    - 数据流分析
    - 资源使用情况

  token_budget: 15000
  priority: "profiling数据 > 瓶颈分析 > 优化方案"
```

**模板3：新功能开发模板**
```yaml
feature_development_template:
  required_sections:
    - 需求描述和用户故事
    - 验收标准
    - 技术规范
    - 设计文档

  optional_sections:
    - 参考实现
    - 相关依赖
    - 集成测试计划

  token_budget: 20000
  priority: "需求 > 验收标准 > 技术规范"
```

**动态组装逻辑**：
```python
def assemble_context(task, template):
    context = {
        "task": task,
        "sections": []
    }

    # 添加必需章节
    for section in template.required_sections:
        content = retrieve_content(task, section)
        context["sections"].append({
            "name": section,
            "content": content,
            "priority": "high"
        })

    # 计算剩余token预算
    used_tokens = calculate_tokens(context)
    remaining_budget = template.token_budget - used_tokens

    # 添加可选章节（按优先级）
    for section in template.optional_sections:
        if remaining_budget <= 0:
            break
        content = retrieve_content(task, section)
        estimated = estimate_tokens(content)
        if estimated <= remaining_budget:
            context["sections"].append({
                "name": section,
                "content": content,
                "priority": "medium"
            })
            remaining_budget -= estimated

    return context
```

---

## 高级优化技术

### 技术1：上下文相关性评分

**目标**：量化每个信息片段的相关性

**评分因素**：
```python
def relevance_score(item, task):
    score = 0.0

    # 因素1：关键词重叠
    score += 0.3 * keyword_overlap(item, task)

    # 因素2：语义相似度
    score += 0.3 * semantic_similarity(item, task)

    # 因素3：引用关系
    score += 0.2 * has_reference_link(item, task)

    # 因素4：时间新鲜度
    score += 0.1 * temporal_relevance(item, task)

    # 因素5：用户明确标记
    score += 0.1 * user_explicit_relevance(item, task)

    return score
```

**应用**：
```python
# 过滤低相关性内容
filtered_items = [
    item for item in all_items
    if relevance_score(item, task) > 0.5
]

# 按相关性排序
sorted_items = sorted(
    filtered_items,
    key=lambda x: relevance_score(x, task),
    reverse=True
)
```

### 技术2：上下文缓存策略

**目标**：避免重复加载相同信息

**缓存层次**：
```yaml
L1_cache:
  scope: 单次会话
  duration: 会话生命周期
  content: 频繁访问的文档、代码

L2_cache:
  scope: 跨会话
  duration: 项目生命周期
  content: 项目结构、API文档

L3_cache:
  scope: 全局
  duration: 永久
  content: 通用知识、最佳实践
```

**缓存失效**：
```python
def should_invalidate_cache(cache_entry, current_state):
    # 文件被修改
    if cache_entry.file_modified_time != current_state.file_modified_time:
        return True

    # 依赖关系变化
    if cache_entry.dependencies != current_state.dependencies:
        return True

    # 时间过期
    if cache_entry.age > MAX_CACHE_AGE:
        return True

    # 用户主动刷新
    if user_requested_refresh:
        return True

    return False
```

### 技术3：上下文版本控制

**目标**：追踪上下文演进，支持回滚

**版本记录**：
```yaml
context_version:
  version_id: "v1.2.0"
  timestamp: "2024-12-26T10:30:00Z"
  changes:
    - type: "add"
      item: "新增API文档"
      reason: "任务需要API参考"

    - type: "remove"
      item: "移除过期配置"
      reason: "配置已废弃"

    - type: "update"
      item: "更新代码示例"
      reason: "代码已重构"

  snapshot: "完整上下文快照（可恢复）"
```

**版本切换**：
```python
def switch_context_version(target_version):
    # 保存当前版本
    current_snapshot = save_context_snapshot()

    # 加载目标版本
    target_snapshot = load_context_snapshot(target_version)

    # 验证兼容性
    if not compatible(current_snapshot, target_snapshot):
        warning("版本不兼容，可能导致上下文不一致")

    return target_snapshot
```

---

## 故障排除

### 问题1：上下文失效

**症状**：
- AI开始重复相同的错误
- AI遗忘之前的约定
- 响应质量明显下降

**诊断**：
```python
# 检查上下文大小
token_count = calculate_tokens(context)
if token_count > 50000:
    cause = "上下文过大"

# 检查信息一致性
if has_contradictions(context):
    cause = "上下文矛盾"

# 检查信息新鲜度
if information_stale(context):
    cause = "上下文过期"

# 检查相关性
if relevance_score(context, task) < 0.3:
    cause = "上下文不相关"
```

**解决方案**：
- 压缩：摘要历史信息
- 清理：移除无关内容
- 更新：刷新过期信息
- 重构：重新组织结构

### 问题2：Lost-in-the-Middle

**症状**：
- AI无法检索中间位置的信息
- 关键信息被忽略

**解决方案**：
```yaml
strategy1: 重新排序
  action: "将关键信息移到首尾"

strategy2: 分段处理
  action: "将大上下文分成多个小段"

strategy3: 显式提示
  action: "在提示词中明确指出关键信息位置"

strategy4: 重复强调
  action: "在开头和结尾都重复关键信息"
```

### 问题3：上下文毒化

**症状**：
- AI在不同信息间反复摇摆
- 决策不一致
- 答案不确定

**解决方案**：
```yaml
immediate_actions:
  - 识别矛盾信息
  - 明确优先级（时间、来源、权威性）
  - 移除低质量信息

long_term_prevention:
  - 建立版本控制机制
  - 添加信息质量标签
  - 使用约束生成器强制优先级
```

---

## 实战练习

### 练习1：重构大型模块

**任务**：重构一个包含30个文件的大型模块

**要求**：
- 保持上下文在15K tokens以内
- 分批实施，每批不超过5个文件
- 保持进展可追踪

**提示**：使用分批实施策略 + 会话状态快照

### 练习2：调试复杂问题

**任务**：调试一个在生产环境出现但本地无法复现的bug

**要求**：
- 收集足够的相关信息
- 避免信息过载
- 保持上下文聚焦

**提示**：使用动态上下文组装 + 相关性评分

### 练习3：跨会话恢复工作

**任务**：在多天时间里逐步实现一个复杂功能

**要求**：
- 每天结束时保存会话状态
- 第二天能够无缝恢复
- 避免重复讨论

**提示**：使用会话状态快照 + 版本控制

---

*本提示词文件覆盖中级复杂场景（约2000 tokens）*
