# Quickstart (labs & startups)

Get a board-ready offline report in under 15 minutes.

## 1. Install

```bash
git clone https://github.com/Hamzakhan7473/sentinelbench.git
cd sentinelbench
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Validate scenarios

```bash
sentinelbench validate --also-example
```

## 3. Run the seed pack (no API keys)

```bash
sentinelbench run --provider mock --mode oracle
```

Reports land in `results/` (JSON + Markdown).

## 4. See a failure contrast (demo)

```bash
sentinelbench run --provider mock --mode empty --output results/demo-empty.json
```

Open the `.md` beside the JSON for failure examples.

## 5. Live provider (optional)

```bash
cp .env.example .env
# set OPENAI_API_KEY when the OpenAI adapter is available
sentinelbench run --provider openai
```

## What to read next

- [Product vision](product-vision.md)  
- [Roadmap](roadmap.md)  
- [Methodology / rubric](methodology.md)  
- [Scenario guidelines](../data/README.md)  
- [Security / publishing](../SECURITY.md)  
