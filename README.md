# outline-maker-lite

文章大纲生成小工具。按主题规则展开层级提纲（一级章节 + 二级要点）；配置 key 时可选 LLM 定制。

## 功能

- 内置 6 段式通用写作骨架（引言/概念/方法/应用/挑战/总结）；
- 主题自动填充到每个章节与要点；
- 输出可读层级文本或 JSON；
- 配置 `OPENAI_API_KEY` 时调用 LLM 生成定制大纲；
- **无 key 自动降级为规则模板**。

## 快速开始

```bash
python3 cli.py "人工智能入门"
```

## 使用示例

```bash
# 强制只用规则
python3 cli.py "咖啡品鉴" --no-llm

# JSON 输出
python3 cli.py "机器学习" --json
```

## 有 API Key 时启用 LLM

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选
export OPENAI_MODEL="gpt-3.5-turbo"                 # 可选
python3 cli.py "量子计算"
```

## 无 API Key 如何运行

不设置任何环境变量直接运行，自动使用规则模板展开大纲，输出标注来源为 `rule`。

## 目录结构

```
outline-maker-lite/
├── maker.py      # 大纲骨架、规则填充、可选 LLM、渲染
├── cli.py        # 命令行入口
├── tests/
│   └── test_maker.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
