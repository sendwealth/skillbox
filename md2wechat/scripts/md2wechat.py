#!/usr/bin/env python3
"""
Markdown → 微信公众号排版 HTML
用法: python3 md2wechat.py input.md        # 输出 input.html
      python3 md2wechat.py -               # 从 stdin 读取
"""

import re
import html as html_mod
import sys
import os

try:
    import markdown
except ImportError:
    print("需要安装 markdown: pip3 install markdown", file=sys.stderr)
    sys.exit(1)


# ── 样式常量 ──────────────────────────────────────────────

FONT_FAMILY = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
MONO_FONT = 'Menlo, Monaco, Consolas, "Courier New", monospace'

CONTAINER = (
    'max-width:100%;margin:0 auto;padding:16px 10px;'
    'font-family:{font};color:#333;word-break:break-word;'
).format(font=FONT_FAMILY)

STYLES = {
    'h1': (
        'font-size:22px;font-weight:bold;color:#1a1a1a;'
        'text-align:center;margin:32px 0 20px 0;padding:0 10px;'
        'border-bottom:2px solid #1a73e8;padding-bottom:10px;'
    ),
    'h2': (
        'font-size:19px;font-weight:bold;color:#1a1a1a;'
        'margin:28px 0 16px 0;padding:8px 12px;'
        'border-left:4px solid #1a73e8;background:#f8f9fa;'
    ),
    'h3': (
        'font-size:17px;font-weight:bold;color:#333;'
        'margin:24px 0 12px 0;padding-left:12px;'
        'border-left:3px solid #5b9bd5;'
    ),
    'h4': (
        'font-size:16px;font-weight:bold;color:#444;'
        'margin:20px 0 10px 0;'
    ),
    'p': (
        'font-size:15px;line-height:1.8;color:#333;'
        'margin:0 0 16px 0;letter-spacing:0.5px;'
    ),
    'strong': (
        'font-weight:bold;color:#1a1a1a;'
    ),
    'em': (
        'font-style:italic;color:#555;'
    ),
    'a': (
        'color:#1a73e8;font-weight:bold;'
        'text-decoration:none;border-bottom:1px solid #1a73e8;'
    ),
    'blockquote': (
        'margin:16px 0;padding:12px 16px;'
        'background:#e8f0fe;border-left:4px solid #1a73e8;'
        'border-radius:0 8px 8px 0;'
    ),
    'blockquote_p': (
        'font-size:14px;line-height:1.8;color:#444;'
        'margin:0;'
    ),
    'ul': (
        'margin:12px 0 16px 0;padding-left:20px;'
        'list-style:none;'
    ),
    'ol': (
        'margin:12px 0 16px 0;padding-left:20px;'
        'list-style:none;counter-reset:wechat-ol;'
    ),
    'li': (
        'font-size:15px;line-height:1.8;color:#333;'
        'margin:6px 0;position:relative;padding-left:4px;'
    ),
    'li_ul': (
        'list-style:circle;margin:4px 0;padding-left:16px;'
    ),
    'code_inline': (
        'font-family:{mono};font-size:13px;'
        'background:#f0f0f0;padding:2px 6px;'
        'border-radius:3px;color:#d63384;'
    ).format(mono=MONO_FONT),
    'code_block': (
        'font-family:{mono};font-size:13px;line-height:1.6;'
        'background:#1e1e1e;color:#d4d4d4;'
        'padding:16px;margin:16px 0;'
        'border-radius:8px;overflow-x:auto;'
        'white-space:pre-wrap;word-break:break-all;'
    ).format(mono=MONO_FONT),
    'pre': (
        'margin:0;background:#1e1e1e;border-radius:8px;'
        'overflow:hidden;'
    ),
    'img': (
        'max-width:100%;border-radius:8px;'
        'margin:16px auto;display:block;'
    ),
    'table': (
        'width:100%;border-collapse:collapse;'
        'margin:16px 0;font-size:14px;'
    ),
    'th': (
        'background:#1a73e8;color:#fff;'
        'font-weight:bold;padding:10px 12px;'
        'text-align:left;border:1px solid #1565c0;'
    ),
    'td': (
        'padding:10px 12px;border:1px solid #ddd;'
    ),
    'tr_even': (
        'background:#f8f9fa;'
    ),
    'hr': (
        'border:none;border-top:1px solid #e0e0e0;'
        'margin:24px 0;'
    ),
    'footnote': (
        'font-size:12px;color:#999;text-align:center;'
        'margin:24px 0 0 0;padding-top:16px;'
        'border-top:1px solid #eee;'
    ),
}


# ── Markdown → HTML ──────────────────────────────────────

def md_to_html(text: str) -> str:
    """用 markdown 库解析，保留原始 HTML"""
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    return md.convert(text)


# ── 内联样式注入 ─────────────────────────────────────────

def style_tag(tag: str, content: str, **extra) -> str:
    s = STYLES.get(tag, '')
    for k, v in extra.items():
        s += f'{k}:{v};'
    return f'<{tag} style="{s}">{content}</{tag}>'


def process(html: str) -> str:
    """递归注入内联样式"""
    out = html

    # ── 代码块 <pre><code> → 带样式的 <section><pre><code> ──
    # 移除 markdown 库生成的 id 属性（微信不需要）
    out = re.sub(r'(<h\d)\s+id="[^"]*"', r'\1', out)

    out = re.sub(
        r'<pre><code(?:\s+class="language-(\w+)")?>(.*?)</code></pre>',
        _repl_code_block,
        out,
        flags=re.DOTALL,
    )

    # ── 行内代码 ──
    out = re.sub(
        r'<code>(.*?)</code>',
        lambda m: f'<code style="{STYLES["code_inline"]}">{m.group(1)}</code>',
        out,
    )

    # ── 图片 ──
    out = re.sub(
        r'<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*/?>',
        lambda m: f'<img src="{m.group(1)}" style="{STYLES["img"]}" '
                  f'alt="{m.group(2) or ""}" />',
        out,
    )

    # ── 链接 ──
    out = re.sub(
        r'<a\s+href="([^"]+)">(.*?)</a>',
        lambda m: f'<a href="{m.group(1)}" style="{STYLES["a"]}">{m.group(2)}</a>',
        out,
    )

    # ── 加粗 / 斜体 ──
    out = re.sub(
        r'<strong>(.*?)</strong>',
        lambda m: f'<strong style="{STYLES["strong"]}">{m.group(1)}</strong>',
        out,
    )
    out = re.sub(
        r'<em>(.*?)</em>',
        lambda m: f'<em style="{STYLES["em"]}">{m.group(1)}</em>',
        out,
    )
    out = re.sub(
        r'<b>(.*?)</b>',
        lambda m: f'<strong style="{STYLES["strong"]}">{m.group(1)}</strong>',
        out,
    )
    out = re.sub(
        r'<i>(.*?)</i>',
        lambda m: f'<em style="{STYLES["em"]}">{m.group(1)}</em>',
        out,
    )

    # ── 标题 ──
    for level in range(1, 5):
        tag = f'h{level}'
        pattern = re.compile(
            rf'<{tag}>(.*?)</{tag}>',
            re.DOTALL,
        )
        out = pattern.sub(
            lambda m, t=tag: f'<{t} style="{STYLES[t]}">{m.group(1)}</{t}>',
            out,
        )

    # ── 段落 ──
    out = re.sub(
        r'<p>(.*?)</p>',
        lambda m: f'<section style="margin:0 0 16px 0;"><p style="{STYLES["p"]}">{m.group(1)}</p></section>',
        out,
        flags=re.DOTALL,
    )

    # ── 引用块 ──
    out = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        _repl_blockquote,
        out,
        flags=re.DOTALL,
    )

    # ── 无序列表 ──
    out = re.sub(
        r'<ul>(.*?)</ul>',
        _repl_ul,
        out,
        flags=re.DOTALL,
    )

    # ── 有序列表 ──
    out = re.sub(
        r'<ol>(.*?)</ol>',
        _repl_ol,
        out,
        flags=re.DOTALL,
    )

    # ── 表格 ──
    out = _process_table(out)

    # ── 分隔线 ──
    out = re.sub(
        r'<hr\s*/?>',
        f'<hr style="{STYLES["hr"]}" />',
        out,
    )

    return out


def _repl_code_block(m) -> str:
    lang = m.group(1) or ''
    code = m.group(2)
    # 保留 HTML 实体，不额外转义（markdown 库已处理）
    return (
        f'<section style="margin:16px 0;border-radius:8px;overflow:hidden;">'
        f'<pre style="{STYLES["pre"]}">'
        f'<code style="{STYLES["code_block"]}">{code}</code>'
        f'</pre></section>'
    )


def _repl_blockquote(m) -> str:
    content = m.group(1)
    # 替换内部 <p> 标签样式，去掉多余 section 包裹
    content = re.sub(
        r'<section[^>]*>\s*<p[^>]*>(.*?)</p>\s*</section>',
        lambda p: f'<p style="{STYLES["blockquote_p"]}">{p.group(1)}</p>',
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r'<p[^>]*>(.*?)</p>',
        lambda p: f'<p style="{STYLES["blockquote_p"]}">{p.group(1)}</p>',
        content,
        flags=re.DOTALL,
    )
    return f'<blockquote style="{STYLES["blockquote"]}">{content}</blockquote>'


def _repl_ul(m) -> str:
    items = m.group(1)
    items = re.sub(
        r'<li>(.*?)</li>',
        lambda li: (
            f'<li style="{STYLES["li"]}">'
            f'<span style="color:#1a73e8;margin-right:8px;">&#8226;</span>'
            f'{li.group(1)}</li>'
        ),
        items,
        flags=re.DOTALL,
    )
    return f'<ul style="{STYLES["ul"]}">{items}</ul>'


def _repl_ol(m) -> str:
    items = m.group(1)
    counter = [0]

    def repl_li(li):
        counter[0] += 1
        num = counter[0]
        return (
            f'<li style="{STYLES["li"]}">'
            f'<span style="color:#1a73e8;font-weight:bold;margin-right:8px;">'
            f'{num}.</span>{li.group(1)}</li>'
        )

    items = re.sub(r'<li>(.*?)</li>', repl_li, items, flags=re.DOTALL)
    return f'<ol style="{STYLES["ol"]}">{items}</ol>'


def _process_table(html: str) -> str:
    """处理表格，注入样式 + 斑马纹"""
    if '<table' not in html:
        return html

    def repl_table(m):
        table_html = m.group(0)
        # 给 table 加样式
        table_html = re.sub(
            r'<table>',
            f'<table style="{STYLES["table"]}">',
            table_html,
        )
        # th
        table_html = re.sub(
            r'<th>(.*?)</th>',
            lambda t: f'<th style="{STYLES["th"]}">{t.group(1)}</th>',
            table_html,
            flags=re.DOTALL,
        )
        # td
        table_html = re.sub(
            r'<td>(.*?)</td>',
            lambda t: f'<td style="{STYLES["td"]}">{t.group(1)}</td>',
            table_html,
            flags=re.DOTALL,
        )
        # 斑马纹：偶数行加背景
        rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        new_table = table_html
        for i, row in enumerate(rows):
            if i > 0 and i % 2 == 0:
                styled_row = (
                    f'<tr style="{STYLES["tr_even"]}">'
                    f'{row}</tr>'
                )
                new_table = new_table.replace(
                    f'<tr>{row}</tr>',
                    styled_row,
                    1,
                )
        return new_table

    return re.sub(
        r'<table>.*?</table>',
        repl_table,
        html,
        flags=re.DOTALL,
    )


# ── 生成完整 HTML ─────────────────────────────────────────

def wrap_html(body: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>微信公众号文章</title>
</head>
<body style="margin:0;padding:0;background:#fff;">
<div style="{CONTAINER}">
{body}
</div>
</body>
</html>'''


# ── 主入口 ────────────────────────────────────────────────

def convert(md_text: str) -> str:
    raw_html = md_to_html(md_text)
    styled = process(raw_html)
    return wrap_html(styled)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 md2wechat.py <input.md>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    if input_path == '-':
        md_text = sys.stdin.read()
        out_path = None
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        out_path = os.path.splitext(input_path)[0] + '.html'

    result = convert(md_text)

    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✅ 输出: {out_path}")
    else:
        print(result)


if __name__ == '__main__':
    main()
