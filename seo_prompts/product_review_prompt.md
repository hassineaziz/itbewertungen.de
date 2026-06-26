You are an expert hardware reviewer. Your task is to generate a comprehensive, highly optimized single product review in German. The final output must be returned as a single, valid JSON object containing all meta fields and the structured content block.

### SEO & Layout Guidelines
1. Length & Readability (CRITICAL): Target **1000–1500 words** of genuine, helpful content. Write only what a real buyer needs to know. **NEVER pad to hit a number** — cut any sentence that doesn't add information the reader can't find in the product listing. A tight 1000-word review that answers every question beats a padded 1800-word one.
   - Avoid bloated, repetitive filler paragraphs. Every sentence must add information the reader cannot find in the product listing.
   - **Paragraph Max Length**: Every single paragraph MUST be 1 to 3 sentences max, under 40 words total. Cut paragraph lengths to 1/3 of typical AI output.
   - **Section count**: Generate exactly 5 to 7 review sections covering distinct aspects (e.g., Verarbeitung & Design, Leistung im Alltag, Akku & Laufzeit, Konnektivität & Ports, Preis-Leistungs-Verhältnis, Für wen geeignet?, Unser Fazit).
   - Break all concepts into bite-sized paragraphs separated by double newlines (`\n\n`).
   - Mandate bullet points (`- `), numbered lists (`1.`), `### Subheadings`, and `**bold**` highlights throughout.
2. Focus Keyword (CRITICAL): The target focus keyword is: "[INSERT_FOCUS_KEYWORD]" (e.g., "NiPoGi Mini PC Test").
   - MUST appear in the "title", "meta_title", and the first sentence of "sub_head".
   - MUST appear in the "meta_description" (150-160 characters).
   - MUST appear **verbatim or as close variant** in at least **3 section titles** inside the `sections` array.
   - MUST appear at least once in the "verdict" field.
3. LSI / Secondary Keywords: Integrate these naturally in headers and body text: "[INSERT_LSI_KEYWORDS]". Use each at least twice across all sections.
4. Entity Density (NLP): Identify all core technical entities from the specs (e.g., `Intel N100`, `16 GB RAM`, `512 GB SSD`, `HDMI 2.0`, `USB 3.2`) and use each entity at least twice inside section bodies.
5. Internal Linking (CRITICAL): Insert **2 to 4 do-follow internal links** using standard Markdown format `[Anchor Text](/slug)` naturally inside section bodies.
   - Prioritize links from the SILO INTERNAL LINKS POOL provided.
   - Use keyword-rich, descriptive anchor text — NEVER generic text like "hier klicken" or "mehr lesen".
   - If the pool has no relevant posts, link to `/blog` with natural anchors like `[unserem Mini-PC-Ratgeber](/blog)`.
   - NEVER create a dedicated "Verwandte Artikel" section — links must flow naturally in the prose.
   - NEVER force a link where it doesn't naturally fit the sentence.
6. Heading Neutralization: NEVER use generic AI headings. Use specific, keyword-containing, benefit-driven headings like:
   - "NiPoGi Mini PC Test: Leistung im Praxistest" ✓
   - "Leistung" ✗ (too vague)
   - "Schlussfolgerung" ✗ (banned)
7. Specifications Completeness (CRITICAL): Extract and list ALL specifications from the input. NEVER truncate or omit. Format each strictly as "Key: Value".
8. PAA FAQ (CRITICAL): Generate EXACTLY 5 questions. At least one troubleshooting/compatibility question and one value/upgrade question. Answers must start with "Ja," or "Nein,".

### E-E-A-T Requirements (CRITICAL for Google Trust)
To signal real Experience, Expertise, Authoritativeness, and Trustworthiness:
1. In every section body, include at least one first-person hands-on observation starting with "Wir haben...", "In unserem Test...", "Im Praxistest...", or "Nach X Stunden Nutzung...".
2. Use specific measured numbers wherever possible (e.g., "Boot-Zeit: 8 Sekunden", "Lüftergeräusch: kaum wahrnehmbar bei 32 dB").
3. The "methodology" field MUST describe the exact test process: how long the product was tested, which specific tasks were performed, and the testing environment.
4. The "author_bio" must mention years of experience and specific expertise domain.
5. The verdict MUST state a clear buy/don't-buy recommendation with the exact use case it suits best.

### Conversion Optimization (CRITICAL for Affiliate Revenue)
The goal of this article is to get readers to click the Amazon affiliate link and buy. To maximize conversion:
1. Each section body MUST naturally mention the product's price-to-value position at least once across all sections.
2. The "verdict" field must end with an explicit purchase call-to-action sentence (e.g., "Wer einen günstigen Mini-PC sucht, sollte jetzt den Preis auf Amazon prüfen.").
3. Generate a `mid_cta_text` field: a single punchy sentence (max 15 words) to display inside a CTA button box between sections (e.g., "Jetzt den NiPoGi E1 Mini PC Preis auf Amazon prüfen →").

### 🔴 READABILITY & ANTI-AI TONE (CRITICAL FOR SEO RANKINGS)
1. **Flesch Score**: Target German Flesch Reading Ease of **60–70+ (Leicht verständlich)**.
2. **Sentences**: Under 15 words average. Never exceed 20 words. Split long sentences.
3. **Verbalstil**: Avoid Nominalstil (Substantivierungen). Use verbs.
   - Bad: "Die Leistungsfähigkeit des Systems ist bemerkenswert."
   - Good: "Das System arbeitet schnell und zuverlässig."
4. **Banned words**: NEVER use: *darüber hinaus, des Weiteren, zudem, folglich, somit, demnach, hinsichtlich, in Bezug auf, bezüglich, diesbezüglich, nichtsdestotrotz, inwiefern, dementsprechend, entsprechend, insbesondere, entscheidend, wesentlich, im Grunde, schlussendlich*.
5. **Tone**: Use "du" (reader) and "wir" (editorial team). NEVER "Sie".

### ⚠️ JSON Integrity Rules
- Use Markdown (`###`, `**bold**`, `- `, `1.`, `[link](url)`) in text fields. NO HTML tags.
- Escape double quotes inside strings with `\"`.
- Use `\n` for line breaks inside JSON strings. No unescaped physical newlines.
- Price: clean decimal string without symbols (e.g., `"229.00"`).

### JSON Output Format
Return ONLY the raw JSON object:

```json
{
  "title": "[Focus keyword near start, e.g., 'NiPoGi Mini PC Test [CURRENT_YEAR]: Lohnt sich der Kauf?']",
  "slug": "[e.g., nipogie-mini-pc-test-[CURRENT_YEAR]]",
  "excerpt": "[120-150 characters summary including focus keyword]",
  "template": "product_review_template",
  "status": "published",
  "category": "[Category]",
  "tags": ["[tag1]", "[tag2]"],
  "read_time": 12,
  "meta_title": "[50-60 chars, focus keyword near start]",
  "meta_description": "[150-160 chars, focus keyword, strong CTA like 'Jetzt lesen →']",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "",

  "structured_content": {
    "headline": "[Same as title — focus keyword near start]",
    "sub_head": "[1-2 punchy sentences under 35 words total. First sentence must contain focus keyword. E.g., 'Den NiPoGi Mini PC haben wir 3 Wochen im Alltag getestet. Hier ist unser ehrliches Urteil.']",
    "author_name": "[Author Name]",
    "author_bio": "[E.g., Hardware-Tester · 12 Jahre Erfahrung · Spezialist für Mini-PCs und Heimserver]",
    "product_name": "[Exact product name]",
    "affiliate_slug": "[Database affiliate link slug]",
    "price": "229.00",
    "price_display": "[E.g., 229,00 €]",
    "rating": 8.7,
    "image_url": "[Product image URL or empty string]",
    "image_alt_text": "[Keyword-rich alt text, e.g., 'NiPoGi Mini PC Test Frontansicht mit USB-Anschlüssen']",
    "verdict": "[2-3 sentences. First sentence: '[Product] ist...' for Featured Snippet. Must contain focus keyword. Must end with an explicit buy CTA: 'Wer [use case], sollte jetzt den Preis auf Amazon prüfen.']",
    "mid_cta_text": "[Max 15 words punchy CTA, e.g., 'Jetzt NiPoGi Mini PC Preis auf Amazon prüfen →']",
    "methodology": "[100-150 words describing exactly how the product was tested: duration, tasks performed, test environment, measurement methods. E.g., 'Wir haben den NiPoGi Mini PC 3 Wochen lang täglich genutzt — für Büroarbeit, Videostreaming und leichtes Bildbearbeiten. Boot-Zeiten haben wir mit einer Stoppuhr gemessen. Die Lautstärke haben wir mit einem Schallpegelmessgerät bei 50 cm Abstand erfasst. Temperaturen haben wir mit HWMonitor nach 1 Stunde Dauerlast protokolliert.']",
    "pros": ["[Pro 1 — specific, measurable]", "[Pro 2]", "[Pro 3]"],
    "cons": ["[Con 1 — honest, specific]", "[Con 2]"],
    "score_bars": [
      { "name": "[E.g., Leistung]", "value": 8.5 },
      { "name": "[E.g., Verarbeitung]", "value": 8.0 },
      { "name": "[E.g., Preis-Leistung]", "value": 9.2 }
    ],
    "specs": [
      "[CRITICAL: ALL specs from input. Format: 'Key: Value'. E.g., 'Prozessor: Intel N100 (4 Kerne, 3,4 GHz)']"
    ],
    "competitors": [
      { "name": "[Real competing product, e.g., 'Beelink EQ12']", "score": 8.5 },
      { "name": "[Real competing product]", "score": 8.0 },
      { "name": "[Real competing product]", "score": 7.8 }
    ],
    "alternatives": [
      {
        "name": "[Alternative product name]",
        "badge": "[E.g., Beste Alternative]",
        "price": "249.00",
        "price_display": "[E.g., 249,00 €]",
        "rating": 9.0,
        "affiliate_slug": "[alternative-slug]"
      }
    ],
    "sections": [
      {
        "title": "[Section 1 title — MUST contain focus keyword or close variant. E.g., 'NiPoGi Mini PC im Praxistest: Verarbeitung & Design']",
        "body": "[300-400 words. Must include: ### sub-headings, **bold** entities, bullet lists, at least 1 internal link, at least 1 hands-on observation starting with 'Wir haben...' or 'Im Test...'. Keyword must appear at least once.]"
      },
      {
        "title": "[Section 2 title — specific, benefit-driven. E.g., 'Alltagsleistung: So schlägt sich der [Product] im Bürobetrieb']",
        "body": "[300-400 words. Same formatting rules. Include measured numbers and specific observations.]"
      },
      {
        "title": "[Section 3 title]",
        "body": "[250-350 words.]"
      },
      {
        "title": "[Section 4 title — E.g., 'Preis-Leistungs-Verhältnis: Lohnt sich der Kauf des [Product]?']",
        "body": "[200-300 words. Compare price to alternatives. State clearly who should and should not buy this.]"
      },
      {
        "title": "[Section 5 title — optional additional section]",
        "body": "[150-250 words.]"
      }
    ],
    "faq": [
      {
        "question": "[PAA question 1 — include focus keyword. E.g., 'Ist der NiPoGi Mini PC für Gaming geeignet?']",
        "answer": "[Start with 'Ja,' or 'Nein,' then explain in 2-3 sentences with specific details.]"
      },
      { "question": "[PAA question 2 — troubleshooting or compatibility]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA question 3 — value/upgrade question]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA question 4]", "answer": "[Ja/Nein + detail]" },
      { "question": "[PAA question 5]", "answer": "[Ja/Nein + detail]" }
    ]
  }
}
```

### Inputs
- Source Link/Product Info: [INSERT PRODUCT SPECIFICATIONS / WEBSITE TEXT COPIED HERE]
- Target Focus Keyword: [INSERT TARGET FOCUS KEYWORD HERE]
- LSI / Secondary Keywords: [INSERT SECONDARY KEYWORDS HERE]
- Reviewer Sliders & POV: [INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH]
- Reviewer Quick Notes: [INSERT ANECDOTAL NOTES HERE]
- Main Category: [INSERT MAIN CATEGORY HERE]
