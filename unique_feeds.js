const xlsx = require('xlsx');
const workbook = xlsx.readFile('/Users/shivanshusharma/Downloads/UP Copy of News Sources _ NFOWR _ Field Teams, Apr 2025.xlsx');
let feeds = new Set();
let domains = new Set();
for (const sheetName of ['Sources']) {
  const sheet = workbook.Sheets[sheetName];
  const data = xlsx.utils.sheet_to_json(sheet);
  data.forEach(r => {
    let url = r['RSS Feed URL'] || r['RSS Feed Link'];
    if (url && url.startsWith('http')) {
      feeds.add(url.trim());
      try { domains.add(new URL(url.trim()).hostname); } catch(e) {}
    }
  });
}
console.log("Unique Feeds:", feeds.size);
console.log("Unique Domains:", domains.size);
console.log(Array.from(domains));
