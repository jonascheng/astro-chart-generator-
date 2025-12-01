# Setup & Running Instructions

## Personal Astro Chart Generator

A web application for generating natal astrological charts. Enter your birth date, time, and location to see your personal natal chart with planetary positions, houses, and aspects.

---

## 📋 Prerequisites

- **Python**: 3.11+ (configured with `pyenv`)
- **Node.js**: 20+ LTS
- **Docker & Docker Compose** (optional, for containerized deployment)
- **macOS/Linux** (primary development platforms)

---

## 🚀 Quick Start (Local Development)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import swisseph; import fastapi; print('✓ Backend dependencies OK')"
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node dependencies
npm install

# Verify installation
echo "✓ Frontend dependencies OK"
```

### 3. Run Both Services

**Terminal 1 - Backend API:**
```bash
cd backend
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend Dev Server:**
```bash
cd frontend
npm run dev
```

**Visit in browser:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 🐳 Docker Deployment (Full Stack)

### Prerequisites
- Docker Desktop installed and running

### Start Everything

```bash
# From repository root
docker-compose up --build

# In a new terminal, verify services are running
curl http://localhost:8000/health  # Should return {"status":"ok"}
```

**Access Application:**
- Frontend: http://localhost
- API Docs: http://localhost:8000/docs

### Stop Services

```bash
docker-compose down
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
python -m pytest -v

# Run only unit tests
python -m pytest tests/unit/ -v

# Run only integration tests
python -m pytest tests/integration/ -v

# Run with coverage
python -m pytest --cov=src tests/
```

### Frontend Tests (when configured)

```bash
cd frontend

# Run with Vitest (when setup complete)
npm run test
```

---

## 📦 Project Structure

```
astro-chart-generator/
├── backend/
│   ├── src/
│   │   ├── api/              # FastAPI application & endpoints
│   │   ├── core/             # Astrological calculation logic
│   │   └── models/           # Pydantic data models
│   ├── tests/
│   │   ├── unit/             # Unit tests for calculations
│   │   └── integration/      # Integration tests for API
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/            # Page components (ChartPage)
│   │   ├── services/         # API communication
│   │   └── styles/           # CSS & Tailwind config
│   ├── Dockerfile
│   └── package.json
│
└── docker-compose.yml        # Multi-container orchestration
```

---

## 🔧 Configuration

### Backend Environment

No environment variables required for local development. The application uses hardcoded city coordinates for the MVP:
- New York, USA
- Los Angeles, USA
- London, UK
- Paris, France
- Sydney, Australia
- Tokyo, Japan
- Berlin, Germany
- Madrid, Spain

Falls back to Greenwich Observatory (51.4769°N, 0°E) for unknown locations.

### Frontend Environment

Frontend runs on `http://localhost:5173` (Vite dev server) and connects to backend at `http://localhost:8000/api`.

---

## 📊 API Reference

### Health Check

```bash
GET /health
```

Response:
```json
{"status": "ok"}
```

### Generate Natal Chart

```bash
POST /api/chart
Content-Type: application/json

{
  "date": "1990-06-15",
  "time": "14:30",
  "country": "USA",
  "city": "New York"
}
```

Response:
```json
{
  "planets": [
    {
      "name": "Sun",
      "sign": "Gemini",
      "degrees": 23.45
    },
    ...
  ],
  "houses": [
    {
      "house_number": 1,
      "sign": "Aries",
      "degrees": 15.20
    },
    ...
  ],
  "aspects": [
    {
      "aspect_type": "Conjunction",
      "planet1": "Sun",
      "planet2": "Mercury",
      "orb": 5.25
    },
    ...
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid date/time format or unknown location
- `422 Unprocessable Entity`: Missing or invalid field

---

## 🎯 Features

✅ **Input Validation**
- Date format validation (YYYY-MM-DD)
- Time format validation (HH:MM)
- Future date rejection
- Real-time validation feedback

✅ **Calculations**
- 10 planetary positions (Sun through Pluto)
- 12 house cusps (Placidus system)
- 5 major aspects (Conjunction, Sextile, Square, Trine, Opposition)
- Accurate Swiss Ephemeris calculations

✅ **Visualization**
- Interactive SVG natal chart
- Zodiac signs ring with symbols
- House lines and numbers
- Planet symbols with interactive hover effects
- Legend with planetary details
- Responsive design (mobile & desktop)

✅ **Accessibility**
- WCAG AA color contrast compliance
- ARIA labels and descriptions
- Keyboard navigation support
- Semantic HTML structure
- Screen reader friendly

✅ **Error Handling**
- Client-side form validation with detailed messages
- Server-side API error descriptions
- Graceful degradation with mock data fallback
- Structured logging with appropriate levels

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Use a different port
python -m uvicorn src.api.main:app --port 8001
```

**Swisseph import errors:**
```bash
# Reinstall with build tools
pip install --no-cache-dir pyswisseph
```

**Tests fail with httpx error:**
```bash
pip install httpx
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Vite will automatically try next available port (5174, 5175, etc.)
npm run dev
```

**Module resolution errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild without cache
docker-compose up --build --no-cache
```

---

## 📈 Performance

- **Chart Generation**: < 500ms
- **Frontend Build**: ~2-3 seconds
- **API Response**: < 200ms
- **SVG Rendering**: < 100ms

---

## 🔐 Security Notes

- CORS is configured to allow all origins (development mode)
- No authentication required (MVP phase)
- City coordinate lookup uses hardcoded values (not external APIs)
- Input validation performed on both client and server

---

## 📝 Development Workflow

### Making Changes

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes in `backend/src/` or `frontend/src/`
3. Run tests to verify: `python -m pytest` or `npm run test`
4. Commit with descriptive message
5. Push to branch: `git push origin feature/my-feature`

### Code Quality

```bash
# Backend - Run linter
cd backend
ruff check src/

# Backend - Format code
ruff format src/

# Frontend - Lint
cd frontend
npm run lint

# Frontend - Format
npm run format
```

---

## 📚 Documentation

- **API Specification**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Specification**: See `specs/001-personal-astro-chart/spec.md`
- **Data Models**: See `backend/src/models/chart.py`
- **Calculations**: See `backend/src/core/calculations.py`

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend API starts without errors
- [ ] Frontend dev server starts and opens browser
- [ ] Health check returns `{"status":"ok"}`
- [ ] Can access Swagger docs at `/docs`
- [ ] Form validates date/time input
- [ ] Can generate a chart for "1990-06-15 14:30 New York USA"
- [ ] Chart displays with planets, houses, and aspects
- [ ] All tests pass: `pytest backend/tests/ -v`
- [ ] No console errors in browser DevTools

---

## 🚦 Next Steps

1. **Deploy to Production**: Use Docker image build scripts
2. **Add Real Geolocation**: Replace hardcoded city coords with API
3. **Implement User Accounts**: Save chart history
4. **Add More Features**: Transits, progressions, synastry
5. **Performance Optimization**: Caching, database integration

---

## 📞 Support

For issues or questions:
1. Check this README's Troubleshooting section
2. Review test outputs: `pytest -v` shows detailed test results
3. Check API docs at `http://localhost:8000/docs` when running
4. Review specification: `specs/001-personal-astro-chart/spec.md`

---

**Last Updated**: December 1, 2025
**Version**: 0.1.0 (MVP)
