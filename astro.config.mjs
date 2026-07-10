// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// TODO: replace with your real domain once connected on Hostinger
const SITE_URL = 'https://tonyquang.com';

// https://astro.build/config
export default defineConfig({
  site: SITE_URL,
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'vi'],
  },
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});

