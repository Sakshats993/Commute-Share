# Frontend development

The frontend is a React application built with Vite. It uses React Router, Axios, Tailwind CSS, and Leaflet. See the root [README](../README.md) for full application setup and Compose instructions.

## Local setup

```sh
npm ci
npm run dev
```

Vite serves the app at `http://localhost:5173`. The Axios client defaults to `http://127.0.0.1:8000`. To use another API origin, create `.env.local` in this directory:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The optional `VITE_OSM_TILE_URL` variable changes the Leaflet tile URL. Vite variables are public browser configuration; never place secrets in them. The map displays a straight-line connection and does not provide road routing or travel-time estimates.

## Checks

```sh
npm test
npm run build
```

Tests use Node's built-in test runner (`node --test`). See [API groups](../docs/API_REFERENCE.md) and [known limitations](../docs/ROADMAP.md).
