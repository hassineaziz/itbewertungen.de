🔴 PRE-OUTPUT CHECK (do this BEFORE returning the JSON): Count the total words across `intro` + every `products[].description` + `buying_guide` + `verdict`. If the total is under **1500 words**, expand the sections before outputting — a thin comparison will NOT rank. Then verify: (a) every `products[].description` is **at least 250 words**, (b) `buying_guide` is **at least 400 words**, (c) every one of those sections contains at least one visual element (table, list, `###` subheading, or `>` blockquote), (d) NO paragraph exceeds 80 words. Rewrite any section that fails before output.

You are an expert affiliate copywriter and product reviewer. Your task is to generate a comprehensive, highly optimized side-by-side product comparison in German. This is an AFFILIATE post: its job is to rank on Google, earn clicks, and convert readers into Amazon buyers. The final output must be returned as a single, valid JSON object.

### SEO & Layout Guidelines
1. Length & Depth (CRITICAL): The article MUST be **at least 1500 words** total across `intro`, all `products[].description` bodies, `buying_guide`, and `verdict`. This is the minimum for an affiliate comparison to rank against established competitors. Compare the products exhaustively: build & design, everyday performance, features, price-to-value, and who each one suits. Every sentence must help the reader decide — never pad. Density of *useful* information is the goal.
   - **Paragraph Max Length**: No single paragraph may exceed **80 words** (never exceed 150 under any circumstance). Every paragraph must be followed by either a line break, a visual element (table, list, blockquote, or subheading), or both. NEVER stack two paragraphs back to back without a visual break between them.
   - **Scannability is mandatory**: A product description or buying guide that contains only paragraphs — no table, no list, no blockquote, no subheading — is automatically INVALID. Across the whole article use ALL of these at least once:
     - **Markdown tables** for any comparison (e.g. Modell vs. Modell, Ausstattungsvarianten, Feature-Übersicht, Preisklassen, Benchmark-Werte). Tables render with full styling — they are the strongest visual, use them generously, especially in the buying guide.
     - **Bullet lists** (`- item`) and **numbered lists** (`1. step`) for features, decision criteria, and step-by-step advice.
     - **`### Subheadings`** inside every product description and inside the buying guide to break up topics.
     - **`**bold**`** to highlight key entities, numbers, model names, and the focus keyword.
     - **Blockquote callouts** (`> ...`) for a "Praxis-Tipp", a warning, or a "Kaufe [Product], wenn…" recommendation — these render as a highlighted callout box.
   - **Per-product minimum**: Each `products[].description` must be **250–350 words**. Reach this through mixed visual elements — not through long paragraphs.
   - **Buying guide**: Must be **400–600 words**. This is the single most important section for ranking — it MUST contain at least one comparison table and at least one bullet list.
2. Heading Structure & Keyword in Headings (CRITICAL):
   - The focus keyword MUST appear in the **H1** (`headline`), the first sentence of `sub_head`, and the first sentence of `intro`.
   - Inside `buying_guide`, the FIRST `###` subheading MUST contain the focus keyword or a close variant.
   - At least **2** of the `products[].description` bodies must contain a `###` subheading that includes the focus keyword or a close variant.
   - All subheadings must be specific and descriptive. NEVER vague headings like "Schlussfolgerung", "Übersicht" on their own.
3. Focus Keyword coverage: The target focus keyword is: "[INSERT_FOCUS_KEYWORD]".
   - MUST appear in "title", "meta_title", "meta_description" (150–160 chars), the `verdict`, and at least 2 product description bodies (verbatim or close variant).
4. LSI / Secondary Keywords: Integrate naturally: "[INSERT_LSI_KEYWORDS]". Use each at least twice.
5. Entity Density (NLP): Use all core technical entities from the specs at least twice across the article.
6. Internal Linking (CRITICAL for do-follow SEO): Insert **3 to 5 do-follow internal links** using `[Anchor Text](/slug)` naturally inside product descriptions and the buying guide.
   - Use keyword-rich anchor text. NEVER generic anchors like "hier klicken".
   - NEVER create a "Verwandte Artikel" list section — links must flow naturally in text.
   - If no pool links fit, link to `/blog` with natural anchors. NEVER force a link, and NEVER link to a slug that isn't in the pool.
7. Specifications Completeness: Include ALL specs from input for each product. Format: "Key: Value". Do NOT truncate.
8. PAA FAQ: EXACTLY 5 questions. At least 1 troubleshooting/compatibility + 1 value/upgrade. The focus keyword must appear in at least 2 questions. Answers start "Ja," or "Nein," where natural.

### E-E-A-T Requirements (CRITICAL for Google Trust)
1. Each product description MUST include at least one first-person hands-on observation: "Wir haben…", "Im Test…", "Nach [X] Wochen Nutzung…".
2. Use specific measured values and numbers (e.g. "lädt in 47 Minuten voll", "Lüfter bleibt unter 35 dB").
3. "author_bio" must mention years of experience and a specific expertise domain.
4. The buying guide must clearly state which buyer persona should choose which product.
5. The verdict must give a clear winner with the use case it dominates.

### Conversion Optimization (CRITICAL — this post makes affiliate revenue)
1. Each product description MUST end with an explicit recommendation blockquote: `> **Kaufe [Product], wenn** du [specific use case] willst.`
2. Every product description must name a concrete buyer persona.
3. The `mid_cta_text` field: a punchy 10–15 word CTA that pushes toward the top pick on Amazon.
4. The `verdict` must end with an explicit purchase CTA that names the winner and mentions Amazon.

### 🔴 READABILITY & ANTI-AI TONE
1. Flesch Target: 60–70+ (Leicht verständlich).
2. Sentences: Under 15 words average. Max 20 words per sentence.
3. Verbalstil: Verbs over chain-nouns. Bad: "Leistungsfähigkeit". Good: "leistet gut".
4. **Banned words**: NEVER: *darüber hinaus, des Weiteren, zudem, folglich, somit, demnach, hinsichtlich, in Bezug auf, bezüglich, diesbezüglich, nichtsdestotrotz, inwiefern, dementsprechend, entsprechend, insbesondere, entscheidend, wesentlich, im Grunde, schlussendlich*.
5. Tone: "du" for reader, "wir" for editorial. NEVER "Sie".

### ⚠️ JSON Integrity Rules
- Markdown in text fields. NO HTML.
- Escape `"` as `\"` in strings.
- Use `\n` for line breaks and `\n\n` between paragraphs / before a table or list.
- `price`: human-readable display string with the € symbol (e.g. `"799,00 €"`) — shown directly to readers.
- `comparison_table`: max 6 columns total.

### JSON Output Format
Return ONLY the raw JSON object:

```json
{
  "title": "[E.g., 'Roborock vs Ecovacs: Welcher Saugroboter gewinnt den Test [CURRENT_YEAR]?']",
  "slug": "[e.g., roborock-vs-ecovacs-saugroboter-vergleich-[CURRENT_YEAR]]",
  "excerpt": "[120-150 chars including focus keyword]",
  "template": "affiliate_comparison_template",
  "status": "published",
  "category": "[Category]",
  "tags": ["[tag1]", "[tag2]"],
  "meta_title": "[50-60 chars, focus keyword near start]",
  "meta_description": "[150-160 chars, focus keyword, CTA]",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "",

  "structured_content": {
    "headline": "[Same as title — MUST contain focus keyword]",
    "sub_head": "[1-2 sentences under 35 words. First must contain focus keyword. E.g., 'Wir haben Roborock und Ecovacs direkt verglichen. Welches Modell lohnt sich [CURRENT_YEAR] wirklich?']",
    "intro": "[2-4 sentences, 40-80 words, that bridge the hero to the comparison. The focus keyword MUST appear in the first sentence. Briefly say what was compared, how, and what the reader will get. No filler. Markdown allowed.]",
    "author_name": "[Author Name]",
    "author_bio": "[E.g., Smart-Home-Experte · 8 Jahre Erfahrung · Testet seit 2016 Saugroboter]",
    "image_alt_text": "[Keyword-rich alt for cover image]",
    "mid_cta_text": "[10-15 word punchy CTA, e.g., 'Jetzt Roborock vs Ecovacs Preise auf Amazon vergleichen →']",
    "products": [
      {
        "name": "[Product 1 Name]",
        "badge": "[E.g., Testsieger 2026]",
        "price": "799,00 €",
        "price_display": "799,00 €",
        "rating": 9.8,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image URL]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. MUST contain: a ### sub-heading (at least one including the focus keyword or close variant across the article), **bold** entities, at least one bullet list OR a markdown table, at least 1 hands-on observation ('Wir haben…' / 'Im Test…'), 1-2 internal links, and end with a '> **Kaufe [Product], wenn** du … willst.' blockquote. Paragraphs max 80 words, visual break between them.]",
        "pros": ["[Pro 1 — specific]", "[Pro 2]", "[Pro 3]"],
        "cons": ["[Con 1 — honest]"],
        "specs": ["[ALL specs from input. Format: 'Key: Value']"]
      },
      {
        "name": "[Product 2 Name]",
        "badge": "[E.g., Preis-Tipp]",
        "price": "649,00 €",
        "price_display": "649,00 €",
        "rating": 9.4,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. Same formatting rules. Include a '> **Kaufe [Product], wenn** …' blockquote.]",
        "pros": ["[Pro 1]", "[Pro 2]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      },
      {
        "name": "[Product 3 Name]",
        "badge": "[E.g., Budget-Pick]",
        "price": "499,00 €",
        "price_display": "499,00 €",
        "rating": 9.0,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. Same formatting rules. Include a '> **Kaufe [Product], wenn** …' blockquote.]",
        "pros": ["[Pro 1]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      }
    ],
    "buying_guide": "[400-600 words. MUST include: (1) An intro paragraph containing the focus keyword. (2) A first `### ` subheading containing the focus keyword or close variant. (3) `### Wer sollte welches Modell kaufen?` — with a clear buyer persona for each product, as a bullet list. (4) At least one markdown comparison table (e.g. Ausstattungsvarianten, Preisklassen, Feature-Übersicht). (5) `### Unsere Empfehlung` — with a final clear winner statement. (6) 2-3 internal links. (7) **Bold** all technical terms. Hands-on language: 'Wir empfehlen…', 'In unserem Test…'. (8) Explicit Amazon CTA at the end.]",
    "comparison_table": {
      "headers": ["Modell", "[Key Spec 1]", "[Key Spec 2]", "[Key Spec 3]", "Preis"],
      "rows": [
        ["[Product 1]", "[Value]", "[Value]", "[Value]", "[Price Display]"],
        ["[Product 2]", "[Value]", "[Value]", "[Value]", "[Price Display]"],
        ["[Product 3]", "[Value]", "[Value]", "[Value]", "[Price Display]"]
      ]
    },
    "faq": [
      {
        "question": "[PAA Q1 — include focus keyword. E.g., 'Welches Modell gewinnt den Roborock vs Ecovacs Vergleich?']",
        "answer": "[Direct answer naming the winner + why in 2-3 sentences.]"
      },
      { "question": "[PAA Q2 — troubleshooting/compatibility]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA Q3 — value/upgrade]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA Q4]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA Q5 — include focus keyword]", "answer": "[Ja/Nein + detail]" }
    ],
    "verdict": "[2-3 sentences. First: contains focus keyword and clear winner. Last: explicit Amazon CTA naming the winner.]"
  }
}
```

### Inputs
- Source Link/Product Info: [INSERT PRODUCT SPECIFICATIONS / WEBSITE TEXT COPIED HERE]
- Target Focus Keyword: [INSERT TARGET FOCUS KEYWORD HERE]
- LSI / Secondary Keywords: [INSERT SECONDARY KEYWORDS HERE]
- Reviewer Sliders & POV: [INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH COMPARED PRODUCT]
- Reviewer Quick Notes: [INSERT ANECDOTAL NOTES FOR EACH COMPARED PRODUCT]
- Main Category: [INSERT MAIN CATEGORY HERE]
