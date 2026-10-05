"""命令行：python3 cli.py "主题" """
import argparse
import json
import sys

from maker import make_outline, render_text


def main(argv=None):
    p = argparse.ArgumentParser(description="outline-maker-lite 文章大纲生成")
    p.add_argument("topic", nargs="?", help="文章主题")
    p.add_argument("--no-llm", action="store_true", help="强制只用规则")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    topic = args.topic or sys.stdin.read().strip()
    if not topic:
        print("错误：未提供主题", file=sys.stderr)
        return 2

    result = make_outline(topic, use_llm=not args.no_llm)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
