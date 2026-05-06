# 飞书/一堂文档抓取技术

## 场景
一堂（yitang.top）的飞书文档需要微信扫码登录，且页面使用虚拟滚动（类似飞书文档），DOM 只渲染可见区域内容。

## 完整流程

### 1. 登录
飞书/一堂使用微信 OAuth QR 码登录。流程：
- 导航到目标 URL，页面重定向到 SSO 登录页
- 登录页加载 `open.weixin.qq.com/connect/qrconnect` iframe
- 截图分享给用户扫码
- 脚本中 `waitForURL` 等待离开 login/sso 页面（timeout 120s）

### 2. 内容抓取（虚拟滚动）
页面 scrollHeight 很大（~153K px），但 innerText 很小（~2-3K 字）→ 虚拟滚动。

**有效方法**：慢速滚动 + 逐帧累积文本
```javascript
const allText = new Set();
for (let y = 0; y < 60000; y += 200) {
  await page.evaluate(pos => window.scrollTo(0, pos), y);
  await page.waitForTimeout(100);
  const text = await page.evaluate(() => {
    const clone = document.body.cloneNode(true);
    clone.querySelectorAll('script, style, noscript, iframe').forEach(el => el.remove());
    return clone.innerText;
  });
  text.split('\n').filter(l => l.trim()).forEach(l => allText.add(l.trim()));
}
```

**陷阱**：虚拟滚动会导致重复内容（目录在每个滚动位置都渲染），使用 Set 去重。

### 3. Playwright 脚本模板
见 `/Users/rowan/Projects/truthverifier/scraper-v3.js`

关键参数：
- viewport: 1440x900
- 滚动步长: 200px
- 每步等待: 100ms
- 最大滚动距离: 60000px
- 用户扫码等待: 120s timeout

### 4. 验证
- 文档总字数标注在页面底部（如 "文档字数：42643"）
- 抓取后对比字数是否接近
