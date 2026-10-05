"""outline-maker-lite — 文章大纲生成。

按主题规则展开层级提纲（一级章节 + 二级要点）。有 OPENAI_API_KEY 时可选 LLM 定制；
无 key 自动降级为规则模板。零第三方依赖（LLM 仅用 urllib）。
"""
from __future__ import annotations

import json
import os
import urllib.request

# 通用写作大纲骨架
SECTIONS = [
    ("引言与背景", ["为什么重要", "本文目标", "读者对象"]),
    ("核心概念", ["基本定义", "关键术语", "常见误区"]),
    ("方法与步骤", ["整体流程", "关键环节", "注意事项"]),
    ("应用场景", ["典型案例", "收益与价值"]),
    ("挑战与展望", ["现存问题", "未来趋势"]),
    ("总结", ["核心要点回顾", "延伸阅读"]),
]


def make_rule_outline(topic: str) -> list[dict]:
    """按主题填充层级提纲。"""
    outline = []
    for title, subs in SECTIONS:
        outline.append({
            "section": f"{title}：{topic}",
            "subsections": [f"{topic} · {s}" for s in subs],
        })
    return outline


def outline_with_llm(topic: str) -> list[dict] | None:
    """有 key 时调用 LLM 生成定制大纲；无 key/失败返回 None。"""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    prompt = (
        f"请为主题「{topic}」生成一份文章大纲，JSON 数组格式，"
        '每项 {"section": 章节名, "subsections": [要点...]}，共 5-6 章。只输出 JSON。'
    )
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是文章大纲规划助手。"},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 600,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return json.loads(content[content.find("["):content.rfind("]") + 1])
    except Exception:
        return None


def make_outline(topic: str, use_llm: bool = True) -> dict:
    """对外主接口。返回 {topic, source, outline}。"""
    if use_llm:
        llm_out = outline_with_llm(topic)
        if llm_out:
            return {"topic": topic, "source": "llm", "outline": llm_out}
    return {"topic": topic, "source": "rule", "outline": make_rule_outline(topic)}


def render_text(result: dict) -> str:
    lines = [f"# 《{result['topic']}》大纲（来源：{result['source']}）"]
    for i, sec in enumerate(result["outline"], 1):
        lines.append(f"{i}. {sec['section']}")
        for s in sec.get("subsections", []):
            lines.append(f"   - {s}")
    return "\n".join(lines)
