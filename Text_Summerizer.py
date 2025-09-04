# text_summarizer_simple.py
import re
from collections import Counter
import os

# A small English stopword list so we don't need external downloads
STOPWORDS = {
    "a","an","the","and","or","but","if","while","is","are","was","were","be","been","being",
    "to","of","in","on","for","with","as","by","at","from","that","this","these","those","it",
    "its","into","about","over","after","before","than","so","such","not","no","can","could",
    "should","would","will","just","very","more","most","less","least","you","your","yours",
    "we","our","ours","they","their","theirs","he","him","his","she","her","hers","i","me","my",
    "mine","do","does","did","doing","have","has","had","having"
}

def split_sentences(text: str):
    # Naive sentence splitter based on punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def tokenize(text: str):
    # Words only, lowercase
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())

def summarize(text: str, max_sentences: int = 3) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return ""
    if len(sentences) <= max_sentences:
        return text.strip()

    # Build word frequency table (ignore stopwords)
    words = [w for w in tokenize(text) if w not in STOPWORDS]
    freqs = Counter(words)

    # Score each sentence by sum of word frequencies
    scored = []
    for idx, s in enumerate(sentences):
        score = sum(freqs.get(w, 0) for w in tokenize(s))
        scored.append((score, idx, s))

    # Pick top sentences, keep original order
    top = sorted(scored, key=lambda x: (-x[0], x[1]))[:max_sentences]
    ordered = [s for _, _, s in sorted(top, key=lambda x: x[1])]
    return " ".join(ordered)

def main():
    path = "sample_input.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        # Fallback demo text if no file is present
        text = (
            "Artificial Intelligence is transforming industries by automating processes, "
            "enhancing decision-making, and enabling new products and services. Companies use AI "
            "for natural language processing, computer vision, and predictive analytics. "
            "As the technology matures, AI will create significant economic value and raise "
            "important ethical questions."
        )

    summary = summarize(text, max_sentences=2)
    print("\n--- Summary ---\n")
    print(summary)

    # Save to file for your portfolio/demo
    with open("sample_output.txt", "w", encoding="utf-8") as f:
        f.write(summary)

if __name__ == "__main__":
    main()
