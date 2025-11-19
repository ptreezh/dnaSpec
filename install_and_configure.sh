#!/bin/bash
# DSGS Context Engineering Skills - 一键安装和配置脚本 (Linux/Mac版本)
# 自动处理环境依赖安装和CLI工具自动配置

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              DSGS Context Engineering Skills                  ║"
echo "║                   一键安装配置脚本                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到python3。请先安装Python 3.8或更高版本。"
    exit 1
fi

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未找到git。请先安装Git。"
    exit 1
fi

echo "✅ 检测到Python3和Git"
echo

# 检查pip是否安装
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ 错误: 未找到pip。"
    exit 1
fi

# 克隆项目或更新现有项目
if [ -d "dnaSpec" ]; then
    echo "🔄 更新现有项目..."
    cd dnaSpec
    git pull
else
    echo "📦 克隆项目..."
    git clone https://github.com/ptreezh/dnaSpec.git
    cd dnaSpec
fi

echo
echo "🛠️  安装依赖和DSGS包..."
python3 -m pip install -e .

if [ $? -ne 0 ]; then
    echo "❌ 安装失败"
    exit 1
fi

echo
echo "🚀 运行自动配置..."
python3 run_auto_config.py

echo
echo "✅ 安装和配置完成！"
echo
echo "现在您可以在AI CLI工具中使用以下命令："
echo "  /speckit.dsgs.context-analysis [上下文] - 分析上下文质量"
echo "  /speckit.dsgs.context-optimization [上下文] - 优化上下文"
echo "  /speckit.dsgs.cognitive-template [任务] - 应用认知模板"
echo "  ...以及其他DSGS技能"