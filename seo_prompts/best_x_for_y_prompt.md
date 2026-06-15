You are an expert copywriter. Your task is to generate a comprehensive, highly optimized listicle review ("Best X for Y") in German. The final output must be returned as a single, valid JSON object containing all meta fields and the structured content block.

### SEO & Layout Guidelines
1. Length & Readability (CRITICAL): The combined text inside the product summaries and the "buying_guide" section must be around 800 to 1000 words maximum total (to keep the final article length concise and punchy).
   - Crucially, avoid bloated, repetitive wall-of-text paragraphs or generic fluff/filler sentences designed merely to pad word counts.
   - **Paragraph Max Length**: Every single paragraph inside the product summaries, reviews, and buying guide MUST be extremely short: **1 to 2 sentences max, and under 30 words total** (literally cut paragraph lengths to 1/3 of typical AI output).
   - **Paragraph Count Limit**: Each product summary must contain exactly 3 to 4 short paragraphs. The buying guide must contain exactly 4 to 6 short paragraphs. Do not exceed these limits.
   - Break down all concepts into brief, bite-sized paragraphs separated by double newlines (`\n\n`) so they render cleanly.
   - Mandate the use of structured lists (bullet points or numbered lists), inline subheaders (e.g., `### Subheading`), and bold text highlights (`**bold**`) to keep the layout engaging, scannable, and professional. Look at how high-quality reviews are written: they use bullet points for lists of points, and short, punchy paragraphs.
2. Focus Keyword: The target focus keyword is: "[INSERT_FOCUS_KEYWORD]" (e.g., "best 4k monitors programming").
3. LSI / Secondary Keywords: Integrate these semantic keywords naturally inside headers and paragraph text: "[INSERT_LSI_KEYWORDS]".
4. Entity Density (NLP): Identify core technical entities and terms from the specifications context (e.g., `IPS Black`, `Thunderbolt 4`, `PPI`, `HDR`) and include each entity term naturally at least twice inside the product summaries and buying guide.
5. Keyword Placement:
   - Must appear near the beginning of the "title" and "meta_title".
   - Must appear in the "meta_description" (150-160 characters limit).
   - Must appear in the "slug" and the first paragraph of the "sub_head".
   - Must appear in at least two product reviews or the buying guide.
6. Internal Linking (CRITICAL): You MUST insert at least 2-3 do-follow internal links (using standard Markdown format: `[Anchor Text](/blog/slug)`) directly inside the paragraph bodies of your sections.
   - Prioritize linking to the main blog page `/blog` or contextually relevant post paths provided in the "SILO INTERNAL LINKS POOL".
   - Ensure these links are naturally integrated into the flow of sentences with keyword-rich, descriptive anchor text. Do NOT use generic anchor text.
   - If no specific post from the links pool fits the context, you MUST insert a natural link to the general reviews page: `[Testberichten](/blog)` or `[unserer Übersicht](/blog)`.
7. Heading Neutralization: Avoid using generic AI-like headings such as "Schlussfolgerung" or "Conclusion" for your final section. Use localized, context-appropriate headings like "Fazit: Unser Testurteil" or "Unser Fazit".
8. Brand Tone: Write in a professional, engaging editorial tone using German "Du" (informal) or "Wir" (editorial). Do NOT use formal "Sie" address.
9. Specifications Completeness (CRITICAL):
   - For EACH product, you MUST extract and list ALL specifications/features provided in the inputs for that product (typically 10-15 specs). Do NOT truncate or summarize.
   - Format each entry strictly as a string in the pattern "Key: Value" (e.g., "Auflösung: 3840 x 2160", "Panel-Typ: IPS Black").
   - Do NOT skip any spec from the inputs. Every specification listed in the input specs list for a product must have a corresponding row in that product's "specs" JSON array.


### ⚠️ CRITICAL: JSON Integrity & Quote Escaping Rules
To prevent broken JSON syntax and output generation cuts:
* **Markdown-First for Text Fields**: Use strictly standard Markdown (e.g., `###` for sub-headings, `**bold**`, bullet lists, and links `[Anchor Text](url)`) inside the `products[].summary` and `buying_guide` fields. Do NOT use HTML tags. The layout renders these fields using Flask's dynamic `| markdown` filter, ensuring JSON stability.
* **Double Quotes in Text**: Any double quotes inside text strings must be escaped with a backslash (`\"`) or replaced with single quotes.
* **Line Breaks**: Use standard `\n` for line breaks within JSON text fields. Never use unescaped physical newlines.
* **Price Value**: Provide all `price` fields strictly in clean decimal string format (e.g., `749.00` or `449.00`), without any currency symbols (€, $, £).
* **German Decimal Protocol**: For pricing, separate the machine raw price (`price`: clean decimal string, e.g., `749.00`) from the formatted German price display (`price_display`: formatted string, e.g., `749,00 €` or `ab 749,00 €`).
* **Specification Invariants**: Ensure all specifications, ratings, and features inside the product summaries, specs lists, and comparison tables are 100% consistent with each other. Do not hallucinate or contradict specs. Use the provided features context contextually.
* **Mobile-First Table Constraint**: Limit the `comparison_table` headers to a maximum of 6 columns total (including Modell and Preis). Select the top 4 specifications that buyers care most about (e.g., Kapazität, Geschwindigkeit, Garantie, etc.) as the core columns to ensure mobile responsiveness and pass Google's Mobile Usability audit. Do NOT exceed 6 columns.
* **PAA FAQ Logic (CRITICAL)**: You MUST generate EXACTLY 5 relevant questions total that people frequently look for answers to in Google search (PAA). The FAQ list must contain at least one troubleshooting or compatibility question (e.g. 'Wie installiere ich...' or 'Ist X kompatibel mit...') and at least one value/upgrade question (e.g. 'Lohnt sich der Aufpreis für...').

### JSON Output Format
Return ONLY the raw JSON object matching this structure:

```json
{
  "title": "[Listicle Title, e.g. Die 5 besten 4K-Monitore für Programmierer 2026]",
  "slug": "[URL slug, e.g., the-5-best-4k-monitors-for-programming-2026]",
  "excerpt": "[120-150 characters summary of the listicle]",
  "template": "best_x_for_y_template",
  "status": "published",
  "category": "[Category, e.g., Office]",
  "tags": [ [array of tags in lowercase] ],
  "read_time": [estimated read time, e.g., 11],
  "meta_title": "[SEO Meta Title: 50-60 characters, keyword near start]",
  "meta_description": "[SEO Meta Description: 150-160 characters, high CTR call-to-action]",
  "focus_keyword": "[The target focus keyword]",
  "cover_image_url": "[High-res main image URL]",
  
  "structured_content": {
    "headline": "[Listicle Title]",
    "sub_head": "[A brief, punchy intro of max 1-2 short sentences (under 30 words total). Do NOT make it a long paragraph. E.g., 'In unserem Praxistest haben wir die besten 4K-Monitore für Programmierer verglichen. Hier ist unsere Übersicht.']",
    "author_name": "[Author Name]",
    "author_bio": "[Author credentials, e.g., Hardware-Tester · 8 Jahre Erfahrung]",
    "image_alt_text": "[Keyword-optimized descriptive alt text for the main cover image]",
    "products": [
      {
        "rank": 1,
        "name": "[Product 1 Name]",
        "badge": "[e.g., Testsieger & Beste Bildqualität]",
        "price": "749.00",
        "price_display": "[Formatted German price string, e.g., 749,00 €]",
        "rating": 9.9,
        "affiliate_slug": "[affiliate-link-slug, e.g., dell-u3224kb]",
        "image_url": "[Product image URL]",
        "image_alt_text": "[Descriptive alt text for the product image]",
        "summary": "[In-depth review. MUST follow these formatting rules: 1. Max 1-2 sentences or 30 words per paragraph (cut paragraph length to 1/3). 2. Use ### for sub-headers within the summary to label sub-topics. 3. Bold (**term**) all technical entities and specs. 4. Include at least one bulleted list (- ) of key takeaways or observations. 5. Integrate reviewer observations and sliders naturally. Keep it highly scannable, and avoid repetitive fluff.]",
        "pros": [ "[Pro 1]", "[Pro 2]" ],
        "cons": [ "[Con 1]" ],
        "specs": [ "[CRITICAL: Include ALL specifications provided in the input specs list for this product. Do not truncate. Format strictly as 'Key: Value', e.g., 'Auflösung: 3840 x 2160']" ]
      },
      {
        "rank": 2,
        "name": "[Product 2 Name]",
        "badge": "[e.g., Preistipp]",
        "price": "449.00",
        "price_display": "[e.g. 449,00 €]",
        "rating": 9.5,
        "affiliate_slug": "[affiliate-slug]",
        "image_url": "[Product image]",
        "image_alt_text": "[Descriptive alt text for the product image]",
        "summary": "[In-depth review. MUST follow these formatting rules: 1. Max 1-2 sentences or 30 words per paragraph (cut paragraph length to 1/3). 2. Use ### for sub-headers to label sub-topics. 3. Bold (**term**) all technical entities and specs. 4. Include at least one bulleted list (- ) of key takeaways. Keep it scannable and avoid fluff.]",
        "pros": [ "[Pro 1]" ],
        "cons": [ "[Con 1]" ],
        "specs": [ "[CRITICAL: Include ALL specifications provided in the input specs list for this product. Do not truncate. Format strictly as 'Key: Value']" ]
      }
    ],
    "buying_guide": "[Comprehensive buying guide detailing panels, ergonomics, specs to look for. Must be at least 500 words long. MUST follow readability rules: 1. Max 1-2 sentences or 30 words per paragraph (cut paragraph length to 1/3). 2. Use ### for sub-headers. 3. Use **bolding** for key terms and findings. 4. Use bulleted lists (- ) or numbered lists (1. ) extensively. 5. ONLY include internal links if they naturally fit in the text, DO NOT force them and NEVER create a 'Verwandte Artikel' list. Avoid bloated wall-of-text paragraphs.]",
    "comparison_table": {
      "headers": [
        "Modell",
        "Eignung / Badge",
        "Panel-Typ",
        "Auflösung",
        "Preis"
      ],
      "rows": [
        [
          "[Product 1 Name]",
          "[Product 1 Badge]",
          "[Product 1 Panel-Typ]",
          "[Product 1 Auflösung]",
          "[Product 1 Price Display]"
        ],
        [
          "[Product 2 Name]",
          "[Product 2 Badge]",
          "[Product 2 Panel-Typ]",
          "[Product 2 Auflösung]",
          "[Product 2 Price Display]"
        ]
      ]
    },
    "faq": [
      {
        "question": "[Google search query FAQ 1. Must include at least one troubleshooting/compatibility question and one value/upgrade question. E.g. 'Ist X kompatibel mit...']",
        "answer": "[FAQ Answer 1. Must start with a direct 'Ja,' or 'Nein,' followed immediately by a clear one-sentence explanation, before expanding into detail to act as Google Featured Snippet-Bait]"
      },
      { "question": "[Google search query FAQ 2]", "answer": "[Direct answer starting with Ja/Nein]" },
      { "question": "[Google search query FAQ 3]", "answer": "[Direct answer starting with Ja/Nein]" },
      { "question": "[Google search query FAQ 4]", "answer": "[Direct answer starting with Ja/Nein]" },
      { "question": "[Google search query FAQ 5]", "answer": "[Direct answer starting with Ja/Nein]" }
    ],
    "verdict": "[Final verdict summary comparing the products and recommending who should buy what. MUST be extremely brief: max 2-3 short sentences. The first sentence must start with '[Product/Category Name] sind...' or similar to act as Google Featured Snippet-Bait. Plain text only.]"
  }
}
```

### Inputs
- Source Link/Product Info: [INSERT PRODUCT SPECIFICATIONS / WEBSITE TEXT COPIED HERE]
- Target Focus Keyword: [INSERT TARGET FOCUS KEYWORD HERE]
- LSI / Secondary Keywords: [INSERT SECONDARY KEYWORDS HERE]
- Reviewer Sliders & POV (Optional per product): [INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH RANK]
- Reviewer Quick Notes (Optional per product): [INSERT ANECDOTAL NOTES FOR EACH RANK]
- Main Category: [INSERT MAIN CATEGORY HERE]
