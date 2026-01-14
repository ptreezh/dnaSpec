# DNASPEC 故障排除指南

## 目录

1. [安装问题](#安装问题)
2. [运行时错误](#运行时错误)
3. [平台特定问题](#平台特定问题)
4. [记忆系统问题](#记忆系统问题)
5. [性能问题](#性能问题)
6. [配置错误](#配置错误)
7. [调试技巧](#调试技巧)
8. [获取帮助](#获取帮助)

---

## 安装问题

### 问题1: `dnaspec: command not found`

**症状**:
```bash
$ dnaspec --version
bash: dnaspec: command not found
```

**原因分析**:
- npm 全局安装路径未添加到 PATH
- Node.js/npm 未正确安装
- 安装过程未完成

**解决方案**:

**步骤1: 验证安装**
```bash
# 检查是否真的安装了
npm list -g dnaspec

# 如果显示 empty，说明没有安装成功
# 重新安装:
npm install -g dnaspec
```

**步骤2: 查找安装路径**
```bash
# 查看npm全局路径
npm config get prefix

# Linux/macOS 输出示例:
# /usr/local

# Windows 输出示例:
# C:\Users\Username\AppData\Roaming\npm
```

**步骤3: 配置 PATH**

**Linux/macOS**:
```bash
# 临时添加（当前会话）
export PATH=$PATH:$(npm config get prefix)/bin

# 永久添加到 ~/.bashrc
echo 'export PATH=$PATH:'$(npm config get prefix)'/bin' >> ~/.bashrc
source ~/.bashrc

# 永久添加到 ~/.zshrc (macOS默认)
echo 'export PATH=$PATH:'$(npm config get prefix)'/bin' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)**:
```powershell
# 查看当前PATH
$env:PATH -split ';'

# 临时添加
$npmPath = npm config get prefix
$env:PATH += ";$npmPath"

# 永久添加（需要管理员权限）
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$npmPath",
    "User"
)
```

**Windows (GUI)**:
1. 右键 "此电脑" -> "属性"
2. "高级系统设置" -> "环境变量"
3. 在 "用户变量" 中找到 "Path"
4. 点击 "编辑" -> "新建"
5. 添加 npm 路径（例如: `C:\Users\Username\AppData\Roaming\npm`）

**步骤4: 验证修复**
```bash
dnaspec --version
# 应该输出: dnaspec v2.0.5
```

---

### 问题2: `EACCES: permission denied`

**症状**:
```bash
$ npm install -g dnaspec
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules/dnaspec
npm ERR! errno -13
npm ERR! Error: EACCES: permission denied
```

**原因分析**:
- 缺少写入全局目录的权限
- Linux/macOS 安全限制

**解决方案**:

**方案1: 使用 sudo（不推荐）**
```bash
sudo npm install -g dnaspec
```

**方案2: 修复 npm 权限（推荐）**
```bash
# 1. 创建全局目录
mkdir ~/.npm-global

# 2. 配置 npm 使用新目录
npm config set prefix '~/.npm-global'

# 3. 添加到 PATH
echo 'export PATH=$PATH:~/.npm-global/bin' >> ~/.bashrc
source ~/.bashrc

# 4. 重新安装
npm install -g dnaspec
```

**方案3: 使用 nvm（最佳实践）**
```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载配置
source ~/.bashrc

# 安装 Node.js
nvm install node

# 安装 dnaspec（不需要 sudo）
npm install -g dnaspec
```

---

### 问题3: Node.js 版本过低

**症状**:
```bash
$ npm install -g dnaspec
npm ERR! code ENOTSUP
npm ERR! notsup Unsupported engine
```

**原因分析**:
- Node.js 版本低于 14.0.0
- dnaspec 需要 Node.js >= 14.0.0

**解决方案**:

**检查当前版本**:
```bash
node --version
npm --version
```

**升级 Node.js**:

**Ubuntu/Debian**:
```bash
# 使用 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 验证
node --version  # 应该是 v18.x.x
```

**macOS**:
```bash
# 使用 Homebrew
brew install node

# 或使用 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

**Windows**:
1. 访问 https://nodejs.org/
2. 下载 LTS 版本（推荐 18.x 或更高）
3. 运行安装程序

**升级后重新安装**:
```bash
npm install -g dnaspec
```

---

### 问题4: Python 环境问题

**症状**:
```bash
$ dnaspec deploy
Error: Python not found or version too old
```

**原因分析**:
- Python 未安装
- Python 版本 < 3.8
- Python 未添加到 PATH

**解决方案**:

**检查 Python**:
```bash
python --version
# 或
python3 --version
```

**安装 Python**:

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

**macOS**:
```bash
# 使用 Homebrew
brew install python@3.11
```

**Windows**:
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.8+ 安装程序
3. ⚠️ 安装时勾选 "Add Python to PATH"

**配置 Python**:

如果 Python 已安装但未识别:
```bash
# Linux/macOS - 添加到 PATH
which python3
# 输出: /usr/bin/python3

echo 'alias python=python3' >> ~/.bashrc
source ~/.bashrc

# Windows - 手动添加到环境变量
# 1. 找到 Python 安装路径（例如: C:\Python311）
# 2. 添加到 PATH 环境变量
```

---

## 运行时错误

### 问题1: 技能执行失败

**症状**:
```bash
$ dnaspec deploy
Error: Skill execution failed
```

**诊断步骤**:

**1. 启用调试模式**
```bash
dnaspec deploy --debug
# 查看详细错误信息
```

**2. 检查技能是否存在**
```bash
dnaspec list
# 确认技能在列表中

dnaspec info agent-creator
# 查看技能详细信息
```

**3. 验证 Python 环境**
```bash
python -c "import sys; print(sys.path)"
# 确认 src/dna_context_engineering 在路径中

python -c "from dna_context_engineering import skills_system"
# 应该没有错误
```

**4. 测试技能直接执行**
```bash
cd skills/agent-creator
python skill.py
# 如果出错，说明技能本身有问题
```

**常见解决方案**:

**方案A: 重新安装**
```bash
npm uninstall -g dnaspec
npm install -g dnaspec
```

**方案B: 修复 Python 路径**
```bash
# 找到项目根目录
cd /path/to/dnaspec

# 添加到 Python 路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src:$(pwd)"

# 或永久添加
echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/dnaspec/src:/path/to/dnaspec"' >> ~/.bashrc
```

**方案C: 安装依赖**
```bash
cd /path/to/dnaspec
pip install -r requirements.txt
```

---

### 问题2: 模块导入错误

**症状**:
```python
ModuleNotFoundError: No module named 'dna_context_engineering'
```

**原因分析**:
- Python 找不到模块
- 路径配置问题
- 虚拟环境问题

**解决方案**:

**方案1: 临时添加路径**
```bash
export PYTHONPATH="/path/to/dnaspec/src:/path/to/dnaspec:$PYTHONPATH"
```

**方案2: 使用 -m 运行**
```bash
cd /path/to/dnaspec
python -m dna_context_engineering.cli
```

**方案3: 安装为开发模式**
```bash
cd /path/to/dnaspec
pip install -e .
```

**方案4: 使用虚拟环境**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装
pip install -e .

# 运行
# 在AI编辑器中使用: /dnaspec.agent-creator "测试"
```

---

### 问题3: JSON 解析错误

**症状**:
```bash
Error: Invalid JSON output
```

**原因分析**:
- 技能输出格式错误
- 编码问题
- 输出被截断

**解决方案**:

**1. 验证技能**
```bash
# 在AI编辑器中使用技能
# /dnaspec.agent-creator "测试任务"
# 技能结果会直接在AI编辑器中显示
```

**2. 检查配置**
```bash
# 验证安装
dnaspec validate

# 查看技能列表
dnaspec list
```

**3. 重新部署**
```bash
# 重新部署技能
dnaspec deploy --force
```

---

### 问题4: 权限错误

**症状**:
```bash
PermissionError: [Errno 13] Permission denied: '/path/to/file'
```

**原因分析**:
- 文件或目录权限不足
- 被其他进程占用

**解决方案**:

**检查权限**:
```bash
ls -la /path/to/file
# 或 Windows
dir /path/to/file
```

**修复权限**:

**Linux/macOS**:
```bash
# 修改文件权限
chmod 644 /path/to/file

# 修改目录权限
chmod 755 /path/to/directory

# 修改所有权
sudo chown $USER:$USER /path/to/file
```

**Windows**:
```powershell
# 以管理员身份运行
# 或修改文件安全属性
```

**检查占用**:
```bash
# Linux/macOS
lsof /path/to/file

# Windows
# 使用资源监视器或 Process Explorer
```

---

## 平台特定问题

### Claude 平台问题

**症状**: Claude Code 无法识别 dnaspec 命令

**解决方案**:

**1. 验证安装**
```bash
dnaspec --version
```

**2. 配置 Claude**
创建 `.claude/settings.json`:
```json
{
  "cli": {
    "enabled": true,
    "dnaspec": {
      "enabled": true,
      "path": "dnaspec"
    }
  }
}
```

**3. 检查路径**
```bash
which dnaspec
# 确保 dnaspec 在 PATH 中
```

---

### IFLOW 平台问题

**症状**: IFLOW 命令执行失败

**解决方案**:

**1. 验证 IFLOW**
```bash
iflow --version
```

**2. 检查命令部署**
```bash
# 确认命令已部署
ls ~/.iflow/commands/dnaspec-*.md
```

**3. 重新部署**
```bash
python tools/cli_command_manager.py --deploy-iflow
```

---

### Cursor/Qwen 平台问题

**症状**: Slash 命令不工作

**解决方案**:

**1. 检查平台配置**
```bash
# 确认平台支持
dnaspec list --platforms
```

**2. 部署 Slash 命令**
```bash
# Cursor
cp skills/*/.cursor/commands ~/.cursor/commands/

# Qwen
cp skills/*/.qwen/commands ~/.qwen/commands/
```

**3. 重启编辑器**
- 完全退出并重启 Cursor/Qwen
- 重新加载命令

---

## 记忆系统问题

### 问题1: 记忆文件创建失败

**症状**:
```bash
Error: Cannot create memory file
```

**原因分析**:
- 目录权限不足
- 磁盘空间不足
- 无效的 agent_id

**解决方案**:

**1. 检查目录权限**
```bash
ls -la memory_storage/
```

**2. 创建目录**
```bash
mkdir -p memory_storage/agents
chmod 755 memory_storage/agents
```

**3. 检查磁盘空间**
```bash
df -h  # Linux/macOS
# 或
dir    # Windows
```

**4. 验证 agent_id**
```python
# agent_id 应该只包含安全字符
valid_id = re.sub(r'[^\w\-]', '_', agent_id)
```

---

### 问题2: 记忆检索失败

**症状**:
```bash
Error: Memory recall failed
```

**原因分析**:
- JSON 文件损坏
- 编码问题
- 不存在的 agent_id

**解决方案**:

**1. 验证 JSON 文件**
```bash
cd memory_storage/agents/<agent-id>
python -m json.tool mem_*.json
```

**2. 修复 JSON**
```bash
# 如果 JSON 损坏，可以尝试修复
# 或删除有问题的文件
rm memory_storage/agents/<agent-id>/mem_<corrupt-id>.json
```

**3. 检查编码**
```bash
file memory_storage/agents/<agent-id>/mem_*.json
# 应该显示: JSON data
```

---

### 问题3: 记忆系统占用空间过大

**症状**:
```bash
memory_storage/ 占用超过 500MB
```

**解决方案**:

**1. 监控大小**
```bash
python scripts/monitor_memory.py
```

**2. 清理记忆**
```bash
# 备份当前记忆
python scripts/backup_memory.py

# 删除旧记忆
find memory_storage/agents/ -name "mem_*.json" -mtime +30 -delete

# 或使用 Python
python -c "
from pathlib import Path
import json
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=30)
for mem_file in Path('memory_storage/agents').rglob('mem_*.json'):
    stat = mem_file.stat()
    if datetime.fromtimestamp(stat.st_mtime) < cutoff:
        mem_file.unlink()
"
```

**3. 调整配置**
```json
{
  "skills": {
    "task-decomposer": {
      "enabled": true,
      "max_short_term": 20,
      "max_long_term": 100,
      "auto_cleanup": true
    }
  }
}
```

**4. 禁用记忆（如果不需要）**
```json
{
  "enabled": false
}
```

---

### 问题4: 技能"不学习"

**症状**: 即使启用了记忆，技能似乎没有改进

**解释**: 这是**正常行为**

**真实情况**:
- 记忆系统是**日志系统**，不是 AI 学习系统
- 技能不会自动改进
- 只是保存了执行历史

**验证**:
```python
# 测试1: 同一输入总是产生相同输出
result1 = skill.execute({'input': 'test'})
result2 = skill.execute({'input': 'test'})
assert result1 == result2  # ✅ 相同

# 测试2: 查看记忆文件
ls memory_storage/agents/skill-*/
# 只是日志文件，不是训练数据
```

**如果需要真正的学习**:
- 使用向量数据库（Pinecone, Milvus）
- 集成大语言模型
- 实现反馈学习机制

详细说明: `MEMORY_SYSTEM_HONEST_ANALYSIS.md`

---

## 性能问题

### 问题1: 技能执行缓慢

**症状**:
```bash
# 在AI编辑器中使用: /dnaspec.task-decomposer "复杂任务"
# 执行超过 10 秒
```

**诊断**:

**1. 测量时间**
```bash
time dnaspec task-decomposer "测试"
```

**2. 启用性能分析**
```bash
dnaspec task-decomposer "测试" --profile
```

**解决方案**:

**方案A: 优化 Python**
```bash
# 使用 PyPy（更快）
pypy -m dna_context_engineering.cli

# 或优化 CPython
python -O -m dna_context_engineering.cli
```

**方案B: 限制记忆**
```json
{
  "max_short_term": 10,
  "max_long_term": 50
}
```

**方案C: 禁用记忆**
```bash
dnaspec task-decomposer "测试" --no-memory
```

**方案D: 增加内存**
```bash
# 限制 Node.js 内存
export NODE_OPTIONS="--max-old-space-size=4096"

# 或在启动时
node --max-old-space-size=4096 $(which dnaspec) list
```

---

### 问题2: 记忆检索慢

**症状**:
```bash
recall_memories() 超过 1 秒
```

**原因分析**:
- 记忆数量过多（> 10000）
- 简单的关键词匹配效率低

**性能数据**:
```
100 条记忆:   < 1ms
1,000 条记忆: ~10ms
10,000 条记忆: ~100ms
100,000 条记忆: ~1000ms (不可接受)
```

**解决方案**:

**方案A: 限制数量**
```python
config = MemoryConfig(
    enabled=True,
    max_short_term=50,
    max_long_term=200,
    auto_cleanup=True
)
```

**方案B: 定期清理**
```bash
# 每周清理
python scripts/cleanup_memory.py --older-than 7days
```

**方案C: 使用索引**
```python
# 实现简单索引（未来版本）
class IndexedMemory:
    def __init__(self):
        self.index = {}  # keyword -> list of memories

    def add_memory(self, memory):
        # 更新索引
        for keyword in self.extract_keywords(memory):
            if keyword not in self.index:
                self.index[keyword] = []
            self.index[keyword].append(memory)
```

**方案D: 升级到向量数据库**
```python
# 使用专业工具
import pinecone

# 或
from chromadb import Client
```

---

### 问题3: 内存占用过高

**症状**:
```bash
# 进程占用 > 1GB 内存
```

**解决方案**:

**1. 监控内存**
```bash
# Linux/macOS
top -p $(pgrep -f dnaspec)

# Windows
tasklist | findstr python
```

**2. 限制 Python 内存**
```bash
# 使用资源限制
ulimit -v 1048576  # 限制 1GB

# 或
resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
```

**3. 禁用记忆**
```python
config = MemoryConfig(enabled=False)
```

**4. 批量处理**
```bash
# 避免同时处理太多任务
dnaspec batch tasks.txt --jobs 1  # 串行
```

---

## 配置错误

### 问题1: 配置文件语法错误

**症状**:
```bash
Error: Invalid configuration JSON
```

**解决方案**:

**1. 验证 JSON**
```bash
# Python
python -m json.tool ~/.dnaspec/config.json

# 或使用 jq
jq '.' ~/.dnaspec/config.json
```

**2. 修复常见错误**

**错误: 缺少逗号**
```json
{
  "enabled": true
  "max_short_term": 50
}
```

**正确**:
```json
{
  "enabled": true,
  "max_short_term": 50
}
```

**错误: 尾部逗号**
```json
{
  "skills": {
    "agent-creator": {
      "enabled": true,
    }
  }
}
```

**正确**:
```json
{
  "skills": {
    "agent-creator": {
      "enabled": true
    }
  }
}
```

**错误: 引号问题**
```json
{
  "path": 'C:\Program Files\node'
}
```

**正确**:
```json
{
  "path": "C:\\Program Files\\node"
}
```

---

### 问题2: 环境变量未生效

**症状**:
```bash
echo $DNASPEC_MEMORY_PATH
# 输出为空
```

**解决方案**:

**Linux/macOS**:
```bash
# 临时设置
export DNASPEC_MEMORY_PATH=/custom/path
export DNASPEC_LOG_LEVEL=debug

# 永久设置
echo 'export DNASPEC_MEMORY_PATH=/custom/path' >> ~/.bashrc
echo 'export DNASPEC_LOG_LEVEL=debug' >> ~/.bashrc
source ~/.bashrc

# 验证
echo $DNASPEC_MEMORY_PATH
```

**Windows**:
```powershell
# 临时设置
$env:DNASPEC_MEMORY_PATH="C:\custom\path"
$env:DNASPEC_LOG_LEVEL="debug"

# 永久设置（PowerShell）
[Environment]::SetEnvironmentVariable(
    "DNASPEC_MEMORY_PATH",
    "C:\custom\path",
    "User"
)

# 永久设置（CMD）
setx DNASPEC_MEMORY_PATH "C:\custom\path"

# 验证
$env:DNASPEC_MEMORY_PATH
```

---

### 问题3: 平台配置冲突

**症状**: 多个平台配置冲突

**解决方案**:

**1. 检查配置优先级**
```
命令行参数 > 环境变量 > 配置文件 > 默认值
```

**2. 查看生效配置**
```bash
dnaspec --dump-config
```

**3. 重置配置**
```bash
# 备份
cp ~/.dnaspec/config.json ~/.dnaspec/config.json.bak

# 重置
rm ~/.dnaspec/config.json
dnaspec --init-config
```

---

## 调试技巧

### 1. 启用详细日志

```bash
# 启用调试模式
dnaspec <skill> "task" --debug

# 设置日志级别
export DNASPEC_LOG_LEVEL=DEBUG
# 在AI编辑器中使用: /dnaspec.agent-creator "测试"

# 查看日志文件
tail -f ~/.dnaspec/logs/dnaspec.log
```

### 2. 使用 Python 调试器

```python
# 在技能中设置断点
import pdb; pdb.set_trace()

# 或使用 ipdb（更好）
import ipdb; ipdb.set_trace()

# 运行
dnaspec <skill> "task" --debug
```

### 3. 追踪执行

```bash
# 追踪 Python 执行
python -m trace --trace /path/to/skill.py

# 追踪系统调用
strace -e trace=file dnaspec <skill> "task"  # Linux
# 或
dtruss dnaspec <skill> "task"  # macOS
```

### 4. 性能分析

```bash
# Python 性能分析
python -m cProfile -o profile.stats /path/to/skill.py

# 查看结果
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
"
```

### 5. 内存分析

```bash
# 使用 memory_profiler
pip install memory_profiler

# 在代码中添加
from memory_profiler import profile

@profile
def skill_function():
    ...

# 运行
python -m memory_profiler skill.py
```

### 6. 测试技能

```bash
# 单独测试技能
cd /path/to/dnaspec
python -m pytest tests/test_<skill>.py -v

# 测试单个函数
python -m pytest tests/test_<skill>.py::test_function -v

# 查看覆盖率
python -m pytest tests/ --cov=skills/<skill> --cov-report=html
```

---

## 获取帮助

### 1. 查看文档

```bash
# 项目文档
cd /path/to/dnaspec
ls docs/

# 在线文档
# https://docs.dnaspec.dev
```

### 2. 社区支持

```bash
# GitHub Issues
https://github.com/your-repo/dnaspec/issues

# 搜索类似问题
https://github.com/your-repo/dnaspec/issues?q=is%3Aissue
```

### 3. 报告问题

**报告模板**:
```markdown
## 问题描述
简要描述问题

## 复现步骤
1. 执行命令: `dnaspec ...`
2. 输入: ...
3. 输出: ...

## 期望行为
应该发生什么

## 实际行为
实际发生了什么

## 环境信息
- OS: [Linux/macOS/Windows]
- Node.js: [版本]
- Python: [版本]
- DNASPEC: [版本]

## 日志输出
\`\`\`
dnaspec <skill> "task" --debug
\`\`\`

## 附加信息
其他相关信息
```

### 4. 联系方式

- **Email**: support@dnaspec.dev
- **Discord**: https://discord.gg/dnaspec
- **Twitter**: @dnaspec_dev

---

## 常见错误代码

| 错误代码 | 含义 | 解决方案 |
|---------|------|----------|
| `E01` | 命令未找到 | 检查 PATH 配置 |
| `E02` | Python 未安装 | 安装 Python 3.8+ |
| `E03` | 技能不存在 | 使用 `dnaspec list` 查看 |
| `E04` | 配置错误 | 验证 JSON 语法 |
| `E05` | 权限不足 | 修复文件权限 |
| `E06` | 内存不足 | 禁用记忆或增加内存 |
| `E07` | 网络错误 | 检查网络连接 |
| `E08` | 模块导入失败 | 检查 PYTHONPATH |
| `E09` | JSON 解析错误 | 验证输出格式 |
| `E10` | 记忆系统错误 | 检查文件系统 |

---

## 预防性维护

### 定期检查清单

```bash
# 每周执行
python scripts/monitor_memory.py
python scripts/backup_memory.py

# 每月执行
npm update -g dnaspec
dnaspec list
dnaspec --check-health

# 每季度执行
清理旧记忆文件
审查配置文件
更新依赖包
```

### 健康检查脚本

```bash
#!/bin/bash
# health_check.sh

echo "DNASPEC 健康检查"
echo "================"

# 1. 版本检查
echo -n "版本: "
dnaspec --version

# 2. 技能检查
echo -n "技能数量: "
dnaspec list | wc -l

# 3. 记忆检查
echo -n "记忆大小: "
du -sh memory_storage/ 2>/dev/null || echo "N/A"

# 4. 磁盘空间
echo -n "磁盘空间: "
df -h . | tail -1 | awk '{print $4 " 可用"}'

# 5. Python 检查
echo -n "Python: "
python --version

# 6. Node.js 检查
echo -n "Node.js: "
node --version

echo "================"
echo "✅ 检查完成"
```

---

**故障排除指南版本**: v2.0.5
**最后更新**: 2025-12-26
**维护状态**: ✅ 积极维护
