#!/bin/bash

# 部署脚本 - 将应用部署到 GitHub 和 Streamlit Cloud

echo "🚀 开始部署流程..."
echo ""

# 检查是否已初始化 git
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    echo "✅ Git 仓库初始化完成"
else
    echo "✅ Git 仓库已存在"
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📝 检测到未提交的更改："
    git status --short
    echo ""
    read -p "是否要提交这些更改？(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入提交信息: " commit_msg
        git add .
        git commit -m "${commit_msg:-Update files}"
        echo "✅ 更改已提交"
    fi
fi

# 检查远程仓库
if git remote | grep -q "origin"; then
    echo ""
    echo "✅ 远程仓库已配置"
    git remote -v
else
    echo ""
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请按照以下步骤操作："
    echo "1. 在 GitHub 上创建新仓库: https://github.com/new"
    echo "2. 复制仓库 URL（例如: https://github.com/username/repo-name.git）"
    echo ""
    read -p "请输入 GitHub 仓库 URL: " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ 远程仓库已添加: $repo_url"
    else
        echo "❌ 未提供仓库 URL，跳过远程配置"
    fi
fi

# 检查当前分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    echo ""
    read -p "当前分支是 '$current_branch'，是否要重命名为 'main'？(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -M main
        echo "✅ 分支已重命名为 main"
    fi
fi

# 推送到 GitHub
if git remote | grep -q "origin"; then
    echo ""
    read -p "是否要推送到 GitHub？(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 推送到 GitHub..."
        git push -u origin main 2>&1
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ 代码已成功推送到 GitHub！"
            echo ""
            echo "📋 下一步："
            echo "1. 访问 https://streamlit.io/cloud"
            echo "2. 使用 GitHub 账号登录"
            echo "3. 点击 'New app'"
            echo "4. 选择你的仓库和分支"
            echo "5. Main file path: app.py"
            echo "6. 点击 'Deploy'"
        else
            echo ""
            echo "❌ 推送失败，请检查："
            echo "   - GitHub 仓库 URL 是否正确"
            echo "   - 是否有推送权限"
            echo "   - 是否需要认证（Personal Access Token）"
        fi
    fi
fi

echo ""
echo "✨ 部署脚本执行完成！"
