// Extract markdown tables if data payload is missing
function extractTableFromMarkdown(content) {
  if (!content) return null;
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.includes('|') && line.includes('-') && /^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$/.test(line)) {
      const headerLine = lines[i - 1];
      if (!headerLine || !headerLine.includes('|')) continue;
      const parseRow = (str) => {
        let trimmed = str.trim();
        if (trimmed.startsWith('|')) trimmed = trimmed.slice(1);
        if (trimmed.endsWith('|')) trimmed = trimmed.slice(0, -1);
        return trimmed.split('|').map(s => s.trim());
      };
      const columns = parseRow(headerLine);
      const rows = [];
      for (let j = i + 1; j < lines.length; j++) {
        const rowLine = lines[j].trim();
        if (!rowLine.includes('|')) break;
        rows.push(parseRow(rowLine));
      }
      if (columns.length > 0 && rows.length > 0) return { columns, rows };
    }
  }
  return null;
}

export function parseChartData(data, content = '') {
  let finalData = data;
  
  if (!finalData || !finalData.columns || !finalData.rows || finalData.rows.length === 0) {
      // Try to fallback to markdown parsing
      const extracted = extractTableFromMarkdown(content);
      if (extracted) {
          finalData = extracted;
      } else {
          return { 
              formattedData: [], 
              xKey: null, 
              yKeys: [], 
              suggestedType: 'bar' 
          };
      }
  }

  // 1. Convert to array of objects for Recharts
  const isArrayOfObjects = !Array.isArray(finalData.rows[0]);
  
  let formattedData = [];
  try {
    formattedData = finalData.rows.map((row) => {
      const obj = {};
      finalData.columns.forEach((col, idx) => {
        let val = isArrayOfObjects ? row[col] : row[idx];
        
        // Try to clean string values (e.g., "$4,999.02 B", "1,000", "€ 50")
        if (typeof val === 'string') {
          const cleanStr = val.replace(/[$€£,]/g, '').trim();
          // Check for magnitude suffixes
          let multiplier = 1;
          let numStr = cleanStr;
          
          if (cleanStr.toUpperCase().endsWith('B')) {
             multiplier = 1000000000;
             numStr = cleanStr.slice(0, -1).trim();
          } else if (cleanStr.toUpperCase().endsWith('M')) {
             multiplier = 1000000;
             numStr = cleanStr.slice(0, -1).trim();
          } else if (cleanStr.toUpperCase().endsWith('K')) {
             multiplier = 1000;
             numStr = cleanStr.slice(0, -1).trim();
          }

          const parsed = parseFloat(numStr);
          if (!isNaN(parsed) && isFinite(parsed) && numStr !== '') {
             val = parsed * multiplier;
          }
        }
        
        obj[col] = val;
      });
      return obj;
    });
  } catch (e) {
    console.error("chartParser mapping logic failed:", e);
    return null;
  }

  // 2. Infer column types
  let xKey = null;
  const yKeys = [];

  // Inspect the first row to determine types
  const sampleRow = formattedData[0];
  
      finalData.columns.forEach(col => {
        const val = sampleRow[col];
        if (typeof val === 'number') {
          yKeys.push(col);
        } else {
          if (!xKey) xKey = col; // Assign the first non-number column as X-Axis
        }
      });

  // If no categorical column was found, but we have multiple numeric cols,
  // we might use the first one as X-axis as a fallback.
  if (!xKey && yKeys.length > 1) {
    xKey = yKeys.shift(); 
  }

  // If we still have no yKeys (all strings?), charting might be meaningless here
  if (yKeys.length === 0) {
    return null;
  }

  // 3. Determine Chart Type
  let chartType = 'bar'; // default
  
  if (xKey) {
     const lowerX = xKey.toLowerCase();
     if (lowerX.includes('date') || lowerX.includes('time') || lowerX.includes('year') || lowerX.includes('month')) {
         chartType = 'line';
     } else if (lowerX.includes('percent') || lowerX.includes('ratio')) {
         chartType = 'pie';
     }
  }

  return {
    formattedData,
    xKey,
    yKeys,
    suggestedType: chartType
  };
}
