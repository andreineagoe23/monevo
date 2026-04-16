# Monevo — Portfolio site

Single-page portfolio for **Monevo** (craft web design and custom development). Built with React, Vite, Tailwind CSS, Framer Motion, and React Router. Dark-first theme with a warm amber accent; output is built to `docs/` for **GitHub Pages**.

## Features

- Responsive layout (mobile through desktop)
- Dark / light mode toggle (dark default), persisted in `localStorage`
- Scroll-linked ambient background and section animations (Framer Motion)
- Contact section with email, WhatsApp, and a validated form (wire your own endpoint when ready)
- SEO-oriented meta tags in `index.html`

## Tech stack

- **React 19** — UI
- **Vite 7** — dev server and production build
- **Tailwind CSS 3** — styling and design tokens
- **Framer Motion** — motion and scroll effects
- **Lucide React** — icons
- **React Router** — routing (`/` today; easy to add more routes later)

## Project structure

- `src/pages/Home.jsx` — main landing sections
- `src/components/` — Navbar, Hero, Services, Projects, Process, About, Contact, Footer
- `src/components/ui/` — shared primitives (Button, Card, Badge, Section, ParallaxBubbles, …)
- `src/data/projects.js` — project list for the work grid
- `public/` — static assets including `favicon.svg` and `CNAME` for custom domain
- `docs/` — **production build output** (do not hand-edit; regenerate with `npm run build`)

## Getting started

### Prerequisites

- Node.js **20.19+** or **22.12+** (recommended for Vite 7)

### Install and dev

```bash
git clone https://github.com/andreineagoe23/monevo.git
cd monevo
npm install
npm run dev
```

Open `http://localhost:5173`.

### Production build

```bash
npm run build
```

Assets are emitted to `docs/` (see `vite.config.js`). Commit `docs/` when deploying via GitHub Pages from the `docs` folder on `main`.

### Preview the production build

```bash
npm run preview
```

## Deployment (GitHub Pages)

- `package.json` includes `"homepage": "https://www.monevo.tech"`.
- `public/CNAME` contains `www.monevo.tech` for a custom domain; it is copied into `docs/` on build.
- Repository Pages settings: publish from the **`/docs`** folder on your default branch (or adjust to match your workflow).

## Customization

- **Contact email** — `src/components/Contact.jsx` (`EMAIL` constant) and mailto in `src/components/Footer.jsx`
- **Copy and sections** — files under `src/components/` and `src/pages/Home.jsx`
- **Projects** — `src/data/projects.js`
- **Colors / fonts** — `tailwind.config.js` and `src/index.css`

## Scripts

| Command        | Description              |
| -------------- | ------------------------ |
| `npm run dev`  | Start Vite dev server    |
| `npm run build`| Build to `docs/`         |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint               |

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

- **Email:** [neagoeandrei23@gmail.com](mailto:neagoeandrei23@gmail.com)
- **Site:** [monevo.tech](https://www.monevo.tech)

---

Built by Andrei Neagoe
