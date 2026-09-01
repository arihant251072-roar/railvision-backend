# RailVision-AI

Predictive Maintenance and Smart Block Scheduling System for Railway Networks.

## Features

- **AI Predictive Engine**: Calculates track health scores (Green/Orange/Red/Dark Red) based on GMT load, weather, sensor data (TMS/TDMS/SMMS), and inspection logs
- **Smart Scheduling**: Finds "Shadow Blocks" (natural gaps in train timetables) for maintenance using Google OR-Tools CP-SAT solver
- **Emergency Response**: Instant action plans for "Dark Red" failures including KAVACH train halting, alternate routing via Dijkstra/A*, and response team dispatch
- **Real-time WebSocket**: Pushes Dark Red alerts, health updates, and train positions to frontend

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **Optimization**: Google OR-Tools CP-SAT
- **Graph Routing**: NetworkX (Dijkstra/A*)
- **Real-time**: WebSockets
- **Containerization**: Docker & Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Manual Setup

1. **Install PostgreSQL 16+ and Redis 7+**

2. **Create virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Run database migrations (tables auto-create on startup)**
```bash
uvicorn app.main:app --reload
```

5. **Access API docs**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Track Segments
- `POST /api/v1/track-segments` - Create track segment
- `GET /api/v1/track-segments` - List track segments
- `GET /api/v1/track-segments/{id}` - Get track segment
- `PATCH /api/v1/track-segments/{id}` - Update track segment

### Maintenance Tasks
- `POST /api/v1/maintenance-tasks` - Create maintenance task
- `GET /api/v1/maintenance-tasks` - List maintenance tasks

### Trains & Schedules
- `POST /api/v1/trains` - Create train
- `GET /api/v1/trains` - List trains
- `POST /api/v1/train-schedules` - Create train schedule
- `GET /api/v1/train-schedules` - List train schedules

### Junctions & Network
- `POST /api/v1/junctions` - Create junction
- `GET /api/v1/junctions` - List junctions
- `POST /api/v1/track-connections` - Create track connection
- `GET /api/v1/track-connections` - List track connections

### Response Teams
- `POST /api/v1/response-teams` - Create response team
- `GET /api/v1/response-teams` - List response teams

### Sensor Data & Inspections
- `POST /api/v1/sensor-data` - Record sensor reading
- `GET /api/v1/sensor-data` - Get sensor data
- `POST /api/v1/inspection-logs` - Create inspection log
- `GET /api/v1/inspection-logs` - List inspection logs

### AI Predictive Engine
- `POST /api/v1/health-score` - Calculate health score for a segment

**Request:**
```json
{
  "track_segment_id": 1,
  "gmt_load": 25.5,
  "weather_condition": "Heavy Rain",
  "temperature_celsius": 28.0,
  "humidity_percent": 85.0,
  "rainfall_mm": 45.0,
  "wind_speed_kmph": 35.0,
  "sensor_tms_value": 1.2,
  "sensor_tdms_value": 0.8,
  "sensor_smms_value": 0.5,
  "inspection_severity": 0.3
}
```

**Response:**
```json
{
  "track_segment_id": 1,
  "health_score": 0.567,
  "health_status": "Orange",
  "contributing_factors": {
    "gmt_load": 0.7,
    "weather": 0.7,
    "sensors": 0.65,
    "inspection": 0.75
  },
  "recommendation": "Track segment shows early signs of degradation. Schedule preventive maintenance within 30 days. Adverse weather conditions accelerating degradation."
}
```

### Smart Scheduling (Shadow Blocks)
- `POST /api/v1/schedule-block` - Find optimal maintenance window

**Request:**
```json
{
  "track_segment_id": 1,
  "requested_duration_hours": 3.5,
  "preferred_start_time": "2026-09-01T00:00:00Z",
  "maintenance_task_id": 1
}
```

**Response:**
```json
{
  "track_segment_id": 1,
  "track_segment_name": "NDLS-CNB Main Line",
  "requested_duration_hours": 3.5,
  "recommended_windows": [
    {
      "start_time": "2026-09-01T02:30:00Z",
      "end_time": "2026-09-01T06:00:00Z",
      "duration_hours": 3.5,
      "trains_before": 2,
      "trains_after": 5,
      "disruption_score": 0.12
    }
  ],
  "optimal_window": {...},
  "message": "Found 3 potential maintenance windows"
}
```

### Emergency Response
- `POST /api/v1/trigger-emergency` - Trigger emergency response for Dark Red failure

**Request:**
```json
{
  "track_segment_id": 1,
  "failure_type": "OHE Failure",
  "description": "OHE wire snapped at km 45.2",
  "severity": "Critical"
}
```

**Response:**
```json
{
  "alert_id": 42,
  "affected_segment_id": 1,
  "affected_segment_name": "NDLS-CNB Main Line",
  "failure_type": "OHE Failure",
  "trains_to_halt": [
    {
      "train_id": 101,
      "train_number": "12345",
      "train_name": "Rajdhani Express",
      "current_latitude": 28.6139,
      "current_longitude": 77.2090,
      "current_speed_kmph": 85.0,
      "distance_to_segment_km": 12.5,
      "estimated_arrival_minutes": 8.8,
      "current_track_segment_id": 3
    }
  ],
  "alternate_routes": [
    {
      "route_id": "ALT-1-1",
      "junctions": [...],
      "total_distance_km": 45.2,
      "estimated_time_minutes": 52.0,
      "track_segments": [5, 6, 7]
    }
  ],
  "recommended_response_team": {
    "id": 5,
    "team_code": "TW-DLH-01",
    "name": "Tower Wagon Delhi Division",
    "team_type": "Tower Wagon",
    "base_station": "Delhi",
    "base_latitude": 28.6139,
    "base_longitude": 77.2090,
    "contact_number": "+91-11-23456789",
    "contact_person": "Chief OHE Inspector",
    "is_available": true
  },
  "kavach_activated": true,
  "message": "Emergency response activated for OHE Failure on NDLS-CNB Main Line. 1 trains in radius. KAVACH activated."
}
```

### Dashboard
- `GET /api/v1/dashboard/summary` - Get system overview

### WebSocket
- `WS /api/v1/ws/{client_id}?channel=alerts|dashboard|all` - Real-time updates

**Message Types:**
- `dark_red_alert` - Critical failure alerts
- `health_update` - Track health score changes
- `schedule_update` - Maintenance window scheduled
- `train_position` - Train location updates

## Health Score Algorithm

The predictive engine calculates health scores using weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| GMT Load | 25% | Gross Million Tonnes per km |
| Weather | 15% | Temperature, humidity, rainfall, wind |
| Sensors (TMS/TDMS/SMMS) | 45% | Track monitoring system readings |
| Inspection | 15% | Manual inspection severity |

**Thresholds:**
- Green: ≥ 0.8
- Orange: 0.6 - 0.8
- Red: 0.4 - 0.6
- Dark Red: < 0.4

## Failure Type to Response Team Mapping

| Failure Type | Response Team |
|-------------|---------------|
| Track Fracture | Track Engineering |
| OHE Failure | Tower Wagon |
| Signal Failure | Signal & Telecom |
| Points Failure | Signal & Telecom |
| Track Circuit Failure | Signal & Telecom |
| Earthwork Slip | Track Engineering |
| Bridge Issue | Bridge |
| Level Crossing Issue | Signal & Telecom |

## Project Structure

```
railvision-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── predictive_engine.py # AI health scoring
│   ├── scheduler.py         # OR-Tools scheduling
│   ├── emergency.py         # Emergency response
│   ├── websocket.py         # WebSocket manager
│   └── api/
│       ├── __init__.py
│       └── routes.py        # API endpoints
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Format
black app/

# Lint
ruff check app/

# Type check
mypy app/
```

## License

MIT License - Built for SIH 2026