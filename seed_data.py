#!/usr/bin/env python3
"""
Seed script to populate database with sample data for RailVision-AI.
Run with: python seed_data.py
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import (
    Base, TrackSegment, Train, TrainSchedule, Junction, TrackConnection,
    ResponseTeam, MaintenanceTask, SensorData, InspectionLog,
    HealthStatus, TaskUrgency, FailureType, ResponseTeamType
)


async def seed_data():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        # Create Junctions
        junctions = [
            Junction(code="NDLS", name="New Delhi", latitude=28.6562, longitude=77.2410, station_type="Major"),
            Junction(code="CNB", name="Kanpur Central", latitude=26.4499, longitude=80.3319, station_type="Major"),
            Junction(code="ALD", name="Prayagraj Junction", latitude=25.4358, longitude=81.8463, station_type="Major"),
            Junction(code="MGS", name="Mughalsarai", latitude=25.2795, longitude=83.1234, station_type="Major"),
            Junction(code="GZB", name="Ghaziabad", latitude=28.6692, longitude=77.4538, station_type="Junction"),
            Junction(code="TDL", name="Tundla Junction", latitude=27.2144, longitude=78.2856, station_type="Junction"),
            Junction(code="ETW", name="Etawah", latitude=26.7744, longitude=79.0139, station_type="Station"),
            Junction(code="FZD", name="Firozabad", latitude=27.1592, longitude=78.3957, station_type="Station"),
            Junction(code="SKB", name="Shikohabad", latitude=27.1025, longitude=78.5803, station_type="Station"),
            Junction(code="CNB2", name="Kanpur Anwarganj", latitude=26.4724, longitude=80.3243, station_type="Station"),
        ]
        
        for j in junctions:
            db.add(j)
        await db.flush()
        
        # Create Track Segments
        segments = [
            TrackSegment(
                segment_code="NDLS-GZB-01",
                name="New Delhi - Ghaziabad Main Line",
                start_station="NDLS", end_station="GZB",
                length_km=25.5, capacity_trains_per_hour=30,
                current_health_score=0.85, health_status=HealthStatus.GREEN,
                gmt_load=18.5,
                latitude_start=28.6562, longitude_start=77.2410,
                latitude_end=28.6692, longitude_end=77.4538,
            ),
            TrackSegment(
                segment_code="GZB-TDL-01",
                name="Ghaziabad - Tundla Main Line",
                start_station="GZB", end_station="TDL",
                length_km=180.2, capacity_trains_per_hour=25,
                current_health_score=0.62, health_status=HealthStatus.ORANGE,
                gmt_load=28.3,
                latitude_start=28.6692, longitude_start=77.4538,
                latitude_end=27.2144, longitude_end=78.2856,
            ),
            TrackSegment(
                segment_code="TDL-CNB-01",
                name="Tundla - Kanpur Main Line",
                start_station="TDL", end_station="CNB",
                length_km=220.8, capacity_trains_per_hour=20,
                current_health_score=0.38, health_status=HealthStatus.RED,
                gmt_load=35.7,
                latitude_start=27.2144, longitude_start=78.2856,
                latitude_end=26.4499, longitude_end=80.3319,
            ),
            TrackSegment(
                segment_code="CNB-ALD-01",
                name="Kanpur - Prayagraj Main Line",
                start_station="CNB", end_station="ALD",
                length_km=195.3, capacity_trains_per_hour=22,
                current_health_score=0.15, health_status=HealthStatus.DARK_RED,
                gmt_load=42.1,
                latitude_start=26.4499, longitude_start=80.3319,
                latitude_end=25.4358, longitude_end=81.8463,
            ),
            TrackSegment(
                segment_code="ALD-MGS-01",
                name="Prayagraj - Mughalsarai Main Line",
                start_station="ALD", end_station="MGS",
                length_km=165.4, capacity_trains_per_hour=24,
                current_health_score=0.72, health_status=HealthStatus.GREEN,
                gmt_load=22.8,
                latitude_start=25.4358, longitude_start=81.8463,
                latitude_end=25.2795, longitude_end=83.1234,
            ),
        ]
        
        for s in segments:
            db.add(s)
        await db.flush()
        
        # Create Track Connections
        connections = [
            TrackConnection(from_junction_id=1, to_junction_id=5, track_segment_id=1, distance_km=25.5, max_speed_kmph=130, is_bidirectional=True),
            TrackConnection(from_junction_id=5, to_junction_id=6, track_segment_id=2, distance_km=180.2, max_speed_kmph=110, is_bidirectional=True),
            TrackConnection(from_junction_id=6, to_junction_id=2, track_segment_id=3, distance_km=220.8, max_speed_kmph=110, is_bidirectional=True),
            TrackConnection(from_junction_id=2, to_junction_id=3, track_segment_id=4, distance_km=195.3, max_speed_kmph=110, is_bidirectional=True),
            TrackConnection(from_junction_id=3, to_junction_id=4, track_segment_id=5, distance_km=165.4, max_speed_kmph=130, is_bidirectional=True),
            # Alternative route connections
            TrackConnection(from_junction_id=1, to_junction_id=7, track_segment_id=1, distance_km=320.0, max_speed_kmph=100, is_bidirectional=True),
            TrackConnection(from_junction_id=7, to_junction_id=8, track_segment_id=2, distance_km=45.0, max_speed_kmph=100, is_bidirectional=True),
            TrackConnection(from_junction_id=8, to_junction_id=9, track_segment_id=3, distance_km=38.0, max_speed_kmph=100, is_bidirectional=True),
            TrackConnection(from_junction_id=9, to_junction_id=2, track_segment_id=4, distance_km=52.0, max_speed_kmph=100, is_bidirectional=True),
        ]
        
        for c in connections:
            db.add(c)
        
        # Create Trains
        trains = [
            Train(train_number="12301", train_name="Rajdhani Express", train_type="Rajdhani", max_speed_kmph=130, length_meters=600),
            Train(train_number="12302", train_name="Rajdhani Express", train_type="Rajdhani", max_speed_kmph=130, length_meters=600),
            Train(train_number="12309", train_name="Shatabdi Express", train_type="Shatabdi", max_speed_kmph=150, length_meters=400),
            Train(train_number="12310", train_name="Shatabdi Express", train_type="Shatabdi", max_speed_kmph=150, length_meters=400),
            Train(train_number="11015", train_name="Kushinagar Express", train_type="Mail/Express", max_speed_kmph=110, length_meters=550),
            Train(train_number="11016", train_name="Kushinagar Express", train_type="Mail/Express", max_speed_kmph=110, length_meters=550),
            Train(train_number="12565", train_name="Bihar Sampark Kranti", train_type="Superfast", max_speed_kmph=110, length_meters=500),
            Train(train_number="12566", train_name="Bihar Sampark Kranti", train_type="Superfast", max_speed_kmph=110, length_meters=500),
            Train(train_number="14005", train_name="Saryu Yamuna Express", train_type="Express", max_speed_kmph=100, length_meters=450),
            Train(train_number="14006", train_name="Saryu Yamuna Express", train_type="Express", max_speed_kmph=100, length_meters=450),
        ]
        
        for t in trains:
            db.add(t)
        await db.flush()
        
        # Create Train Schedules (next 7 days)
        now = datetime.utcnow()
        base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        schedules_data = [
            # NDLS-GZB segment
            (1, 1, 1, base_date + timedelta(hours=6, minutes=0), base_date + timedelta(hours=6, minutes=5)),
            (1, 2, 2, base_date + timedelta(hours=6, minutes=30), base_date + timedelta(hours=6, minutes=35)),
            (1, 3, 1, base_date + timedelta(hours=7, minutes=0), base_date + timedelta(hours=7, minutes=5)),
            (1, 5, 2, base_date + timedelta(hours=8, minutes=0), base_date + timedelta(hours=8, minutes=5)),
            (1, 7, 1, base_date + timedelta(hours=9, minutes=0), base_date + timedelta(hours=9, minutes=5)),
            (1, 9, 2, base_date + timedelta(hours=10, minutes=0), base_date + timedelta(hours=10, minutes=5)),
            
            # GZB-TDL segment
            (2, 1, 2, base_date + timedelta(hours=8, minutes=30), base_date + timedelta(hours=8, minutes=35)),
            (2, 2, 1, base_date + timedelta(hours=9, minutes=0), base_date + timedelta(hours=9, minutes=5)),
            (2, 3, 2, base_date + timedelta(hours=9, minutes=30), base_date + timedelta(hours=9, minutes=35)),
            (2, 5, 1, base_date + timedelta(hours=10, minutes=30), base_date + timedelta(hours=10, minutes=35)),
            (2, 7, 2, base_date + timedelta(hours=11, minutes=30), base_date + timedelta(hours=11, minutes=35)),
            (2, 9, 1, base_date + timedelta(hours=12, minutes=30), base_date + timedelta(hours=12, minutes=35)),
            
            # TDL-CNB segment
            (3, 1, 3, base_date + timedelta(hours=13, minutes=0), base_date + timedelta(hours=13, minutes=10)),
            (3, 2, 4, base_date + timedelta(hours=14, minutes=0), base_date + timedelta(hours=14, minutes=10)),
            (3, 5, 3, base_date + timedelta(hours=16, minutes=0), base_date + timedelta(hours=16, minutes=10)),
            (3, 7, 4, base_date + timedelta(hours=18, minutes=0), base_date + timedelta(hours=18, minutes=10)),
            
            # CNB-ALD segment
            (4, 1, 4, base_date + timedelta(hours=17, minutes=0), base_date + timedelta(hours=17, minutes=15)),
            (4, 3, 3, base_date + timedelta(hours=20, minutes=0), base_date + timedelta(hours=20, minutes=15)),
            (4, 5, 4, base_date + timedelta(hours=22, minutes=0), base_date + timedelta(hours=22, minutes=15)),
            
            # ALD-MGS segment
            (5, 1, 5, base_date + timedelta(hours=21, minutes=0), base_date + timedelta(hours=21, minutes=10)),
            (5, 3, 6, base_date + timedelta(hours=23, minutes=0), base_date + timedelta(hours=23, minutes=10)),
            (5, 7, 5, base_date + timedelta(days=1, hours=1, minutes=0), base_date + timedelta(days=1, hours=1, minutes=10)),
        ]
        
        for i, (seg_id, train_id, seq, arr, dep) in enumerate(schedules_data):
            db.add(TrainSchedule(
                train_id=train_id,
                track_segment_id=seg_id,
                sequence_order=seq,
                scheduled_arrival=arr,
                scheduled_departure=dep,
                current_latitude=None,
                current_longitude=None,
                current_speed_kmph=0.0,
                is_running=False,
            ))
        
        # Add some running trains with positions
        running_trains = [
            (1, 1, 1, 28.65, 77.25, 95.0),
            (2, 2, 1, 28.66, 77.35, 105.0),
            (3, 5, 2, 27.80, 77.90, 110.0),
            (4, 7, 3, 27.00, 78.20, 100.0),
            (4, 1, 4, 26.80, 79.50, 85.0),
        ]
        
        for seg_id, train_id, seq, lat, lon, speed in running_trains:
            db.add(TrainSchedule(
                train_id=train_id,
                track_segment_id=seg_id,
                sequence_order=seq,
                scheduled_arrival=now + timedelta(minutes=30),
                scheduled_departure=now + timedelta(minutes=35),
                current_latitude=lat,
                current_longitude=lon,
                current_speed_kmph=speed,
                is_running=True,
            ))
        
        # Create Response Teams
        teams = [
            ResponseTeam(
                team_code="TE-DLH-01",
                name="Track Engineering Delhi Division",
                team_type=ResponseTeamType.TRACK_ENGINEERING,
                base_station="New Delhi",
                base_latitude=28.6562,
                base_longitude=77.2410,
                contact_number="+91-11-23456789",
                contact_person="Senior DEN/Track",
                is_available=True,
            ),
            ResponseTeam(
                team_code="TE-CNB-01",
                name="Track Engineering Kanpur Division",
                team_type=ResponseTeamType.TRACK_ENGINEERING,
                base_station="Kanpur",
                base_latitude=26.4499,
                base_longitude=80.3319,
                contact_number="+91-512-2345678",
                contact_person="DEN/Track Kanpur",
                is_available=True,
            ),
            ResponseTeam(
                team_code="ST-DLH-01",
                name="Signal & Telecom Delhi Division",
                team_type=ResponseTeamType.SIGNAL_TELECOM,
                base_station="New Delhi",
                base_latitude=28.6562,
                base_longitude=77.2410,
                contact_number="+91-11-23456790",
                contact_person="Sr. DSTE",
                is_available=True,
            ),
            ResponseTeam(
                team_code="TW-DLH-01",
                name="Tower Wagon Delhi Division",
                team_type=ResponseTeamType.TOWER_WAGON,
                base_station="New Delhi",
                base_latitude=28.6562,
                base_longitude=77.2410,
                contact_number="+91-11-23456791",
                contact_person="Chief OHE Inspector",
                is_available=True,
            ),
            ResponseTeam(
                team_code="TW-CNB-01",
                name="Tower Wagon Kanpur Division",
                team_type=ResponseTeamType.TOWER_WAGON,
                base_station="Kanpur",
                base_latitude=26.4499,
                base_longitude=80.3319,
                contact_number="+91-512-2345679",
                contact_person="OHE Inspector Kanpur",
                is_available=True,
            ),
            ResponseTeam(
                team_code="BRG-ALD-01",
                name="Bridge Engineering Prayagraj",
                team_type=ResponseTeamType.BRIDGE,
                base_station="Prayagraj",
                base_latitude=25.4358,
                base_longitude=81.8463,
                contact_number="+91-532-2345678",
                contact_person="Bridge Engineer",
                is_available=True,
            ),
            ResponseTeam(
                team_code="ERT-MGS-01",
                name="Emergency Relief Train Mughalsarai",
                team_type=ResponseTeamType.EMERGENCY_RELIEF,
                base_station="Mughalsarai",
                base_latitude=25.2795,
                base_longitude=83.1234,
                contact_number="+91-541-2345678",
                contact_person="Emergency Controller",
                is_available=True,
            ),
        ]
        
        for t in teams:
            db.add(t)
        
        # Create Maintenance Tasks
        tasks = [
            MaintenanceTask(
                task_code="MT-2026-001",
                track_segment_id=3,
                title="Rail Replacement - TDL-CNB km 145-150",
                description="Replace 5km of 60kg rails due to excessive wear",
                urgency=TaskUrgency.HIGH,
                required_team_type=ResponseTeamType.TRACK_ENGINEERING,
                estimated_duration_hours=6.0,
                required_personnel=12,
                status="Planned",
            ),
            MaintenanceTask(
                task_code="MT-2026-002",
                track_segment_id=4,
                title="Emergency OHE Repair - CNB-ALD",
                description="OHE wire replacement after storm damage",
                urgency=TaskUrgency.CRITICAL,
                required_team_type=ResponseTeamType.TOWER_WAGON,
                estimated_duration_hours=4.0,
                required_personnel=8,
                status="In Progress",
            ),
            MaintenanceTask(
                task_code="MT-2026-003",
                track_segment_id=2,
                title="Ballast Tamping - GZB-TDL",
                description="Deep screening and tamping for geometry correction",
                urgency=TaskUrgency.MEDIUM,
                required_team_type=ResponseTeamType.TRACK_ENGINEERING,
                estimated_duration_hours=8.0,
                required_personnel=15,
                status="Planned",
            ),
            MaintenanceTask(
                task_code="MT-2026-004",
                track_segment_id=1,
                title="Signal Cable Replacement",
                description="Replace aging signaling cables at NDLS yard",
                urgency=TaskUrgency.MEDIUM,
                required_team_type=ResponseTeamType.SIGNAL_TELECOM,
                estimated_duration_hours=5.0,
                required_personnel=6,
                status="Planned",
            ),
        ]
        
        for t in tasks:
            db.add(t)
        
        # Create Sensor Data
        sensor_types = ["TMS", "TDMS", "SMMS", "Rail_Temp", "Vibration"]
        for segment in segments:
            for sensor_type in sensor_types:
                for i in range(24):  # Last 24 hours
                    db.add(SensorData(
                        track_segment_id=segment.id,
                        sensor_type=sensor_type,
                        value=round(0.5 + (i * 0.02) + (hash(sensor_type) % 10) * 0.05, 2),
                        unit="mm" if sensor_type in ["TMS", "TDMS", "SMMS"] else "C" if sensor_type == "Rail_Temp" else "g",
                        recorded_at=now - timedelta(hours=24-i),
                        location_km=round(segment.length_km * 0.5, 1),
                    ))
        
        # Create Inspection Logs
        inspections = [
            InspectionLog(
                track_segment_id=1,
                inspector_name="JE/Track NDLS",
                inspection_date=now - timedelta(days=2),
                findings="Minor rail wear detected at km 12.3. No immediate action required.",
                severity_score=0.15,
                recommended_action="Monitor during next inspection cycle",
            ),
            InspectionLog(
                track_segment_id=2,
                inspector_name="SSE/Track GZB",
                inspection_date=now - timedelta(days=5),
                findings="Ballast fouling observed between km 45-60. Geometry deviations within limits.",
                severity_score=0.35,
                recommended_action="Plan deep screening in next 60 days",
            ),
            InspectionLog(
                track_segment_id=3,
                inspector_name="DEN/Track TDL",
                inspection_date=now - timedelta(days=1),
                findings="Multiple rail fractures detected at km 145.2, 147.8. Urgent replacement needed.",
                severity_score=0.75,
                recommended_action="Immediate rail replacement. Speed restriction 30 kmph imposed.",
            ),
            InspectionLog(
                track_segment_id=4,
                inspector_name="SSE/Track CNB",
                inspection_date=now - timedelta(hours=6),
                findings="OHE mast foundation settlement at km 89.5. Wire tension critical.",
                severity_score=0.85,
                recommended_action="Emergency OHE repair. Tower wagon dispatched.",
            ),
            InspectionLog(
                track_segment_id=5,
                inspector_name="JE/Track ALD",
                inspection_date=now - timedelta(days=3),
                findings="Track geometry within limits. Minor ballast deficiency at few locations.",
                severity_score=0.10,
                recommended_action="Routine maintenance",
            ),
        ]
        
        for insp in inspections:
            db.add(insp)
        
        await db.commit()
        print("Database seeded successfully!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())