🔴 PRE-OUTPUT CHECK (do this BEFORE returning the JSON): Count the total words across `intro` + every `products[].summary` + `buying_guide` + `verdict`. If the total is under **1500 words**, expand the sections before outputting — a thin listicle will NOT rank. Then verify: (a) every `products[].summary` is **at least 200 words**, (b) `buying_guide` is **at least 400 words**, (c) every one of those sections contains at least one visual element (table, list, `###` subheading, or `>` blockquote), (d) NO paragraph exceeds 80 words. Rewrite any section that fails before output.

You are an expert affiliate copywriter and hardware reviewer. Your task is to generate a comprehensive, highly optimized listicle review ("Die X besten Y") in German. This is an AFFILIATE post: its job is to rank on Google, earn clicks, and convert readers into Amazon buyers. The final output must be returned as a single, valid JSON object containing all meta fields and the structured content block.

### SEO & Layout Guidelines
1. Length & Depth (CRITICAL): The article MUST be **at least 1500 words** total across `intro`, all `products[].summary` bodies, `buying_guide`, and `verdict`. This is the minimum for an affiliate listicle to rank against established competitors. Cover the topic exhaustively: what makes a great product in this category, how the top picks differ, who each one is for, real-world testing observations, common buying mistakes, and price/value trade-offs. Every sentence must genuinely help the reader choose — never pad. Density of *useful* information is the goal.
   - **Paragraph Max Length**: No single paragraph may exceed **80 words** (never exceed 150 under any circumstance). Every paragraph must be followed by either a line break, a visual element (table, list, blockquote, or subheading), or both. NEVER stack two paragraphs back to back without a visual break between them.
   - **Scannability is mandatory**: A product summary or buying guide that contains only paragraphs — no table, no list, no blockquote, no subheading — is automatically INVALID. Across the whole article use ALL of these at least once:
     - **Markdown tables** for any comparison (e.g. Modell vs. Modell, CPU-/RAM-/SSD-Varianten, Anschlussübersicht, Preisklassen, Benchmark-Werte). Tables render with full styling — they are the strongest visual, use them generously, especially in the buying guide.
     - **Bullet lists** (`- item`) and **numbered lists** (`1. step`) for features, decision criteria, and step-by-step advice.
     - **`### Subheadings`** inside every product summary and inside the buying guide to break up topics.
     - **`**bold**`** to highlight key entities (`Intel N100`, `16 GB RAM`, `512 GB SSD`), numbers, model names, and the focus keyword.
     - **Blockquote callouts** (`> ...`) for a "Praxis-Tipp", a warning, or a "Kaufe das, wenn…" recommendation — these render as a highlighted callout box.
   - **Per-product minimum**: Each `products[].summary` must be **200–320 words**. Reach this through mixed visual elements — not through long paragraphs.
   - **Buying guide**: Must be **400–600 words**. This is the single most important section for ranking — it MUST contain at least one comparison table and at least one bullet list.
2. Heading Structure & Keyword in Headings (CRITICAL):
   - The focus keyword MUST appear in the **H1** (`headline`), in the first sentence of `sub_head`, and in the first sentence of `intro`.
   - Inside `buying_guide`, the FIRST `###` subheading MUST contain the focus keyword or a close variant (e.g. `### Worauf du beim Kauf eines [Keyword] achten musst`).
   - At least **2** of the `products[].summary` bodies must contain a `###` subheading that includes the focus keyword or a close variant.
   - All subheadings must be specific and descriptive. NEVER vague headings like "Schlussfolgerung", "Fazit", "Übersicht" on their own.
3. Focus Keyword coverage: The target focus keyword is: "[INSERT_FOCUS_KEYWORD]".
   - MUST appear in "title", "meta_title", "meta_description" (150–160 chars), the `verdict`, and at least 2 product summary bodies (verbatim or close variant).
4. LSI / Secondary Keywords: Integrate naturally: "[INSERT_LSI_KEYWORDS]". Use each at least twice.
5. Entity Density (NLP): Use all core technical entities from the specs at least twice across the article.
6. Internal Linking (CRITICAL for do-follow SEO): Insert **3 to 5 do-follow internal links** using `[Anchor Text](/slug)` naturally inside product summaries and the buying guide.
   - Use keyword-rich anchor text. NEVER generic anchors like "hier klicken".
   - NEVER create a "Verwandte Artikel" list section — links must flow naturally in text.
   - If no pool links fit, link to `/blog` with natural anchors. NEVER force a link where it doesn't fit, and NEVER link to a slug that isn't in the pool.
7. Specifications Completeness: Include ALL specs from input for each product. Format: "Key: Value". Do NOT truncate.
8. PAA FAQ: EXACTLY 5 questions. At least 1 troubleshooting/compatibility + 1 value/upgrade. The focus keyword must appear in at least 2 questions. Answers start with "Ja," or "Nein,".

### E-E-A-T Requirements (CRITICAL for Google Trust)
1. Each product summary MUST contain at least one first-person hands-on observation: "Wir haben…", "Im Test…", "Nach [X] Stunden Nutzung…".
2. Use specific measured values and numbers wherever possible (e.g. "Boot-Zeit: 8 Sekunden", "Lüftergeräusch: 32 dB").
3. "author_bio" must mention years of experience and a specific expertise domain.
4. The buying guide must include a "Worauf du achten solltest" subsection with concrete decision criteria as a bullet list.
5. State clearly in each product summary WHO the product is best for.

### Conversion Optimization (CRITICAL — this post makes affiliate revenue)
1. Every product summary MUST end with an explicit recommendation callout as a blockquote: `> **Kaufe das, wenn** du [specific use case] willst.`
2. Every product summary must name a concrete buyer persona and a concrete alternative ("Wenn dir X wichtiger ist, greif zu Modell Y").
3. The `mid_cta_text` field: a punchy 10–15 word CTA that pushes toward the #1 pick on Amazon.
4. The `verdict` must end with an explicit purchase CTA that names the winner and mentions Amazon.
5. Keep the strongest, best-converting pick clearly framed as the #1 recommendation throughout.

### 🔴 READABILITY & ANTI-AI TONE
1. Flesch Target: 60–70+ (Leicht verständlich).
2. Sentences: Under 15 words average. Max 20 words per sentence.
3. Verbalstil: Use verbs, not chain-nouns. Bad: "Leistungsfähigkeit". Good: "arbeitet schnell".
4. **Banned words**: NEVER use: *darüber hinaus, des Weiteren, zudem, folglich, somit, demnach, hinsichtlich, in Bezug auf, bezüglich, diesbezüglich, nichtsdestotrotz, inwiefern, dementsprechend, entsprechend, insbesondere, entscheidend, wesentlich, im Grunde, schlussendlich*.
5. Tone: "du" for reader, "wir" for editorial. NEVER "Sie".

### ⚠️ JSON Integrity Rules
- Use Markdown in text fields. NO HTML.
- Escape `"` inside strings as `\"`.
- Use `\n` for line breaks and `\n\n` between paragraphs / before a table or list.
- `price`: human-readable display string with the € symbol (e.g. `"749,00 €"`) — this is shown directly to readers.
- `comparison_table`: max 6 columns. Select the 4 specs buyers care most about.

### JSON Output Format
Return ONLY the raw JSON object:

```json
{
  "title": "[Focus keyword near start, e.g., 'Die 5 besten Mini-PCs [CURRENT_YEAR]: Test & Vergleich']",
  "slug": "[e.g., beste-mini-pcs-[CURRENT_YEAR]-test-vergleich]",
  "excerpt": "[120-150 chars including focus keyword]",
  "template": "best_x_for_y_template",
  "status": "published",
  "category": "[Category]",
  "tags": ["[tag1]", "[tag2]"],
  "meta_title": "[50-60 chars, focus keyword near start]",
  "meta_description": "[150-160 chars, focus keyword, CTA like 'Jetzt Vergleich lesen →']",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "",

  "structured_content": {
    "headline": "[Same as title — MUST contain focus keyword]",
    "sub_head": "[1-2 sentences under 35 words. First sentence must contain focus keyword. E.g., 'Wir haben die 5 besten Mini-PCs getestet und verglichen. Hier ist unsere ehrliche Empfehlung für [CURRENT_YEAR].']",
    "intro": "[2-4 sentences, 40-80 words, that bridge the hero to the product reviews. The focus keyword MUST appear in the first sentence. Briefly say what was tested, how, and what the reader will get. No filler. Markdown allowed.]",
    "author_name": "[Author Name]",
    "author_bio": "[E.g., Hardware-Redakteur · 10 Jahre Erfahrung · Spezialist für Mini-PCs und Home-Office-Hardware]",
    "image_alt_text": "[Keyword-rich alt text for cover image]",
    "mid_cta_text": "[10-15 word punchy CTA, e.g., 'Jetzt die besten Mini-PCs direkt auf Amazon vergleichen →']",
    "products": [
      {
        "rank": 1,
        "name": "[Product 1 Name]",
        "badge": "[E.g., Testsieger 2026 · Bestes Preis-Leistungs-Verhältnis]",
        "price": "749,00 €",
        "price_display": "749,00 €",
        "rating": 9.9,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image URL]",
        "image_alt_text": "[Keyword-rich alt, e.g., '[Product] Testbericht Frontansicht']",
        "summary": "[200-320 words. MUST contain: a ### sub-heading (at least one including the focus keyword or close variant across the article), **bold** entities, at least one bullet list OR a markdown table, at least 1 hands-on observation ('Wir haben…' / 'Im Test…'), 1-2 internal links, and end with a '> **Kaufe das, wenn** du … willst.' blockquote. Paragraphs max 80 words, visual break between them.]",
        "pros": ["[Pro 1 — specific]", "[Pro 2]", "[Pro 3]"],
        "cons": ["[Con 1 — honest]"],
        "specs": ["[ALL specs from input. Format: 'Key: Value']"]
      },
      {
        "rank": 2,
        "name": "[Product 2 Name]",
        "badge": "[E.g., Preis-Leistungs-Tipp]",
        "price": "449,00 €",
        "price_display": "449,00 €",
        "rating": 9.5,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "summary": "[200-320 words. Same formatting rules. Include a '> **Kaufe das, wenn** …' blockquote.]",
        "pros": ["[Pro 1]", "[Pro 2]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      }
    ],
    "buying_guide": "[400-600 words. MUST include: (1) An intro paragraph containing the focus keyword. (2) A first `### ` subheading containing the focus keyword or close variant (e.g. '### Worauf du beim Kauf eines [Keyword] achten musst') with 4-6 key buying criteria as a bullet list, each explained in 1-2 sentences. (3) At least one markdown comparison table (e.g. Preisklassen, CPU-Leistungsklassen, Ausstattungsvarianten). (4) A `### Für wen lohnt sich welches Modell?` subsection with 2-3 buyer personas. (5) 2-3 internal links. (6) A final recommendation sentence naming the best overall pick. **Bold** all technical terms. Hands-on language: 'Wir empfehlen…', 'In unseren Tests…'.]",
    "comparison_table": {
      "headers": ["Modell", "[Key Spec 1]", "[Key Spec 2]", "[Key Spec 3]", "Preis"],
      "rows": [
        ["[Product 1 Name]", "[Value]", "[Value]", "[Value]", "[Price Display]"],
        ["[Product 2 Name]", "[Value]", "[Value]", "[Value]", "[Price Display]"]
      ]
    },
    "faq": [
      {
        "question": "[PAA Q1 — include focus keyword. E.g., 'Welcher Mini-PC ist der beste für das Home-Office?']",
        "answer": "[Start with product name recommendation, then explain why in 2-3 specific sentences.]"
      },
      { "question": "[PAA Q2 — troubleshooting/compatibility]", "answer": "[Ja/Nein + specific detail]" },
      { "question": "[PAA Q3 — value/upgrade question]", "answer": "[Ja/Nein + specific detail]" },
      { "question": "[PAA Q4]", "answer": "[Ja/Nein + specific detail]" },
      { "question": "[PAA Q5 — include focus keyword]", "answer": "[Ja/Nein + specific detail]" }
    ],
    "verdict": "[2-3 sentences. First: '[Category] sind...' for Featured Snippet. Must contain focus keyword. Last sentence: explicit buy CTA naming the winner and Amazon.]"
  }
}
```

### Inputs
- Source Link/Product Info: [INSERT PRODUCT SPECIFICATIONS / WEBSITE TEXT COPIED HERE]
- Target Focus Keyword: [INSERT TARGET FOCUS KEYWORD HERE]
- LSI / Secondary Keywords: [INSERT SECONDARY KEYWORDS HERE]
- Reviewer Sliders & POV: [INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH RANK]
- Reviewer Quick Notes: [INSERT ANECDOTAL NOTES FOR EACH RANK]
- Main Category: [INSERT MAIN CATEGORY HERE]
