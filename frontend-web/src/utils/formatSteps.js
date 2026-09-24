/**
 * Helper to ensure Steps (1, 2, 3, 4...), bullet items, sub-points, and sections
 * render line-by-line rather than merged into a single paragraph.
 */
export function formatStepsLineByLine(text) {
  if (!text || typeof text !== 'string') return text || '';

  let res = text;

  // 1. Separate Step headers (Step 1, Step 2, படி 1, படி 2, चरण 1, चरण 2, etc.)
  // Ensure double newlines before and after each Step item
  res = res.replace(
    /([^\n])\s*(•\s*\*\*Step\s*\d+[^:]*:\*\*|•\s*Step\s*\d+[^:]*:|\*\*Step\s*\d+[^:]*:\*\*|Step\s*\d+[^:]*:|•\s*\*\*படி\s*\d+[^:]*:\*\*|•\s*படி\s*\d+[^:]*:|\*\*படி\s*\d+[^:]*:\*\*|படி\s*\d+[^:]*:|•\s*\*\*चरण\s*\d+[^:]*:\*\*|•\s*चरण\s*\d+[^:]*:|\*\*चरण\s*\d+[^:]*:\*\*|चरण\s*\d+[^:]*:)/gi,
    '$1\n\n$2'
  );

  // 2. Separate numbered points like "1. ", "2. ", "3. ", "4. " inline in paragraphs
  res = res.replace(/([^\n])\s+(\d+\.\s+)/g, '$1\n\n$2');

  // 3. Separate bullet items (•, -, *) that follow text without blank lines
  res = res.replace(/([^\n])\n([•\-\*]\s+)/g, '$1\n\n$2');

  // 4. Ensure sub-bullet points like "  - **For Name..." are clean on separate lines
  res = res.replace(/([^\n])\n(\s+-\s+)/g, '$1\n\n$2');

  // 5. Ensure major sections with emojis start on their own clean blocks
  res = res.replace(/([^\n])\s*([🏢👤📝🏛️🌾💳📌⚠️⚖️🪜📁📜]\s*\*\*)/g, '$1\n\n$2');

  return res;
}
