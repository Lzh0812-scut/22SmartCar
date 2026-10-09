#!/bin/bash
FAIL=0
echo "🔍 开始模拟 M0-1 环境检测 (Ubuntu 22.04 + ROS2 Humble)..."

# 1. Ubuntu 版本
if grep -q "22.04" /etc/os-release; then echo "✅ Ubuntu 22.04"; else echo "❌ 非 22.04"; FAIL=$((FAIL+1)); fi

# 2. ROS2 Humble (检测环境变量)
if [ -n "$ROS_DISTRO" ] && [ "$ROS_DISTRO" = "humble" ]; then echo "✅ ROS2 Humble"; else echo "⚠️ ROS2 Humble 未激活(需 source 或安装)"; FAIL=$((FAIL+1)); fi

# 3. Python 虚拟环境 (conda 或 uv)
if command -v conda &> /dev/null || command -v uv &> /dev/null; then echo "✅ Python 虚拟环境工具"; else echo "❌ 无 conda/uv"; FAIL=$((FAIL+1)); fi

# 4. C/C++ 工具链
for cmd in gcc g++ make cmake; do
  if ! command -v $cmd &> /dev/null; then echo "❌ 缺 $cmd"; FAIL=$((FAIL+1)); else echo "✅ $cmd"; fi
done

# 5. 编辑器 (VS Code)
if command -v code &> /dev/null; then echo "✅ VS Code"; else echo "⚠️ VS Code 未装(终端无 code 命令)"; fi

# 6. Git 配置
if git config --global user.name &> /dev/null && git config --global user.email &> /dev/null; then echo "✅ Git 已配置"; else echo "❌ Git 未配 name/email"; FAIL=$((FAIL+1)); fi

# 7. 网络/SSH (结合你之前的坑)
if command -v ssh &> /dev/null; then echo "✅ ssh 可用"; else echo "❌ 缺 ssh"; FAIL=$((FAIL+1)); fi

echo "---------------------------------"
echo "检测结束，FAIL=$FAIL (目标: FAIL=0)"
exit $FAIL
