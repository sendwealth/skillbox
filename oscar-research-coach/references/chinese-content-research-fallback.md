# Chinese Content Research Fallback Strategy

## Problem

When researching topics related to the Chinese internet ecosystem (WeChat Official Accounts, Zhihu, Jike, Sogou WeChat Search, etc.), essentially all search and content channels are blocked from this environment:

| Channel | What Happens | 
|---------|-------------|
| Google | Empty response or CAPTCHA |
| Bing | Returns irrelevant results (often Japanese content) |
| DuckDuckGo / Startpage / SearXNG | Block or return empty |
| Sogou WeChat Search (weixin.sogou.com) | Anti-spider page |
| Zhihu Search | Empty page (JS-rendered) |
| WeChat MP articles (mp.weixin.qq.com) | CAPTCHA wall |
| wemp.app / sgly.com (WeChat aggregators) | Connection closed |
| niaogebiji.com | Connection closed |
| woshipm.com search | 404 or JS-dependent |
| Subagents | Timeout after 600s with 25+ failed API calls |

## Proven Fallback Strategy

When research touches Chinese content ecosystems and tools fail (confirm within 3-4 attempts, not 25):

### 1. Switch to Knowledge-Driven Mode
Use the AI's training knowledge combined with:
- Structured analysis frameworks (JTBD, Product Kernel, Growth Flywheel, etc.)
- User-provided context (specific account names, pain points, goals)
- Competitive analysis patterns (competitor quadrants, positioning matrices)
- Domain knowledge about platform mechanics (e.g., WeChat Official Account's subscription model, social distribution via Moments, Sogou SEO factors)

### 2. Compile, Don't Scrape
Instead of trying to verify every fact via live search:
- Build the report from framework-driven reasoning
- Label every conclusion with confidence level:
  - ✅ 事实 (Fact) — verified or widely established
  - 💬 观点 (Opinion) — from user/expert statements
  - ❓ 推测 (Inference) — logically derived but unverified
- Include a "需用户自行验证" (needs user verification) section at the end

### 3. Structure the Output
Use the OSCAR report template, but acknowledge the limitation upfront:
- State clearly that live search was attempted and blocked
- Explain that the analysis is framework-driven
- List specific items the user should cross-verify themselves

### 4. Effective for These Research Types
This fallback works best for:
- **设计题** (Design questions) — best practices, methodology, frameworks
- **解答题** (Hypothesis validation) — when reasoning from first principles suffices
- **竞对跟踪** (Competitor tracking) — partial, needs user verification

It works less well for:
- Pure data questions (market size, revenue figures) — these need live sources
- Real-time monitoring (latest competitor moves) — need live access

## Example: WeChat Content Strategy Research

A session researching WeChat Official Account content quality for a tech/AI account ("数字冲浪") succeeded with this approach:
- 5-10 minutes of tool attempts → all blocked
- ~20 minutes of framework-driven compilation
- Output: 19,000-word structured report with JTBD analysis, competitor pattern analysis, content SOP, growth timeline, and confidence labels
- User received actionable next steps plus a verification checklist

The key insight: for design questions about Chinese content ecosystems, framework-driven reasoning produces reports that are 80%+ as useful as live-researched ones, without the 25+ failed API calls.
