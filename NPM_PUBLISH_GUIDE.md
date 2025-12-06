# DSGS Context Engineering Skills - NPM发布指南

## 发布前准备

### 1. 确认修改
- [x] 修复了npm配置脚本路径问题
- [x] 所有修改已提交到git
- [x] 版本号已更新到1.0.3

### 2. 检查项目状态
```bash
# 检查git状态（应显示干净）
git status

# 检查版本号
npm version
```

## 发布选项

### 选项1：发布到原包（需要权限）
如果您有`dnaspec`包的发布权限：

```bash
# 1. 登录npm账户
npm login

# 2. 验证包内容
npm pack  # 会生成一个.tgz文件供检查

# 3. 发布
npm publish
```

### 选项2：发布为新包（推荐）
如果您没有原包的权限或希望发布自己的版本：

1. 修改package.json中的包名：
```json
{
  "name": "my-dnaspec",  // 或其他未被占用的名称
  "version": "1.0.3",
  // ... 其他配置
}
```

2. 按照上述步骤发布

### 选项3：发布到自己的作用域
```json
{
  "name": "@yourusername/dnaspec",  // 例如 @myuser/dnaspec
  "version": "1.0.3",
  // ... 其他配置
}
```

## 验证发布

发布后，可以通过以下方式验证：

```bash
# 1. 从npm安装
npm install -g dnaspec  # 或您发布的包名

# 2. 测试功能
dnaspec

# 3. 验证修复是否生效
# 尝试安装并确认配置脚本路径问题已解决
```

## Git标签管理

npm version命令已自动创建git标签：
```bash
git tag  # 查看所有标签
git push origin main --tags  # 推送标签到远程仓库
```

## 重要提醒

1. **权限问题**：您可能无法发布到现有的`dnaspec`包，因为它属于原作者
2. **版本控制**：每次发布前必须更新版本号
3. **测试**：发布前请确保在本地测试所有功能
4. **文档**：更新README.md以反映新版本的特性和修复

## 恢复操作

如果需要撤销版本更新：
```bash
git tag -d v1.0.3  # 删除本地标签
git push --delete origin v1.0.3  # 删除远程标签（如果已推送）
git reset --hard HEAD~1  # 回到上一个提交（谨慎使用）
```

## 最新修复说明

**修复内容**：
- 修复了npm安装过程中`run_auto_config.py`脚本路径错误的问题
- 问题：`spawn`函数使用相对路径`run_auto_config.py`，在npm全局安装时无法找到文件
- 解决：使用`path.join(projectDir, 'run_auto_config.py')`构建绝对路径

**影响**：
- 修复前：npm安装后自动配置失败
- 修复后：npm安装后自动配置正常工作