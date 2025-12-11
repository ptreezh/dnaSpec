# DNASPEC跨CLI技能部署方案

## 1. 当前架构分析

### 1.1 核心组件
1. **BaseSkill类** (`src/dna_spec_kit_integration/core/skill_base.py`)
   - 提供标准化的技能接口
   - 支持渐进式信息披露（BASIC/STANDARD/DETAILED）
   - 统一的输入验证和错误处理机制

2. **重构后的技能实现** (`src/dna_spec_kit_integration/skills/*_refactored.py`)
   - 继承BaseSkill类
   - 实现_execute_skill_logic和_format_output方法
   - 支持不同详细级别的输出格式

3. **技能执行器** (`src/dna_spec_kit_integration/core/skill_executor.py`)
   - 协调技能映射和Python桥接器
   - 验证输入参数并格式化输出结果

4. **Python桥接器** (`src/dna_spec_kit_integration/core/python_bridge.py`)
   - 动态导入和执行Python技能模块
   - 提供统一的技能执行接口

### 1.2 接口规范
```python
# 标准化输入参数
args = {
    "input": "主要输入内容",
    "detail_level": "basic|standard|detailed",
    "options": {},  # 可选配置参数
    "context": {}   # 上下文信息
}

# 标准化输出格式
result = {
    "status": "success|error",
    "data": {},  # 技能执行结果
    "metadata": {
        "skill_name": "技能名称",
        "execution_time": 0.123,
        "confidence": 0.85,
        "detail_level": "standard"
    }
}
```

## 2. 跨CLI部署架构设计

### 2.1 部署器核心类
```python
class RealSkillDeployer:
    def deploy_skills_to_platform(self, platform_name: str, platform_info: Dict[str, Any]) -> Dict[str, Any]:
        # 根据平台类型部署技能
        if platform_name == 'claude':
            return self._deploy_to_claude(extension_path)
        elif platform_name == 'qwen':
            return self._deploy_to_qwen(extension_path)
        # ... 其他平台
```

### 2.2 平台适配策略

#### Claude CLI
- 使用Claude自定义技能规范格式
- 生成JSON配置文件描述技能接口
- 支持命令映射和权限声明

#### Qwen CLI
- 使用Qwen插件规范格式
- 生成function类型的插件定义
- 支持OpenAI兼容的函数调用接口

#### 通用平台
- 使用DSKS（DNASPEC Skill Kit Specification）格式
- 生成统一的配置文件描述所有技能
- 支持斜杠命令调用方式

## 3. TDD驱动实施方案

### 3.1 测试计划

#### 单元测试
1. **BaseSkill类测试**
   - 输入验证功能测试
   - 错误处理机制测试
   - 渐进式信息披露功能测试

2. **重构技能测试**
   - 各技能_execute_skill_logic方法测试
   - 不同详细级别输出格式测试
   - 边界条件和异常情况测试

#### 集成测试
1. **技能执行器测试**
   - 技能映射功能测试
   - Python桥接器集成测试
   - 输入验证和输出格式化测试

2. **部署器测试**
   - 各平台部署功能测试
   - 配置文件生成测试
   - 部署结果验证测试

#### 端到端测试
1. **跨CLI技能调用测试**
   - Claude CLI调用DNASPEC技能测试
   - Qwen CLI调用DNASPEC技能测试
   - 通用平台调用DNASPEC技能测试

### 3.2 实施步骤

#### 第一阶段：基础框架完善
1. 创建测试目录结构
2. 编写BaseSkill类单元测试
3. 完善重构技能的测试覆盖
4. 建立持续集成测试流程

#### 第二阶段：部署器增强
1. 扩展RealSkillDeployer支持更多CLI平台
2. 实现独立的技能执行函数
3. 添加部署验证和回滚机制
4. 编写部署器集成测试

#### 第三阶段：跨CLI验证
1. 搭建多CLI测试环境
2. 实现端到端技能调用测试
3. 验证渐进式信息披露功能
4. 性能基准测试和优化

## 4. 关键技术要点

### 4.1 渐进式信息披露实现
- 通过DetailLevel枚举控制输出详细程度
- 在_format_output方法中实现不同级别的格式化逻辑
- 保持向后兼容性同时提供增强功能

### 4.2 跨平台适配
- 抽象平台特定的部署逻辑
- 使用配置驱动的部署策略
- 统一错误处理和日志记录机制

### 4.3 独立执行支持
- 为每个技能提供独立的执行函数
- 实现命令行接口支持
- 支持JSON输入输出格式

## 5. 风险评估与缓解

### 5.1 技术风险
1. **平台兼容性问题**
   - 缓解：建立平台兼容性矩阵，定期验证

2. **性能瓶颈**
   - 缓解：实现缓存机制，优化技能加载流程

3. **部署失败回滚**
   - 缓解：实现备份和恢复机制

### 5.2 实施风险
1. **测试覆盖不足**
   - 缓解：采用TDD方法，确保测试先行

2. **文档缺失**
   - 缓解：同步更新技术文档和用户手册

## 6. 验收标准

### 6.1 功能验收
- [ ] 所有重构技能通过单元测试
- [ ] 支持至少3个CLI平台部署
- [ ] 渐进式信息披露功能正常工作
- [ ] 独立执行模式可用

### 6.2 性能验收
- [ ] 技能加载时间 < 100ms
- [ ] 技能执行时间 < 1s（简单任务）
- [ ] 内存占用 < 50MB

### 6.3 兼容性验收
- [ ] Windows/Linux/macOS平台支持
- [ ] Python 3.7+版本兼容
- [ ] 主流CLI工具集成验证