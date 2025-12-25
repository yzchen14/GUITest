# PyWebView + FastAPI + React App

A desktop application template using PyWebView for the GUI, FastAPI for the backend, and React for the frontend.

## Project Structure

```
├── main.py                 # Entry point - starts backend and launches PyWebView
├── requirements.txt        # Python dependencies for pywebview
├── backend/
│   ├── main.py            # FastAPI application
│   └── requirements.txt    # Python dependencies for FastAPI
└── frontend/
    ├── package.json       # React dependencies
    ├── public/
    │   └── index.html     # HTML entry point
    └── src/
        ├── App.js         # Main React component
        ├── App.css        # Styles
        ├── index.js       # React DOM render
        └── index.css      # Global styles
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
# Install pywebview and other root dependencies
pip install -r requirements.txt

# Install FastAPI backend dependencies
pip install -r backend/requirements.txt
```

### 2. Setup React Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 3. Build the Frontend (Production)

```bash
cd frontend
npm run build
```

This creates an optimized build in `frontend/build/` that will be served by FastAPI.

## Running the Application

### Option 1: Production Mode (Recommended)

```bash
# Build React frontend first
cd frontend
npm run build
cd ..

# Run the desktop app
python main.py
```

### Option 2: Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Then open your browser to `http://localhost:3000`

## Development

- **Backend**: Edit files in `backend/main.py` and restart the server
- **Frontend**: Edit files in `frontend/src/` and the dev server will hot-reload
- **API Endpoints**: Available at `http://127.0.0.1:8000/api/*`

## Adding More API Routes

Edit `backend/main.py`:

```python
@app.get("/api/new-endpoint")
async def new_endpoint():
    return {"data": "your response"}
```

## Troubleshooting

- **Port 8000 already in use**: Change the port in `backend/main.py` and update the URL in `main.py`
- **Frontend not loading**: Make sure to run `npm run build` in the frontend folder
- **CORS issues**: FastAPI is configured to serve the React build directly, which avoids CORS

## Next Steps

- Add database integration (SQLAlchemy, MongoDB, etc.)
- Implement authentication/authorization
- Add more complex React components and pages
- Create additional FastAPI routes
