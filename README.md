# 🎧 MoodTune

MoodTune is a web application that recommends Spotify songs and playlists based on the user's mood, tastes, and preferences. This project is built as a **monorepo using Turborepo**, with a frontend app in React + Vite and a backend app in Flask + Python.

> ⚠️ **Notice!**  
> Although MoodTune is a functional app where you can get your personalized playlists, it's still being refactored and improved for its future production release. This is why you may not experience a smooth user experience, including long loading times or uncontrolled stuttering. We're working on fixing this! You'll soon be able to use a much more efficient version of MoodTune.

---

## 📦 Project Structure

```
MoodTune/
├── apps/
│   ├── frontend/    # React + Vite + TS + SASS
│   └── backend/     # Flask + Python
├── .gitignore
├── turbo.json
└── package.json     # Shared dev scripts
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

**1. Clone the repository:**
  ```bash
  git clone https://github.com/yourusername/moodtune.git
  ```

**2. Install the monorepo dependencies:**
  ```bash
  pnpm install
  ```

---

#### Mount local Backend
**1. Go to backend directory**
  ```bash
  cd apps/backend
  ```

**2. Set Up the Virtual Environment**
  Create and activate a virtual environment:
  
  Windows
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

  macOS/Linux
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Install Dependencies**
  Install the required Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

**4. Configure Environment Variables**
  Create a .env file in the `apps/backend` directory and add the corresponding keys. After that, execute the following command.
  ```
  set FLASK_APP=run.py
  ```

**5. Add the models files**
  Download the files that you can find [here](https://drive.google.com/drive/folders/1i-Mq9OqLtSa0eTa0wxmNM41MtwTsX2eK?usp=sharing) and add it to `apps/backend/src/models`

**6. Run the Application**
  Start the Flask development server:
  ```bash
  python run.py
  ```

The server will be available at [http://127.0.0.1:5000.](http://localhost:5000/)

---

#### Mount local Frontend
**1. Go to frontend directory**
  ```bash
  cd apps/frontend
  ```

**2. Install depencencies**
  ```bash
  pnpm install
  ```

**5. Run the Application**
  Start the Flask development server:
  ```bash
  pnpm dev
  ```

The frontend will be available at [http://127.0.0.1:5173.](http://localhost:5173/)

---

## 📜 License

This project is licensed under the MIT License.
