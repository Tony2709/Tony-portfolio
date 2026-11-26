// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

import react from '@astrojs/react';

// TODO: replace with your real domain once connected on Hostinger
const SITE_URL = 'https://tonyquang.com';

// https://astro.build/config
export default defineConfig({
  site: SITE_URL,
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'vi'],
  },
  integrations: [sitemap(), react()],
  vite: {
    plugins: [tailwindcss()],
    // Astro loads react-dom/client itself to hydrate the island, so Vite's scan never sees that import and
    // serves the raw CommonJS file in dev, which has no named exports. Naming it here gets it pre-bundled.
    optimizeDeps: {
      include: ["react", "react-dom", "react-dom/client", "react/jsx-runtime"],
    },
  },
});