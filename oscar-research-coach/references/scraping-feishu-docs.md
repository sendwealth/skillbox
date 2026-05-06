# Scraping 飞书/一堂 Documents with Playwright

Session from 2026-05-04: extracting a 42,643-char course document from yitang.top/fs-doc (飞书文档).

## Problem

飞书-style documents use virtual scrolling — the DOM only renders visible content. `innerText` captures only what's in the viewport. Large `scrollHeight` (150K+ px) but small text capture.

## Solution: Slow-Scroll Accumulation

```javascript
const { chromium } = require('playwright');

const page = await (await chromium.launch({ headless: false }))
  .newContext({ viewport: { width: 1440, height: 900 } })
  .newPage();

// Handle WeChat QR login
await page.goto(DOC_URL, { waitUntil: 'networkidle', timeout: 30000 });
if (page.url().includes('login') || page.url().includes('sso')) {
  console.log('📱 Scan the QR code with WeChat...');
  await page.waitForURL(url => !url.includes('login') && !url.includes('sso'), { timeout: 120000 });
  await page.waitForTimeout(5000);
}

// Slow-scroll with Set-based text accumulation to handle virtual DOM
const allText = new Set();
for (let y = 0; y < 60000; y += 200) {
  await page.evaluate(pos => window.scrollTo(0, pos), y);
  await page.waitForTimeout(100);

  const visibleText = await page.evaluate(() => {
    const clone = document.body.cloneNode(true);
    clone.querySelectorAll('script, style, noscript, iframe').forEach(el => el.remove());
    return clone.innerText;
  });

  visibleText.split('\n').filter(l => l.trim()).forEach(l => allText.add(l.trim()));
}

const finalText = Array.from(allText).join('\n');
```

## Key Pitfalls

1. **Use a Set for text**: Virtual DOM unloads and re-renders the same content as you scroll. A Set deduplicates naturally.

2. **Scroll step size**: 200px steps with 100ms waits worked. Larger steps (800px+) miss content because the virtual DOM unloads before capture.

3. **WeChat QR login**: Browser must be headed so user can scan. After scanning, page auto-redirects from login → content.

4. **Detection of "loaded"**: Stop when consecutive scrolls yield no new text (3-5 empty scrolls).

5. **Avoid fullPage screenshots**: On virtual-scroll pages, produces blank output.

## Alternative: Position Screenshots

```javascript
const positions = [0, 3000, 6000, 9000, 12000, 15000, 18000, 21000, 24000];
for (const pos of positions) {
  await page.evaluate(y => window.scrollTo(0, y), pos);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `pos-${pos}.png` });
}
```
