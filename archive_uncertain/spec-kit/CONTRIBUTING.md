# 贡献指南

感谢您对spec.kit项目的兴趣！我们欢迎任何形式的贡献，无论是报告错误、提出新功能、改善文档还是提交代码。

## 行为准则

参与本项目前，请阅读我们的 [行为准则](CODE_OF_CONDUCT.md)。

## 贡献方式

### 1. 报告错误

如果您发现了错误，请通过GitHub Issues报告。请确保您的报告包含：

- **清晰的标题和描述**
- **重现步骤**（如果适用）
- **预期行为**与**实际行为**的对比
- **环境信息**（操作系统、AI平台版本等）
- **相关日志或错误信息**

### 2. 请求新功能

我们欢迎功能请求！请创建一个Issue，详细描述：

- 您希望添加的功能
- 该功能如何解决问题
- 使用场景和示例
- 与其他功能的区别

### 3. 提交代码

#### 环境设置

1. **Fork 仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/spec-kit.git
   cd spec-kit
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或者
   git checkout -b bugfix/issue-number
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

#### 代码规范

- **Python**: 遵感和Google Python风格
- **注释**: 为所有函数和类编写清晰的文档字符串
- **测试**: 为新功能编写单元测试
- **提交信息**: 遵感Conventional Commits规范

#### 提交流程

1. **编写测试**
   ```bash
   # 为新功能或修复编写测试
   pytest tests/
   ```

2. **运行测试**
   ```bash
   pytest --cov=src tests/
   ```

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add new skill for context analysis"
   ```

4. **推送并创建Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # 然后在GitHub上创建PR
   ```

### 4. 改善文档

文档改善同样受欢迎！您可以：

- 修正拼写和语法错误
- 改善说明和示例
- 添加使用案例
- 本地化内容

## 开发流程

### 项目结构
```
spec-kit/
├── skills/                 # Claude Skills实现
├── scripts/                # Python脚本
├── docs/                   # 文档
├── tests/                  # 测试
├── commands/               # 命令文件
├── README.md               # 主文档
├── CONTRIBUTING.md         # 本文件
├── CODE_OF_CONDUCT.md      # 行为准则
└── requirements.txt        # 依赖
```

### 测试指南

- **单元测试**: 为每个脚本功能编写单元测试
- **集成测试**: 测试技能间的交互
- **端到端测试**: 测试完整的用户场景
- **覆盖率**: 目标100%测试覆盖率

### 代码审查

所有拉取请求都需要审查。审查关注：

- **功能正确性**: 代码是否按预期工作
- **代码质量**: 清晰、可维护、遵循规范
- **测试**: 是否有足够测试覆盖
- **文档**: 是否有适当文档

## 需要帮助？

如果您需要帮助或有问题：

- 查看 [文档](docs/)
- 在Issues中提问
- 联系维护者 (3061176@qq.com)

## 感谢

再次感谢您对spec.kit项目的贡献！每一个贡献都在帮助我们创建更好的AI辅助开发工具。

---

*本项目遵循开放包容的贡献政策。我们欢迎来自所有背景的贡献者。*