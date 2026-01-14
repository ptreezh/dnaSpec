# DNASPEC 部署指南

## 目录

1. [部署前准备](#部署前准备)
2. [NPM 包部署](#npm-包部署)
3. [开发模式部署](#开发模式部署)
4. [生产环境部署](#生产环境部署)
5. [多平台配置](#多平台配置)
6. [环境验证](#环境验证)
7. [故障排除](#故障排除)

---

## 部署前准备

### 系统要求

#### 最低要求

| 组件 | 版本 | 说明 |
|------|------|------|
| **Node.js** | >= 14.0.0 | JavaScript 运行时 |
| **npm** | >= 6.0.0 | 包管理器 |
| **Python** | >= 3.8 | 核心技能执行 |
| **磁盘空间** | >= 100MB | 安装和运行 |
| **内存** | >= 2GB | 推荐值 |

#### 推荐配置

| 组件 | 版本 | 说明 |
|------|------|------|
| **Node.js** | >= 18.0.0 | LTS 版本 |
| **npm** | >= 9.0.0 | 最新特性支持 |
| **Python** | >= 3.10 | 稳定性和性能 |

### 环境检查

在部署前，运行环境检查：

```bash
# 检查 Node.js
node --version
# 期望输出: v18.x.x 或更高

# 检查 npm
npm --version
# 期望输出: 9.x.x 或更高

# 检查 Python
python --version
# 期望输出: Python 3.8.x 或更高

# 检查权限
npm config get prefix
# 确保有写入权限
```

---

## NPM 包部署

### 方式1: 全局安装（推荐）

#### 安装步骤

```bash
# 1. 全局安装
npm install -g dnaspec

# 2. 验证安装
dnaspec --version
# 输出: dnaspec v2.0.5

# 3. 查看可用技能
dnaspec list
```

#### 路径配置

如果命令未识别，需要配置 PATH：

**Linux/macOS**:
```bash
# 查找 npm 全局路径
npm config get prefix
# 输出: /usr/local

# 添加到 PATH
export PATH=$PATH:/usr/local/bin

# 永久添加（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

**Windows**:
```powershell
# 查找 npm 全局路径
npm config get prefix
# 输出: C:\Users\Username\AppData\Roaming\npm

# 添加到 PATH（系统设置）
# 环境变量 -> 系统变量 -> Path -> 编辑
# 添加: C:\Users\Username\AppData\Roaming\npm
```

### 方式2: 项目本地安装

```bash
# 1. 初始化项目
mkdir my-project
cd my-project
npm init -y

# 2. 安装 dnaspec
npm install dnaspec

# 3. 使用 npx 运行
npx dnaspec list

# 4. 或添加到 package.json scripts
```

在 `package.json` 中添加DNASPEC管理脚本：

```json
{
  "scripts": {
    "dnaspec:list": "dnaspec list",
    "dnaspec:deploy": "dnaspec deploy",
    "dnaspec:validate": "dnaspec validate"
  }
}
```

使用：

```bash
npm run dnaspec:list      # 列出所有技能
npm run dnaspec:deploy    # 部署到AI编辑器
npm run dnaspec:validate  # 验证安装
```

**注意**: 技能需要在AI编辑器（如Claude/Cursor）中使用Slash命令调用：
```bash
/dnaspec.agent-creator "创建智能体"
/dnaspec.task-decomposer "分解任务"
```

### 方式3: 开发模式安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-repo/dnaspec.git
cd dnaspec

# 2. 安装依赖
npm install

# 3. 链接到全局
npm link

# 4. 验证
dnaspec --version
```

---

## 生产环境部署

### 1. 服务器部署

#### 准备工作

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS/RHEL

# 2. 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 3. 安装 Python
sudo apt install -y python3 python3-pip

# 4. 安装 dnaspec
sudo npm install -g dnaspec
```

#### 配置服务

创建系统服务（Ubuntu 示例）：

```bash
# 创建服务文件
sudo nano /etc/systemd/system/dnaspec.service
```

内容：

```ini
[Unit]
Description=DNASPEC CLI Tool
After=network.target

[Service]
Type=simple
User=dnaspec
ExecStart=/usr/bin/dnaspec list
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable dnaspec

# 启动服务
sudo systemctl start dnaspec

# 查看状态
sudo systemctl status dnaspec
```

### 2. Docker 部署

#### Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM node:18-alpine

# 安装 Python
RUN apk add --no-cache python3 py3-pip

# 安装 dnaspec
RUN npm install -g dnaspec

# 创建工作目录
WORKDIR /app

# 验证安装
RUN dnaspec --version

# 默认命令
CMD ["dnaspec", "list"]
```

#### docker-compose.yml

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  dnaspec:
    build: .
    container_name: dnaspec
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - DNASPEC_LOG_LEVEL=info
      - DNASPEC_MEMORY_PATH=/app/data/memory
    ports:
      - "3000:3000"  # 如果有 web 界面
```

构建和运行：

```bash
# 构建镜像
docker-compose build

# 运行容器
docker-compose up -d

# 执行命令
docker-compose exec dnaspec dnaspec list
```

### 3. CI/CD 集成

#### GitHub Actions

创建 `.github/workflows/test.yml`:

```yaml
name: Test DNASPEC

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install DNASPEC
        run: npm install -g dnaspec

      - name: Verify Installation
        run: dnaspec --version

      - name: List Skills
        run: dnaspec list

      - name: Validate Installation
        run: dnaspec validate

      # 注意: 技能需要在AI编辑器环境中测试，不能在CI中直接执行
      # 在支持的AI编辑器中测试: /dnaspec.agent-creator "测试"
```

#### GitLab CI

创建 `.gitlab-ci.yml`:

```yaml
image: node:18

stages:
  - test

test:
  stage: test
  script:
    - npm install -g dnaspec
    - dnaspec --version
    - dnaspec list
```

---

## 多平台配置

### Claude 配置

配置文件：`.claude/settings.json`

```json
{
  "cli": {
    "enabled": true,
    "dnaspec": {
      "enabled": true,
      "path": "dnaspec",
      "args": ["--verbose"]
    }
  }
}
```

### VS Code 配置

创建 `.vscode/settings.json`:

```json
{
  "dnaspec.enabled": true,
  "dnaspec.autoComplete": true,
  "dnaspec.format": "json"
}
```

### IFLOW 配置

IFLOW 配置自动检测，无需额外配置。

---

## 环境验证

### 基础验证脚本

创建 `verify_installation.sh`:

```bash
#!/bin/bash

echo "DNASPEC 环境验证"
echo "=================="

# 1. Node.js 检查
echo -n "Node.js: "
if command -v node &> /dev/null; then
    node --version
else
    echo "未安装"
    exit 1
fi

# 2. npm 检查
echo -n "npm: "
if command -v npm &> /dev/null; then
    npm --version
else
    echo "未安装"
    exit 1
fi

# 3. Python 检查
echo -n "Python: "
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "未安装"
    exit 1
fi

# 4. DNASPEC 检查
echo -n "DNASPEC: "
if command -v dnaspec &> /dev/null; then
    dnaspec --version
else
    echo "未安装"
    exit 1
fi

echo ""
echo "✅ 所有检查通过！"
```

运行验证：

```bash
chmod +x verify_installation.sh
./verify_installation.sh
```

### 功能测试

```bash
# 测试1: 基础命令
dnaspec --version
dnaspec --help
dnaspec list

# 测试2: 部署验证
dnaspec validate
dnaspec deploy

# 测试3: 在AI编辑器中测试技能（在Claude/Cursor/Qwen中执行）
# /dnaspec.agent-creator "测试智能体创建"
# /dnaspec.task-decomposer "测试任务分解"
# /dnaspec.constraint-generator "测试约束生成"

# 测试4: 记忆系统（可选）
python scripts/setup_memory.py
python examples/ci_project_helper.py
```

---

## 故障排除

### 问题1: 命令未找到

**症状**: `dnaspec: command not found`

**解决方案**:

1. 检查安装：
```bash
npm list -g dnaspec
```

2. 查看全局路径：
```bash
npm config get prefix
```

3. 手动添加 PATH：
```bash
export PATH=$PATH:$(npm config get prefix)/bin
```

4. 重新安装：
```bash
npm uninstall -g dnaspec
npm install -g dnaspec
```

### 问题2: Python 模块导入错误

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:

```bash
# 1. 检查 Python 版本
python --version

# 2. 安装缺失的模块
pip install -r requirements.txt

# 3. 或使用虚拟环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题3: 技能执行失败

**症状**: 技能执行报错

**调试步骤**:

```bash
# 1. 查看详细日志
dnaspec <skill-name> "<task>" --debug

# 2. 检查技能配置
dnaspec info <skill-name>

# 3. 测试技能
cd skills/<skill-name>
python -m pytest tests/
```

### 问题4: 记忆系统错误

**症状**: 记忆保存/读取失败

**解决方案**:

```bash
# 1. 检查权限
ls -la memory_storage/

# 2. 重新初始化
python scripts/setup_memory.py

# 3. 清理并重建
rm -rf memory_storage/
python scripts/setup_memory.py
```

---

## 性能优化

### 1. 内存优化

```bash
# 限制 Node.js 内存
export NODE_OPTIONS="--max-old-space-size=4096"

# 或在启动脚本中
node --max-old-space-size=4096 $(which dnaspec) list
```

### 2. 并发处理

```bash
# 并行执行多个任务
dnaspec batch tasks.txt --parallel --jobs 4
```

### 3. 缓存配置

```json
{
  "cache": {
    "enabled": true,
    "max_size": 100,
    "ttl": 3600
  }
}
```

---

## 监控和日志

### 日志配置

创建 `~/.dnaspec/logging.json`:

```json
{
  "level": "info",
  "file": "/var/log/dnaspec/app.log",
  "max_size": "100M",
  "max_files": 10
}
```

### 监控命令

```bash
# 查看系统状态
dnaspec status

# 查看记忆系统状态
python scripts/monitor_memory.py

# 查看技能统计
dnaspec stats
```

---

## 备份和恢复

### 备份

```bash
# 1. 备份配置
cp -r ~/.dnaspec ~/backup/dnaspec-config-$(date +%Y%m%d)

# 2. 备份记忆
python scripts/backup_memory.py

# 3. 备份技能
tar -czf dnaspec-skills-$(date +%Y%m%d).tar.gz skills/
```

### 恢复

```bash
# 1. 恢复配置
cp -r ~/backup/dnaspec-config-20251226 ~/.dnaspec

# 2. 恢复记忆
tar -xzf memory_backups/backup_20251226.tar.gz -C /
```

---

## 升级策略

### 滚动升级

```bash
# 1. 检查当前版本
dnaspec --version

# 2. 查看最新版本
npm view dnaspec version

# 3. 更新
npm update -g dnaspec

# 4. 验证
dnaspec --version
dnaspec list
```

### 回滚

```bash
# 1. 查看已安装版本
npm list -g dnaspec

# 2. 安装特定版本
npm install -g dnaspec@2.0.3

# 3. 验证
dnaspec --version
```

---

## 安全建议

### 1. 权限管理

```bash
# 以非 root 用户运行
sudo adduser dnaspec
su - dnaspec
npm install -g dnaspec
```

### 2. 文件权限

```bash
# 限制配置文件权限
chmod 600 ~/.dnaspec/config.json

# 限制日志权限
chmod 644 /var/log/dnaspec/*
```

### 3. 网络安全

```bash
# 使用 HTTPS 安装
npm config set registry https://registry.npmjs.org/

# 验证包完整性
npm install --verify dnaspec
```

---

## 附录

### A. 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DNASPEC_HOME` | 配置目录 | `~/.dnaspec` |
| `DNASPEC_LOG_LEVEL` | 日志级别 | `info` |
| `DNASPEC_MEMORY_PATH` | 记忆路径 | `./memory_storage` |
| `DNASPEC_CACHE_SIZE` | 缓存大小 | `100` |

### B. 配置文件位置

| 平台 | 配置文件 |
|------|----------|
| **Linux/macOS** | `~/.dnaspec/config.json` |
| **Windows** | `%APPDATA%/dnaspec/config.json` |

### C. 相关资源

- **NPM 包**: https://www.npmjs.com/package/dnaspec
- **GitHub**: https://github.com/your-repo/dnaspec
- **文档**: https://docs.dnaspec.dev

---

**部署指南版本**: v2.0.5
**最后更新**: 2025-12-26
