# dnaspec npm包发布指南

## 包信息
- **包名**: `dnaspec`
- **版本**: 1.0.2
- **描述**: Dynamic Specification Growth System - Context Engineering Skills for AI-assisted development
- **作者**: pTree Dr.Zhang (AI Persona Lab 2025)
- **命令行工具**: `dnaspec` (不再提供`dsgs`别名)

## 发布前检查

### 1. 确认package.json信息
- [x] 包名 `dnaspec` 尚未被占用
- [x] 版本号正确 (`1.0.2`)
- [x] 描述信息准确
- [x] 所有依赖项已正确声明
- [x] `files` 字段包含了必要的文件

### 2. 验证功能
```bash
# 本地安装测试
npm install -g .
dsgs
# 或
dnaspec
```

### 3. 检查文件
```bash
npm pack --dry-run
```

## 发布流程

### 1. 注册npm账户
如果还没有npm账户，请先在 https://www.npmjs.com/signup 注册。

### 2. 登录npm
```bash
npm login
# 按提示输入用户名、密码和邮箱
```

### 3. 发布包
```bash
npm publish --access public
```

## 发布后验证

### 1. 检查npmjs.com网站
访问 https://www.npmjs.com/package/dnaspec 确认包已发布成功

### 2. 测试安装
```bash
# 创建测试目录
mkdir test-dnaspec
cd test-dnaspec
npm install -g dnaspec
dsgs
```

## 后续版本更新

### 1. 版本更新
```bash
# 修复bug使用patch
npm version patch

# 新功能使用minor
npm version minor

# 重大更新使用major
npm version major
```

### 2. 重新发布
```bash
npm publish
```

## 注意事项

1. 包名`dnaspec`必须是唯一的
2. 包发布的版本号不能重复，每次更新必须增加版本号
3. 确保所有敏感信息都已从代码中移除
4. 所有文件都已正确包含在`files`字段中
5. 发布前进行全面测试

## 依赖要求

用户安装此包需要：
- Node.js >= 14.0.0
- Python >= 3.8
- Git >= 2.0.0

## 包含的文件

根据package.json的files字段，以下文件将被包含在发布的包中：
- index.js
- package.json
- README.md
- launch_dnaspec.bat
- launch_dnaspec.sh
- src/**/* (所有src目录下的文件)
- pyproject.toml
- 所有.md文档文件

## 回滚策略

如果发布有问题的版本，可以：
```bash
# 取消发布（24小时内）
npm unpublish dnaspec@<version>

# 或发布修复版本
npm version patch
npm publish
```