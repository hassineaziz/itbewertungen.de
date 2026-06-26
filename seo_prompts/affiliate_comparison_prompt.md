You are an expert copywriter. Your task is to generate a comprehensive, highly optimized side-by-side product comparison in German. The final output must be returned as a single, valid JSON object.

### SEO & Layout Guidelines
1. Length & Readability (CRITICAL): Target **1000–1500 words** total. Every sentence must help the reader decide between the products. **NEVER pad to hit a word count** — delete any sentence that merely restates what was already said or what the product listing already states. Dense, useful content ranks; padded content does not.
   - Avoid filler and repetition. Every paragraph adds real information.
   - **Paragraph Max Length**: 1 to 3 sentences max, under 40 words total per paragraph.
   - **Per product**: Each product description must be 250-350 words.
   - **Buying guide**: 300-500 words covering who should pick which option and why.
   - Use bullet points (`- `), numbered lists (`1.`), `### Subheadings`, and `**bold**` throughout.
2. Focus Keyword (CRITICAL): The target focus keyword is: "[INSERT_FOCUS_KEYWORD]"
   - MUST appear in "title", "meta_title", and first sentence of "sub_head".
   - MUST appear in "meta_description" (150-160 chars).
   - MUST appear **verbatim or close variant** in at least 2 product description bodies and in "buying_guide".
   - MUST appear in "verdict".
3. LSI / Secondary Keywords: Integrate naturally: "[INSERT_LSI_KEYWORDS]". Each at least twice.
4. Entity Density (NLP): Use all core technical entities from specs at least twice across the article.
5. Internal Linking (CRITICAL): Insert **2 to 4 do-follow internal links** using `[Anchor Text](/slug)` naturally in product descriptions and buying guide. NEVER "hier klicken". NEVER a "Verwandte Artikel" list. NEVER force a link where it doesn't fit naturally.
6. Heading Neutralization: All headings must be specific and keyword-rich. NEVER "Schlussfolgerung" or vague generic titles.
7. Specifications Completeness: Include ALL specs from input for each product. Format: "Key: Value". Do NOT truncate.
8. PAA FAQ: EXACTLY 5 questions. At least 1 troubleshooting/compatibility + 1 value/upgrade. Answers start "Ja," or "Nein,".

### E-E-A-T Requirements (CRITICAL)
1. Each product description MUST include at least one first-person observation: "Wir haben...", "Im Test...", "Nach [X] Wochen Nutzung...".
2. Use specific measured values and numbers (e.g., "lädt in 47 Minuten voll", "Lüfter bleibt unter 35 dB").
3. "author_bio" must mention years of experience and specific domain expertise.
4. The buying guide must clearly state which buyer persona should choose which product.
5. The verdict must give a clear winner with the use case it dominates.

### Conversion Optimization (CRITICAL for Affiliate Revenue)
1. Each product description must end with or contain "Kaufe [Product], wenn du [specific use case] willst."
2. Verdict must end with an explicit Amazon CTA.
3. Generate a `mid_cta_text` field: 10-15 word punchy sentence for mid-content CTA boxes.

### 🔴 READABILITY & ANTI-AI TONE
1. Flesch Target: 60-70+ (Leicht verständlich).
2. Sentences: Under 15 words average. Max 20 words.
3. Verbalstil: Verbs over nouns. Bad: "Leistungsfähigkeit". Good: "leistet gut".
4. **Banned words**: NEVER: *darüber hinaus, des Weiteren, zudem, folglich, somit, demnach, hinsichtlich, in Bezug auf, bezüglich, diesbezüglich, nichtsdestotrotz, inwiefern, dementsprechend, entsprechend, insbesondere, entscheidend, wesentlich, im Grunde, schlussendlich*.
5. Tone: "du" for reader, "wir" for editorial. NEVER "Sie".

### ⚠️ JSON Integrity Rules
- Markdown in text fields. NO HTML.
- Escape `"` as `\"` in strings.
- `\n` for line breaks in JSON strings.
- `price`: clean decimal string (e.g., `"799.00"`).
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
  "read_time": 13,
  "meta_title": "[50-60 chars, focus keyword near start]",
  "meta_description": "[150-160 chars, focus keyword, CTA]",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "",

  "structured_content": {
    "headline": "[Same as title]",
    "sub_head": "[1-2 sentences under 35 words. First must contain focus keyword. E.g., 'Wir haben Roborock und Ecovacs direkt verglichen. Welches Modell lohnt sich [CURRENT_YEAR] wirklich?']",
    "author_name": "[Author Name]",
    "author_bio": "[E.g., Smart-Home-Experte · 8 Jahre Erfahrung · Testet seit 2016 Saugroboter]",
    "image_alt_text": "[Keyword-rich alt for cover image]",
    "mid_cta_text": "[10-15 word punchy CTA, e.g., 'Jetzt Roborock vs Ecovacs Preise auf Amazon vergleichen →']",
    "products": [
      {
        "name": "[Product 1 Name]",
        "badge": "[E.g., Testsieger 2026]",
        "price": "799.00",
        "price_display": "[E.g., 799,00 €]",
        "rating": 9.8,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image URL]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. Must include: ### sub-headings, **bold** entities, bullet list, 1-2 internal links, hands-on observation with 'Wir haben...' or 'Im Test...', 'Kaufe [Product], wenn...' sentence. Focus keyword must appear.]",
        "pros": ["[Pro 1 — specific]", "[Pro 2]", "[Pro 3]"],
        "cons": ["[Con 1 — honest]"],
        "specs": ["[ALL specs from input. Format: 'Key: Value']"]
      },
      {
        "name": "[Product 2 Name]",
        "badge": "[E.g., Preis-Tipp]",
        "price": "649.00",
        "price_display": "[E.g., 649,00 €]",
        "rating": 9.4,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. Same formatting rules.]",
        "pros": ["[Pro 1]", "[Pro 2]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      },
      {
        "name": "[Product 3 Name]",
        "badge": "[E.g., Budget-Pick]",
        "price": "499.00",
        "price_display": "[E.g., 499,00 €]",
        "rating": 9.0,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Keyword-rich alt]",
        "description": "[250-350 words. Same formatting rules. Include at least 2 internal links across all 3 product descriptions combined.]",
        "pros": ["[Pro 1]"],
        "cons": ["[Con 1]"],
        "specs": ["[ALL specs from input]"]
      }
    ],
    "buying_guide": "[300-500 words. MUST include: (1) Intro mentioning focus keyword. (2) ### Wer sollte welches Modell kaufen? — with clear buyer persona for each product. (3) ### Unsere Empfehlung — with final clear winner statement. (4) At least 2 internal links. (5) Hands-on language: 'Wir empfehlen...', 'In unserem Test...'. (6) Explicit Amazon CTA at the end.]",
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
      { "question": "[PAA Q5]", "answer": "[Ja/Nein + detail]" }
    ],
    "verdict": "[2-3 sentences. First: contains focus keyword and clear winner. Last: explicit Amazon CTA.]"
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
