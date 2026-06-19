import json
import sys
from datetime import datetime

# Built-in site metadata
SITE_DATA = {
    "title": "雷速体育",
    "url": "https://cn-cns-leisu.com",
    "tags": ["体育资讯", "比分直播", "赛事数据", "雷速"],
    "keywords": ["雷速", "体育", "比分", "直播", "数据"],
    "description": "提供全球体育赛事即时比分、数据分析和新闻资讯的综合平台。",
    "language": "zh-CN",
    "category": "Sports",
}

def safe_print_json(data):
    """Output structured JSON safely."""
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        return f'{{"error": "Serialization failed: {str(e)}"}}'

def build_summary(site):
    """Build a structured summary dictionary from site data."""
    required_keys = ["title", "url", "tags", "keywords", "description"]
    for key in required_keys:
        if key not in site:
            raise KeyError(f"Missing required key: {key}")

    summary = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": site["url"],
        "site_name": site["title"],
        "keywords": list(set(site.get("keywords", []))),
        "tags": sorted(site.get("tags", [])),
        "url": site["url"],
        "description": site["description"].strip(),
        "language": site.get("language", "unknown"),
        "category": site.get("category", "general"),
    }
    return summary

def format_as_text(summary):
    """Convert summary dict to human-readable text block."""
    lines = []
    lines.append(f"站点名称: {summary['site_name']}")
    lines.append(f"URL: {summary['url']}")
    lines.append(f"关键词: {', '.join(summary['keywords'])}")
    lines.append(f"标签: {', '.join(summary['tags'])}")
    lines.append(f"简介: {summary['description']}")
    lines.append(f"语言: {summary['language']}")
    lines.append(f"类别: {summary['category']}")
    lines.append(f"生成时间: {summary['generated_at']}")
    return "\n".join(lines)

def format_as_markdown(summary):
    """Convert summary dict to markdown block."""
    md = f"## {summary['site_name']}\n\n"
    md += f"- **URL**: [{summary['url']}]({summary['url']})\n"
    md += f"- **关键词**: `{'`, `'.join(summary['keywords'])}`\n"
    md += f"- **标签**: {', '.join(f'`{t}`' for t in summary['tags'])}\n"
    md += f"- **简介**: {summary['description']}\n"
    md += f"- **语言**: {summary['language']}\n"
    md += f"- **类别**: {summary['category']}\n"
    md += f"- **生成时间**: {summary['generated_at']}\n"
    return md

def format_as_html(summary):
    """Convert summary dict to HTML fragment (safe escaping)."""
    site_name = summary["site_name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    url = summary["url"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    keywords = ", ".join(summary["keywords"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    tags = ", ".join(summary["tags"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    description = summary["description"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lang = summary["language"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    category = summary["category"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    gen_time = summary["generated_at"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    html = f"<div class='site-summary'>\n"
    html += f"  <h2>{site_name}</h2>\n"
    html += f"  <p><strong>URL:</strong> <a href='{url}'>{url}</a></p>\n"
    html += f"  <p><strong>关键词:</strong> {keywords}</p>\n"
    html += f"  <p><strong>标签:</strong> {tags}</p>\n"
    html += f"  <p><strong>简介:</strong> {description}</p>\n"
    html += f"  <p><strong>语言:</strong> {lang}</p>\n"
    html += f"  <p><strong>类别:</strong> {category}</p>\n"
    html += f"  <p><strong>生成时间:</strong> {gen_time}</p>\n"
    html += f"</div>\n"
    return html

def main():
    # Determine output format
    if len(sys.argv) > 1:
        fmt = sys.argv[1].lower()
    else:
        fmt = "text"

    try:
        summary = build_summary(SITE_DATA)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if fmt == "json":
        output = safe_print_json(summary)
    elif fmt == "markdown":
        output = format_as_markdown(summary)
    elif fmt == "html":
        output = format_as_html(summary)
    elif fmt == "text":
        output = format_as_text(summary)
    else:
        print(f"Unsupported format: {fmt}", file=sys.stderr)
        sys.exit(1)

    print(output)

if __name__ == "__main__":
    main()