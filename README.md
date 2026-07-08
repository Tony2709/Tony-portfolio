# Tony Quang — Portfolio

Personal portfolio site for Tony Quang, built with [Astro](https://astro.build) + Tailwind CSS.

## Stack

- **Astro** (static output — no server runtime required at deploy time)
- **Tailwind CSS v4** for styling
- **@astrojs/sitemap** for SEO

## Commands

Run from the project root:

| Command             | Action                                       |
| :------------------- | :-------------------------------------------- |
| `npm install`         | Install dependencies                          |
| `npm run dev`         | Start local dev server at `localhost:4321`    |
| `npm run build`       | Build the production site to `./dist/`        |
| `npm run preview`     | Preview the production build locally          |

## Content

All site copy lives in [`src/data/content.ts`](./src/data/content.ts) — edit that file to update text without touching component markup. Photos live in `src/assets/`.

> **Note:** The featured case study currently anonymises the client as "a sports nutrition & performance coaching practice (Sunshine Coast, QLD)" per the source content notes. If the client has confirmed they're happy being named, update `caseStudy.client` and remove `caseStudy.clientNote` in `src/data/content.ts`.

Before going live, also update `SITE_URL` in [`astro.config.mjs`](./astro.config.mjs) and the `Sitemap:` line in [`public/robots.txt`](./public/robots.txt) to your real domain.

## Deploying to Hostinger

This repo auto-deploys to Hostinger via FTP on every push to `main` (see [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)). It builds the site with `npm run build` and uploads the contents of `dist/` to your Hostinger hosting.

**One-time setup:**

1. In Hostinger's hPanel, go to **Files → FTP Accounts** and note (or create) an FTP account with access to the folder you want to publish to (usually `public_html/` for your primary domain, or `domains/yourdomain.com/public_html/` for an addon domain).
2. In your GitHub repo, go to **Settings → Secrets and variables → Actions** and add these repository secrets:
   - `FTP_SERVER` — your Hostinger FTP host (e.g. `ftp.yourdomain.com` or the IP shown in hPanel)
   - `FTP_USERNAME` — the FTP account username
   - `FTP_PASSWORD` — the FTP account password
   - `FTP_SERVER_DIR` — the target directory on the server (e.g. `/public_html/`)
3. Push to `main` — the workflow builds and uploads automatically. Check the **Actions** tab for progress/logs.

To deploy manually instead: run `npm run build` and upload the contents of `dist/` via Hostinger's File Manager or an FTP client (e.g. FileZilla).
