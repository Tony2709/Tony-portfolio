import sharp from "sharp";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");

const width = 1200;
const height = 630;

const svg = `
<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f0e1a" />
      <stop offset="100%" stop-color="#1e1b4b" />
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#bg)" />
  <circle cx="1000" cy="480" r="360" fill="#4338ca" opacity="0.4" />
  <circle cx="1050" cy="150" r="220" fill="#818cf8" opacity="0.3" />
  <text x="80" y="260" font-family="Georgia, serif" font-size="72" font-weight="700" fill="#f3efe6">Tony Quang</text>
  <text x="80" y="320" font-family="Arial, sans-serif" font-size="34" fill="#818cf8">Digital Marketer: Content, SEO &amp; AI-Assisted Growth</text>
  <text x="80" y="400" font-family="Arial, sans-serif" font-size="26" fill="#b9b2a4">Sydney, Australia</text>
  <rect x="80" y="440" width="120" height="6" rx="3" fill="#818cf8" />
</svg>
`;

await sharp(Buffer.from(svg)).png().toFile(path.join(root, "public", "og-image.png"));

console.log("OG image written to public/og-image.png");
