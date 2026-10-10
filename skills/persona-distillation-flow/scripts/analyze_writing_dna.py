#!/usr/bin/env python3
"""
analyze_writing_dna.py
写作 DNA 语言特征量化分析工具 (Writing DNA Quantitative Analyzer)

功能：
1. 自动读取文本文件或语料目录（.txt / .md）。
2. 统计句长分布（平均句长、短句 <=15字占比、长句 >=50字占比）。
3. 统计标点符号使用频率与比例（破折号、省略号、叹号、引号等）。
4. 统计段落特征（段落平均句数、单句成段比例）。
5. 提取高频词与过度使用的副词噪声。
6. 输出结构化 Markdown 与 JSON 报告，为 L1 语言 DNA 提供刚性物理指标。

用法：
    python3 analyze_writing_dna.py <file_or_dir> [-o output.md] [--json]

示例：
    python3 ./skills/persona-distillation-flow/scripts/analyze_writing_dna.py /path/to/novel.txt -o language-dna-stats.md
"""

import sys
import os
import re
import argparse
import json
from collections import Counter

# 常见副词列表（用于检测过度使用的副词噪声）
COMMON_ADVERBS = [
    "非常", "十分", "极其", "极其", "格外", "相当", "格外", "极其",
    "几乎", "简直", "大致", "大抵", "大约", "似乎", "仿佛", "隐约",
    "忽然", "突然", "骤然", "猛然", "决然", "断然", "毅然", "赫然",
    "竟然", "居然", "偏偏", "明明", "分明", "分外", "格外", "固然",
    "其实", "实在", "委实", "着实", "诚然", "果真", "果然", "未免",
    "顿时", "刹那", "转瞬", "旋即", "随即", "立时", "当下", "登时"
]

def clean_text(text: str) -> str:
    """清理多余空行与控制字符"""
    return text.replace('\r\n', '\n').replace('\r', '\n')

def split_into_paragraphs(text: str) -> list[str]:
    """拆分为非空段落列表"""
    lines = clean_text(text).split('\n')
    return [line.strip() for line in lines if line.strip()]

def split_into_sentences(text: str) -> list[str]:
    """拆分为句子列表（按句号、问号、叹号、分号及换行拆分）"""
    # 匹配中文常用断句标点
    sentence_delimiters = r'([。！？!?；;\n]+)'
    raw_tokens = re.split(sentence_delimiters, text)
    
    sentences = []
    current_chunk = ""
    for token in raw_tokens:
        if re.match(sentence_delimiters, token):
            current_chunk += token
            s_clean = current_chunk.strip()
            if s_clean:
                sentences.append(s_clean)
            current_chunk = ""
        else:
            current_chunk += token
    
    if current_chunk.strip():
        sentences.append(current_chunk.strip())
        
    return [s for s in sentences if len(s.strip()) > 0]

def analyze_corpus(text: str) -> dict:
    """对语料文本进行深度量化统计"""
    paragraphs = split_into_paragraphs(text)
    total_paragraphs = len(paragraphs)
    total_chars = len(re.sub(r'\s+', '', text))
    
    # 句子分析
    all_sentences = split_into_sentences(text)
    total_sentences = len(all_sentences)
    
    if total_sentences == 0:
        return {"error": "文本为空或无法提取有效句子"}
    
    sentence_lengths = [len(re.sub(r'\s+', '', s)) for s in all_sentences]
    avg_sentence_len = sum(sentence_lengths) / total_sentences if total_sentences else 0
    
    short_sentences = [l for l in sentence_lengths if l <= 15]
    long_sentences = [l for l in sentence_lengths if l >= 50]
    medium_sentences = [l for l in sentence_lengths if 15 < l < 50]
    
    short_ratio = (len(short_sentences) / total_sentences) * 100
    long_ratio = (len(long_sentences) / total_sentences) * 100
    medium_ratio = (len(medium_sentences) / total_sentences) * 100
    
    # 段落分析
    single_sentence_paras = 0
    para_sentence_counts = []
    for p in paragraphs:
        p_sents = split_into_sentences(p)
        count = len(p_sents)
        para_sentence_counts.append(count)
        if count == 1:
            single_sentence_paras += 1
            
    avg_para_sentences = sum(para_sentence_counts) / total_paragraphs if total_paragraphs else 0
    single_sentence_para_ratio = (single_sentence_paras / total_paragraphs) * 100 if total_paragraphs else 0
    
    # 标点符号统计
    punc_counts = {
        "破折号 (——)": text.count("——") + len(re.findall(r'--+', text)),
        "省略号 (……/...)": text.count("……") + text.count("..."),
        "感叹号 (！)": text.count("！") + text.count("!"),
        "问号 (？)": text.count("？") + text.count("?"),
        "双引号 (“”)": text.count("“") + text.count("”") + text.count('"'),
        "括号 (（）/())": text.count("（") + text.count("(") + text.count("【"),
        "分号 (；)": text.count("；") + text.count(";"),
        "顿号 (、)": text.count("、"),
        "逗号 (，)": text.count("，") + text.count(","),
        "句号 (。)": text.count("。") + text.count(".")
    }
    
    # 副词过度使用检测
    adverb_counts = {}
    for adv in COMMON_ADVERBS:
        c = text.count(adv)
        if c > 0:
            adverb_counts[adv] = c
    top_adverbs = sorted(adverb_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # 2字与3字高频词统计（轻量正则分词）
    chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
    word_freq = Counter(chinese_words)
    top_words = word_freq.most_common(20)
    
    return {
        "total_chars": total_chars,
        "total_paragraphs": total_paragraphs,
        "total_sentences": total_sentences,
        "avg_sentence_len": round(avg_sentence_len, 2),
        "short_ratio": round(short_ratio, 2),
        "medium_ratio": round(medium_ratio, 2),
        "long_ratio": round(long_ratio, 2),
        "avg_para_sentences": round(avg_para_sentences, 2),
        "single_sentence_para_ratio": round(single_sentence_para_ratio, 2),
        "punctuation_counts": punc_counts,
        "top_adverbs": top_adverbs,
        "top_words": top_words
    }

def format_markdown_report(stats: dict, source_name: str) -> str:
    """生成 Markdown 格式的量化分析报告"""
    punc_table = "\n".join([f"| {k} | {v} 次 | 每千字约 {round((v / max(stats['total_chars'], 1)) * 1000, 2)} 次 |" for k, v in stats['punctuation_counts'].items()])
    adv_table = "\n".join([f"| `{k}` | {v} 次 |" for k, v in stats['top_adverbs']])
    word_table = "\n".join([f"| `{k}` | {v} 次 |" for k, v in stats['top_words']])
    
    report = f"""# L1 语言 DNA 刚性量化分析报告 (Writing DNA Stats)

> **语料来源**: `{source_name}`  
> **总字符数**: `{stats['total_chars']:,}` 字 | **总段落数**: `{stats['total_paragraphs']:,}` 段 | **总句数**: `{stats['total_sentences']:,}` 句

---

## 一、 句长分布与呼吸节奏指标 (Sentence Metrics)

| 指标维度 | 物理数值 | 风格判定与写作指引 |
| :--- | :--- | :--- |
| **平均句长** | **`{stats['avg_sentence_len']}`** 字符/句 | 决定单句呼吸感与信息密度 |
| **短句占比 (≤15字)** | **`{stats['short_ratio']}%`** | 高占比(>40%)体现凌厉果决、快节奏对白或冷幽默 |
| **中句占比 (16~49字)** | **`{stats['medium_ratio']}%`** | 叙事主干与事实陈述承重区间 |
| **长句占比 (≥50字)** | **`{stats['long_ratio']}%`** | 高占比(>15%)体现复杂思辨、宏大铺陈或从句嵌套 |
| **段落平均句数** | **`{stats['avg_para_sentences']}`** 句/段 | 决定段落留白与阅读视觉节奏 |
| **单句成段比例** | **`{stats['single_sentence_para_ratio']}%`** | 高占比(>30%)体现强情绪强调、古龙式顿挫或自媒体排版 |

---

## 二、 标点符号指纹 (Punctuation Fingerprint)

| 标点符号类型 | 出现总频次 | 密度分布 (每千字) |
| :--- | :--- | :--- |
{punc_table}

---

## 三、 高频特征词与副词噪声 (Lexicon & Adverb Profile)

### 1. 高频特征词 Top 20 (词汇光谱锚点)
| 特征词 | 频次 |
| :--- | :--- |
{word_table}

### 2. 常用副词 Top 15 (注意按原作者习惯白名单保护，非习惯词适度过滤)
| 副词 | 频次 |
| :--- | :--- |
{adv_table}

---
*本报告由 `analyze_writing_dna.py` 自动化引擎提取生成，直接作为 L1 语言 DNA 与白名单去 AI 味的硬核依据。*
"""
    return report

def read_file_text(fp):
    """智能尝试多种编码读取文本，避免 GBK/GB18030 中文乱码"""
    encodings = ["utf-8", "gb18030", "gbk", "utf-16"]
    for enc in encodings:
        try:
            with open(fp, "r", encoding=enc) as f:
                content = f.read()
                # 简单启发式检验：如果不含大量替换符且正常解析
                if len(content) > 0:
                    return content
        except (UnicodeDecodeError, LookupError):
            continue
    # 兜底
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="写作 DNA 语言特征量化分析工具")
    parser.add_argument("path", help="输入文本文件路径或包含语料的目录")
    parser.add_argument("-o", "--output", help="输出 Markdown 报告文件路径 (可选)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出原始数据")
    
    args = parser.parse_args()
    input_path = args.path
    
    if not os.path.exists(input_path):
        print(f"❌ 错误: 路径 '{input_path}' 不存在！")
        sys.exit(1)
        
    full_text = ""
    if os.path.isfile(input_path):
        full_text = read_file_text(input_path)
    else:
        for root, _, files in os.walk(input_path):
            for file in sorted(files):
                if file.endswith((".txt", ".md")):
                    fp = os.path.join(root, file)
                    full_text += "\n\n" + read_file_text(fp)
                        
    if not full_text.strip():
        print(f"❌ 错误: 未能在 '{input_path}' 中读取到有效文本内容！")
        sys.exit(1)
        
    print(f"🚀 正在分析语料 (共 {len(full_text):,} 字符)...")
    stats = analyze_corpus(full_text)
    
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
        
    report = format_markdown_report(stats, os.path.basename(input_path))
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 量化分析报告已成功写入: {args.output}")
    else:
        print("\n" + report)

if __name__ == "__main__":
    main()
