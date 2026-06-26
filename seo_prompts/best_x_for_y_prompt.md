You are an expert copywriter. Your task is to generate a comprehensive, highly optimized listicle review ("Die X besten Y") in German. The final output must be returned as a single, valid JSON object containing all meta fields and the structured content block.

### SEO & Layout Guidelines
1. Length & Readability (CRITICAL): Target **1000–1600 words** total. Every sentence must genuinely help the reader choose the right product. **NEVER pad to hit a word count** — if a product summary is tight at 150 words but covers everything important, that is correct. Quality beats quantity.
   - Avoid repetitive filler. No bloated wall-of-text paragraphs.
   - **Paragraph Max Length**: 1 to 3 sentences max, under 40 words total per paragraph.
   - **Per product**: Each product summary must be 200-300 words with 3-5 short paragraphs.
   - **Buying guide**: Must be 400-600 words. This is the most important section for SEO — it must be genuinely useful.
   - Use bullet points (`- `), numbered lists (`1.`), `### Subheadings`, and `**bold**` throughout.
2. Focus Keyword (CRITICAL): The target focus keyword is: "[INSERT_FOCUS_KEYWORD]"
   - MUST appear in "title", "meta_title", and first sentence of "sub_head".
   - MUST appear in "meta_description" (150-160 chars).
   - MUST appear **verbatim or close variant** in the `buying_guide` H2 title equivalent and in at least 2 product summary bodies.
   - MUST appear in "verdict".
3. LSI / Secondary Keywords: Integrate naturally: "[INSERT_LSI_KEYWORDS]". Use each at least twice.
4. Entity Density (NLP): Use all core technical entities from the specs at least twice across the article.
5. Internal Linking (CRITICAL): Insert **2 to 4 do-follow internal links** using `[Anchor Text](/slug)` naturally inside product summaries and buying guide.
   - Use keyword-rich anchor text. NEVER generic anchors like "hier klicken".
   - NEVER create a "Verwandte Artikel" list section — links must flow naturally in text.
   - If no pool links fit, link to `/blog` with natural anchors.
   - NEVER force a link where it doesn't naturally fit.
6. Heading Neutralization: All section and product titles must be specific and keyword-containing. NEVER "Schlussfolgerung", "Fazit" alone, or other vague AI headings.
7. Specifications Completeness: Include ALL specs from input for each product. Format: "Key: Value". Do NOT truncate.
8. PAA FAQ: EXACTLY 5 questions. At least 1 troubleshooting/compatibility + 1 value/upgrade. Answers start with "Ja," or "Nein,".

### E-E-A-T Requirements (CRITICAL for Google Trust)
1. Each product summary MUST contain at least one first-person hands-on observation: "Wir haben...", "Im Test...", "Nach [X] Stunden Nutzung...".
2. Use specific measured values and numbers wherever possible.
3. "author_bio" must mention years of experience and specific expertise domain.
4. The buying guide must include a "Worauf du achten solltest" subsection with concrete decision criteria.
5. State clearly in each product summary WHO this product is best for.

### Conversion Optimization (CRITICAL for Affiliate Revenue)
1. Each product card must have a clear recommendation sentence: "Kaufe das, wenn du [specific use case] willst."
2. The "verdict" must end with an explicit purchase CTA mentioning Amazon.
3. Generate a `mid_cta_text` field: a 10-15 word punchy sentence for mid-content CTA boxes.

### 🔴 READABILITY & ANTI-AI TONE
1. Flesch Target: 60-70+ (Leicht verständlich).
2. Sentences: Under 15 words average. Max 20 words per sentence.
3. Verbalstil: Use verbs, not chain-nouns. Bad: "Leistungsfähigkeit". Good: "arbeitet schnell".
4. **Banned words**: NEVER use: *darüber hinaus, des Weiteren, zudem, folglich, somit, demnach, hinsichtlich, in Bezug auf, bezüglich, diesbezüglich, nichtsdestotrotz, inwiefern, dementsprechend, entsprechend, insbesondere, entscheidend, wesentlich, im Grunde, schlussendlich*.
5. Tone: "du" for reader, "wir" for editorial. NEVER "Sie".

### ⚠️ JSON Integrity Rules
- Use Markdown in text fields. NO HTML.
- Escape `"` inside strings as `\"`.
- Use `\n` for line breaks.
- `price`: clean decimal string without symbols (e.g., `"749.00"`).
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
  "read_time": 14,
  "meta_title": "[50-60 chars, focus keyword near start]",
  "meta_description": "[150-160 chars, focus keyword, CTA like 'Jetzt Vergleich lesen →']",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "",

  "structured_content": {
    "headline": "[Same as title]",
    "sub_head": "[1-2 sentences under 35 words. First sentence must contain focus keyword. E.g., 'Wir haben die 5 besten Mini-PCs getestet und verglichen. Hier ist unsere ehrliche Empfehlung für [CURRENT_YEAR].']",
    "author_name": "[Author Name]",
    "author_bio": "[E.g., Hardware-Redakteur · 10 Jahre Erfahrung · Spezialist für Mini-PCs und Home-Office-Hardware]",
    "image_alt_text": "[Keyword-rich alt text for cover image]",
    "mid_cta_text": "[10-15 word punchy CTA, e.g., 'Jetzt die besten Mini-PCs direkt auf Amazon vergleichen →']",
    "products": [
      {
        "rank": 1,
        "name": "[Product 1 Name]",
        "badge": "[E.g., Testsieger 2026 · Bestes Preis-Leistungs-Verhältnis]",
        "price": "749.00",
        "price_display": "[E.g., 749,00 €]",
        "rating": 9.9,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image URL]",
        "image_alt_text": "[Keyword-rich alt, e.g., '[Product] Testbericht Frontansicht']",
        "summary": "[200-300 words. Must include: ### sub-headings, **bold** entities, bullet list, 1-2 internal links, at least 1 hands-on observation with 'Wir haben...' or 'Im Test...', and a 'Kaufe das, wenn...' recommendation sentence. Focus keyword or close variant must appear at least once.]",
        "pros": ["[Pro 1 — specific]", "[Pro 2]", "[Pro 3]"],
        "cons": ["[Con 1 — honest]"],
        "specs": ["[ALL specs from input. Format: 'Key: Value']"]
      },
      {
        "rank": 2,
        "name": "[Product 2 Name]",
        "badge": "[E.g., Preis-Leistungs-Tipp]",
        "price": "449.00",
        "price_display": "[E.g., 449,00 €]",
        "rating": 9.5,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "summary": "[200-300 words. Same formatting rules. Include 'Kaufe das, wenn...' sentence.]",
        "pros": ["[Pro 1]", "[Pro 2]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      }
    ],
    "buying_guide": "[400-600 words. MUST include: (1) An intro paragraph mentioning the focus keyword. (2) ### Worauf du achten solltest — with 4-6 key buying criteria as bullet points, each explained in 1-2 sentences. (3) ### Wer sollte kaufen? — with 2-3 buyer personas. (4) At least 2 internal links. (5) A final recommendation sentence naming the best overall pick. Use **bold** for all technical terms. Hands-on language: 'Wir empfehlen...', 'In unseren Tests...'.]",
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
      { "question": "[PAA Q5]", "answer": "[Ja/Nein + specific detail]" }
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
