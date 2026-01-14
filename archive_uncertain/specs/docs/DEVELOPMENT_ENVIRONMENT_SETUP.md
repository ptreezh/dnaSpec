# DNASPEC智能架构师项目开发环境配置

## 环境要求

### Python环境
- Python 3.8+
- 虚拟环境管理: venv 或 conda
- 依赖管理: pip

### 开发工具
- 代码编辑器: VS Code 或 PyCharm
- 版本控制: Git
- 测试框架: pytest
- 代码质量: pylint, black, isort

### Claude Skills相关
- Claude Code环境
- Skills开发工具
- Markdown编辑器

## 依赖包列表

### 核心依赖
```txt
# 核心框架
click>=8.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# 测试框架
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.0.0

# 代码质量
pylint>=2.17.0
black>=23.0.0
isort>=5.12.0

# 文档处理
pandoc>=2.3.0
markdown>=3.4.0

# YAML处理
PyYAML>=6.0.0

# 日志处理
loguru>=0.7.0

# 数据处理
pandas>=2.0.0
numpy>=1.24.0
</`

### 开发依赖
```txt
# 开发工具
ipython>=8.0.0
jupyter>=1.0.0
pre-commit>=3.0.0

# 调试工具
pdbpp>=0.10.0
memory-profiler>=0.61.0

# 性能分析
pytest-benchmark>=4.0.0
line-profiler>=4.0.0
</`

## 环境配置步骤

### 1. 创建虚拟环境
```bash
# 使用venv
python -m venv dnaspec-env
source dnaspec-env/bin/activate  # Linux/Mac
# 或
dnaspec-env\Scripts\activate      # Windows

# 使用conda
conda create -n dnaspec-env python=3.9
conda activate dnaspec-env
```

### 2. 安装依赖
```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装可选依赖
pip install -r requirements-optional.txt
```

### 3. 配置开发工具
```bash
# 配置pre-commit钩子
pre-commit install

# 配置pytest
pytest --version

# 验证环境
python -c "import pytest; print(pytest.__version__)"
```

## 项目结构初始化

### 创建基础目录结构
```bash
mkdir -p src/dnaspec_architect
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p docs
mkdir -p config
```

### 创建基础文件
```bash
touch src/dnaspec_architect/__init__.py
touch src/dnaspec_architect/main.py
touch tests/__init__.py
touch requirements.txt
touch requirements-dev.txt
touch .gitignore
touch README.md
```

## 测试环境配置

### pytest配置
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_functions = test_*
addopts = 
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --strict-markers
markers =
    unit: unit tests
    integration: integration tests
    slow: slow tests
```

### 代码质量配置

#### pylint配置
```ini
[MASTER]
load-plugins=pylint.extensions.docparams

[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-few-public-methods,
    too-many-arguments,
    too-many-locals

[DESIGN]
max-args=10
max-locals=20
max-returns=6
max-branches=20
max-statements=100
```

#### black配置
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

## 环境验证

### 1. 基础验证
```bash
# 验证Python版本
python --version

# 验证核心包
python -c "import click, pydantic, pytest; print('Environment OK')"
```

### 2. 测试验证
```bash
# 运行简单测试
pytest --version
```

### 3. 代码质量验证
```bash
# 验证代码格式化工具
black --version
isort --version
pylint --version
```

## 持续集成配置

### GitHub Actions配置
```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## 开发工作流

### 1. 日常开发流程
```bash
# 1. 激活环境
source dnaspec-env/bin/activate

# 2. 拉取最新代码
git pull origin main

# 3. 运行测试
pytest tests/

# 4. 编写代码
# ...

# 5. 格式化代码
black src/ tests/
isort src/ tests/

# 6. 代码检查
pylint src/

# 7. 提交代码
git add .
git commit -m "feat: implement new feature"
git push origin main
```

### 2. 测试驱动开发流程
```bash
# 1. 编写测试
# tests/unit/test_new_feature.py

# 2. 运行测试（应该失败）
pytest tests/unit/test_new_feature.py

# 3. 编写实现代码
# src/dnaspec_architect/new_feature.py

# 4. 运行测试（应该通过）
pytest tests/unit/test_new_feature.py

# 5. 重构优化
# 优化代码结构和性能

# 6. 再次运行测试确保功能正常
pytest tests/unit/test_new_feature.py
```

## 环境维护

### 依赖更新
```bash
# 更新依赖
pip list --outdated
pip install --upgrade package_name

# 冻结依赖
pip freeze > requirements.txt
```

### 环境重建
```bash
# 删除旧环境
deactivate
rm -rf dnaspec-env

# 重新创建环境
python -m venv dnaspec-env
source dnaspec-env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 故障排除

### 常见问题解决

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install --no-cache-dir package_name
   ```

2. **测试环境问题**
   ```bash
   python -m pytest tests/
   ```

3. **代码格式化问题**
   ```bash
   black --check src/
   isort --check-only src/
   ```

4. **环境变量问题**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

这个开发环境配置确保了项目的可重现性和一致性，为TDD驱动的开发提供了坚实的基础。