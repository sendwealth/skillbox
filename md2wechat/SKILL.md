---
name: md2wechat
description: 将 Markdown 文本转化为微信公众号排版，输出可直接粘贴到微信编辑器的 HTML
tags: [wechat, markdown, formatting]
---

# Markdown 转微信公众号排版

将任意 Markdown 文本转换为微信公众号兼容的内联样式 HTML，可直接粘贴到微信编辑器使用。

## 触发条件

用户说：公众号排版、微信排版、md转微信、wechat format、公众号文章格式化 等。

## 使用方式

```bash
python3 ~/.hermes/skills/md2wechat/scripts/md2wechat.py input.md
```

输出为 HTML 文件（同目录 input.html），浏览器打开后全选复制，粘贴到微信公众号编辑器即可。

也支持 stdin：
```bash
echo "# 标题" | python3 ~/.hermes/skills/md2wechat/scripts/md2wechat.py -
```

## 排版风格

- 主色调：科技蓝 #1a73e8，强调色 #e8f0fe
- 字体：-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- 正文 15px，行高 1.8，段间距 16px
- 标题带左侧色条装饰
- 引用块带浅蓝背景 + 左边框
- 代码块深色背景，等宽字体
- 图片自适应宽度，圆角 8px
- 表格斑马纹 + 圆角
- 链接文字蓝色加粗（微信不支持跳转，但视觉可区分）
- 列表缩进清晰，有序/无序均有自定义标记

## 设计原则

1. 全部内联样式（微信编辑器会剥离 <style> 标签）
2. 不使用 class（微信编辑器不支持外部 CSS）
3. 不使用 Flexbox / Grid（兼容性差）
4. 图片 max-width: 100%（适配手机）
5. 段落用 <section> 包裹（微信编辑器常见结构）
6. 代码块中特殊字符转义

## 技术实现

脚本位于 scripts/md2wechat.py，依赖：
- Python 3 标准库（re, html, sys）
- markdown 库（pip install markdown）
- 无其他第三方依赖

核心流程：
1. 读取 Markdown 文本
2. 用 markdown 库解析为 HTML AST
3. Post-process：注入内联样式、替换 HTML 结构
4. 包装在微信兼容的容器 div 中
5. 输出完整 HTML 文件
