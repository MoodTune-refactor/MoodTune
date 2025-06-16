# 🎧 MoodTune Monorepo

MoodTune is a web application that recommends Spotify songs and playlists based on the user's mood, tastes, and preferences. This project is built as a **monorepo using Turborepo**, with a frontend app in React + Vite and a backend app in Flask + Python.

---

## 📦 Project Structure

```
MoodTune/
├── apps/
│   ├── frontend/    # React + Vite + TS + SASS
│   └── backend/     # Flask + Python
├── packages/        # (optional) Shared libraries
├── .gitignore
├── turbo.json
├── package.json     # Shared dev scripts
```

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have installed:

* [Python 3.10+](https://www.python.org/)
* [pnpm](https://pnpm.io/)
* [Node.js 18+](https://nodejs.org/)
* [Git](https://git-scm.com/)

---

### 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/moodtune.git
cd moodtune
```

2. Install the monorepo dependencies:

```bash
pnpm install
```

3. Create virtual environments and `.env` files separately inside each app (see below 👇).

---

## 🧩 Applications

### 🎨 Frontend (`apps/frontend`)

Frontend built with React + Vite + TypeScript + SASS.

#### Useful scripts:

```bash
# Dev (frontend only)
pnpm dev:frontend

# Build
pnpm build --filter=frontend
```

#### `.env` example (`apps/frontend/.env.example`):

```env
VITE_API_URL=http://localhost:5000
VITE_SPOTIFY_CLIENT_ID=your_public_client_id
```

---

### 🔥 Backend (`apps/backend`)

Backend API built with Python and Flask.

#### Setup:

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate         # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
python run.py
```

#### `.env` example (`apps/backend/.env.example`):

```env
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@host/db
SPOTIFY_CLIENT_SECRET=your_private_key
```

---

## 🔄 Unified Development

To run **frontend and backend in parallel**:

```bash
pnpm dev
```

This uses Turborepo to execute both `dev` scripts in parallel. You can customize this in `turbo.json`.

---

## 👩‍💻 Useful Commands

```bash
pnpm dev             # Run frontend and backend together
pnpm dev:frontend    # Run only frontend
pnpm dev:backend     # Run only backend (if defined)
pnpm build           # Build all apps
```

---

## 📜 License

This project is licensed under the MIT License.
