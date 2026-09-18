# Smart Face Attendance

A modular biometric attendance platform built with **Python, computer vision, FastAPI, React, and TypeScript**.

The project started as a Python face-recognition experiment and is evolving into a production-style biometric attendance service that can operate independently or integrate with larger systems such as:

* Employee Management Systems
* HR Management Systems
* Gym Management Systems
* Student Management Systems
* Access Control Systems
* Workplace attendance kiosks

The project is also being developed as a practical learning platform for:

* Software Engineering
* Computer Vision
* Full-Stack Development
* API Design
* System Architecture
* Security
* DevOps
* Docker
* CI/CD
* AWS Cloud Architecture

---

# Project Vision

The long-term goal is not simply to build a face-recognition application.

The goal is to build a reusable **Biometric Attendance Platform**.

```text
Employee / HR Management System
              │
              │ REST API / Events
              ▼
┌───────────────────────────────────┐
│   Smart Face Attendance Platform  │
│                                   │
│   React + TypeScript              │
│            │                      │
│            ▼                      │
│        FastAPI API                │
│            │                      │
│     ┌──────┼────────┐             │
│     ▼      ▼        ▼             │
│ Attendance Biometrics Integrations│
│     │      │        │             │
│     └──────┼────────┘             │
│            ▼                      │
│         Database                  │
└───────────────────────────────────┘
```

Face recognition is treated as one capability inside the overall attendance system rather than the entire application.

---

# Current System

The current application can:

* Register a person
* Capture facial training images
* Detect faces in real time
* Generate SFace embeddings
* Recognize registered users
* Reject unknown users using similarity thresholds
* Require stable identity recognition across multiple frames
* Perform liveness verification
* Detect eye blinks
* Detect head movement
* Require the user to return to the center position
* Reduce basic static-photo spoofing
* Record attendance in SQLite
* Prevent duplicate attendance on the same day
* View today's attendance
* Export attendance as CSV
* Manage registered people
* Run through a Tkinter desktop interface
* Expose attendance information through FastAPI
* Display live attendance information using React + TypeScript

---

# Biometric Verification Pipeline

The current verification process is:

```text
Camera
  │
  ▼
YuNet Face Detection
  │
  ▼
SFace Face Embedding
  │
  ▼
Cosine Similarity Matching
  │
  ▼
Stable Identity Verification
  │
  ▼
MediaPipe Face Landmarker
  │
  ├── Blink Detection
  ├── Head Turn Detection
  └── Return-to-Center Detection
  │
  ▼
Identity + Liveness Verified
  │
  ▼
Attendance Recorded
```

---

# Anti-Spoofing

Face recognition alone cannot determine whether the camera is seeing a live person.

For example, SFace may correctly recognize a photograph containing a registered person's face.

The system therefore performs an additional liveness challenge.

```text
Static photograph
      │
      ▼
Identity recognition may PASS
      │
      ▼
Blink challenge
      │
      ▼
FAIL
      │
      ▼
Attendance rejected
```

A real user must currently:

1. Look directly at the camera
2. Blink when requested
3. Turn their head
4. Return their face to the center position

This is a basic challenge-response liveness system.

It is intended for learning and practical attendance use cases and should not be considered equivalent to high-security biometric anti-spoofing systems used by banks or government identity platforms.

---

# Technology Stack

## Computer Vision

* Python
* OpenCV
* OpenCV Contrib
* YuNet
* SFace
* MediaPipe Face Landmarker
* NumPy

## Backend

Current:

* FastAPI
* Python
* SQLite

Planned:

* SQLAlchemy
* Alembic
* PostgreSQL
* Authentication and authorization
* API versioning
* Integration APIs
* Audit logging

## Frontend

Current:

* React
* TypeScript
* Vite

Planned frontend foundation:

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui
* TanStack Query
* React Router
* React Hook Form
* Zod
* Lucide Icons

The new frontend will support:

* Light theme
* Dark theme
* System theme
* Responsive layouts
* Reusable UI components
* Accessible dialogs and forms
* Loading skeletons
* Error states
* Empty states
* Toast notifications
* Search and filtering
* Modern tables and dashboards

---

# Application Architecture

The project is currently transitioning from a script-oriented structure into a modular full-stack architecture.

Target architecture:

```text
smart-face-attendance/
│
├── backend/
│   └── app/
│       ├── main.py
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── router.py
│       │       ├── attendance.py
│       │       ├── people.py
│       │       ├── biometrics.py
│       │       └── system.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   └── security.py
│       │
│       ├── models/
│       ├── schemas/
│       ├── repositories/
│       ├── services/
│       │   ├── attendance_service.py
│       │   ├── biometric_service.py
│       │   └── recognition_service.py
│       │
│       └── db/
│
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       │   ├── layout/
│       │   └── ui/
│       │
│       ├── features/
│       │   ├── dashboard/
│       │   ├── attendance/
│       │   ├── people/
│       │   ├── reports/
│       │   └── settings/
│       │
│       ├── hooks/
│       ├── lib/
│       ├── routes/
│       ├── services/
│       └── types/
│
├── data/
├── models/
└── ...
```

---

# Backend Architecture

The backend will follow a layered architecture.

```text
API Route
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Database
```

This keeps:

* HTTP logic
* business logic
* database logic
* biometric processing

separated from one another.

This approach makes the system easier to:

* test
* maintain
* integrate
* deploy
* scale
* extend

---

# API Design

The API is being designed so external systems can integrate with the attendance service.

API versioning will follow:

```text
/api/v1/
```

Example endpoints:

```text
GET    /api/v1/dashboard

GET    /api/v1/people
POST   /api/v1/people
DELETE /api/v1/people/{id}

GET    /api/v1/attendance
GET    /api/v1/attendance/today

POST   /api/v1/biometrics/enroll
POST   /api/v1/biometrics/verify
```

Versioning allows future API changes without immediately breaking systems already integrated with the platform.

---

# External System Integration

The biometric platform is designed to eventually work with other systems.

For example:

```text
Employee Management System
         │
         ▼
Employee EMP-00482
         │
         ▼
Smart Face Attendance API
         │
         ▼
Biometric Profile
         │
         ▼
Attendance Event
         │
         ▼
EMP-00482
```

A biometric profile should not depend directly on a specific employee database.

Instead, the architecture can use references such as:

```text
subject_id
subject_type
external_reference
```

Example:

```text
subject_id         = EMP-00482
subject_type       = employee
external_reference = HRMS-00482
```

This allows the same biometric platform to work with employees, students, members, or other user types.

---

# Future Event-Driven Architecture

A later version may publish attendance events.

```text
Face Verified
     │
     ▼
AttendanceRecorded
     │
     ▼
Event System
     │
     ├── Employee Management
     ├── Payroll
     ├── Notifications
     └── Analytics
```

This can later be implemented using AWS services such as:

* Amazon EventBridge
* Amazon SNS
* Amazon SQS

---

# Database Strategy

## Current

SQLite is currently used because it is:

* lightweight
* simple
* local
* easy to develop with

Current attendance data includes:

```text
Person ID
Person Name
Attendance Date
Attendance Time
Verification Method
Created Timestamp
```

Duplicate attendance for the same user on the same day is prevented.

## Planned

The cloud-ready architecture will migrate to:

```text
PostgreSQL
+
SQLAlchemy
+
Alembic
```

Possible future tables:

```text
organizations
users
subjects
biometric_profiles
biometric_embeddings
attendance_events
devices
audit_logs
integration_clients
```

---

# Frontend Vision

The React interface is being designed as a modern responsive management application.

Main navigation:

```text
Dashboard
Attendance
People
Devices
Reports
Integrations
Settings
```

Example dashboard:

```text
┌──────────────┬───────────────────────────────────────────────┐
│              │ Smart Attendance                Theme  Admin │
│              ├───────────────────────────────────────────────┤
│ Dashboard    │                                               │
│ Attendance   │ Registered   Present   Absent   System        │
│ People       │    124         108       16     Online       │
│ Devices      │                                               │
│ Reports      │ Attendance Overview                           │
│ Integrations │                                               │
│ Settings     │ Recent Attendance                             │
│              │                                               │
│              │ Janith      08:42      Verified              │
│              │ Kasun       08:45      Verified              │
└──────────────┴───────────────────────────────────────────────┘
```

---

# Theme System

The new frontend will support:

```text
Light
Dark
System
```

User theme preferences will be remembered locally.

The goal is to provide a professional interface suitable for:

* administration
* HR departments
* reception desks
* biometric kiosks
* desktop systems
* tablets

---

# Edge + Cloud Architecture

An important architectural consideration is webcam access.

A cloud server cannot directly access a webcam connected to an employee's local computer.

Therefore, the long-term architecture will separate local biometric processing from cloud business services.

```text
┌──────────── Local Device / Kiosk ─────────────┐
│                                               │
│ Camera                                        │
│   │                                           │
│   ▼                                           │
│ Face Detection                                │
│ Liveness Verification                         │
│ Biometric Verification                        │
│   │                                           │
└───┼───────────────────────────────────────────┘
    │ HTTPS
    ▼
Cloud API
    │
    ▼
Attendance Platform
    │
    ▼
Database
```

Possible edge devices include:

* Reception computers
* Attendance kiosks
* Tablets
* Raspberry Pi devices
* Dedicated employee terminals

---

# AWS Learning Roadmap

A major goal of this project is gaining practical AWS experience.

Possible target architecture:

```text
Users
  │
  ▼
CloudFront
  │
  ▼
React Frontend
  │
  ▼
API / Load Balancer
  │
  ▼
FastAPI Containers
  │
  ├───────────────┐
  ▼               ▼
RDS PostgreSQL    S3
```

Planned AWS technologies may include:

* Amazon CloudFront
* Amazon S3
* AWS Amplify Hosting
* Amazon ECS
* AWS Fargate
* Amazon ECR
* Amazon RDS for PostgreSQL
* Amazon Cognito
* AWS Secrets Manager
* AWS KMS
* Amazon CloudWatch
* Amazon Route 53
* AWS Certificate Manager
* Amazon EventBridge
* Amazon SNS
* Amazon SQS

---

# Containerization and DevOps

Future infrastructure stages will introduce:

```text
Docker
Docker Compose
GitHub Actions
CI/CD
AWS ECR
AWS ECS Fargate
Infrastructure as Code
```

Infrastructure as Code may later use:

* AWS CDK
* Terraform

---

# Authentication and Security

Because biometric information is sensitive, security is an important part of the future architecture.

Planned security features include:

* HTTPS
* JWT authentication
* Role-based access control
* Audit logging
* Encryption
* Input validation
* CORS restrictions
* Rate limiting
* Secure API integrations
* Secret management
* Encrypted biometric data

Potential roles:

```text
SUPER_ADMIN
HR_ADMIN
MANAGER
ATTENDANCE_OPERATOR
VIEWER
DEVICE
```

Biometric embeddings should not be treated like ordinary profile images.

---

# Current Project Structure

The project currently contains a mixture of the original Python prototype and the new full-stack architecture.

```text
smart-face-attendance/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── data/
│   ├── attendance.db
│   ├── faces/
│   └── models/
│
├── models/
│   ├── face_detection_yunet_2023mar.onnx
│   ├── face_recognition_sface_2021dec.onnx
│   └── face_landmarker.task
│
├── attendance_db.py
├── register_face.py
├── build_sface_embeddings.py
├── recognize_sface.py
├── liveness_test.py
├── verify_identity.py
├── dashboard.py
├── people_manager.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The older Tkinter application is currently retained while the React application reaches feature parity.

---

# Running the Python Environment

Create the virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

# Running FastAPI

From the project root:

```bash
fastapi dev backend/main.py
```

Development API:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running React

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The current communication flow is:

```text
React
   │
   ▼
FastAPI
   │
   ▼
Python Services
   │
   ▼
SQLite
```

---

# Registering a Person

Run:

```bash
python register_face.py
```

Example:

```text
Person ID: 001
Name: Janith Dasanayaka
```

Captured face images are stored locally under:

```text
data/faces/
```

Biometric face datasets are excluded from Git.

---

# Building Face Embeddings

After registration:

```bash
python build_sface_embeddings.py
```

This generates the local SFace biometric database.

---

# Testing Recognition

Run:

```bash
python recognize_sface.py
```

The application displays:

```text
Name
Person ID
Similarity
```

Unknown users are rejected if their similarity does not meet the configured threshold.

---

# Testing Liveness

Run:

```bash
python liveness_test.py
```

Current challenge:

```text
Look Straight
    ↓
Blink
    ↓
Turn Head
    ↓
Return to Center
    ↓
Liveness Passed
```

---

# Complete Verification

Run:

```bash
python verify_identity.py
```

Successful verification performs:

```text
Face Detection
      ↓
SFace Recognition
      ↓
Stable Identity
      ↓
Liveness Verification
      ↓
Attendance Recording
```

---

# Privacy

Sensitive local files are intentionally excluded from Git.

Examples:

```gitignore
data/faces/
data/models/
data/*.db

models/*.onnx
models/*.task

.venv/
frontend/node_modules/
```

The public repository should not contain:

* Registered users' face images
* Generated biometric embeddings
* Local attendance databases
* Secrets
* Environment variables

---

# Development Roadmap

## Phase 1 — Computer Vision

* [x] Webcam integration
* [x] Haar face detection
* [x] Face dataset collection
* [x] LBPH prototype
* [x] Identify LBPH limitations
* [x] YuNet integration
* [x] SFace integration
* [x] Deep facial embeddings
* [x] Unknown-person detection

## Phase 2 — Liveness

* [x] MediaPipe Face Landmarker
* [x] Blink detection
* [x] Head-turn detection
* [x] Return-to-center detection
* [x] Static-photo challenge-response protection
* [x] Combined recognition + liveness verification

## Phase 3 — Attendance

* [x] SQLite attendance database
* [x] Attendance recording
* [x] Duplicate prevention
* [x] Today's attendance
* [x] CSV export

## Phase 4 — Desktop Prototype

* [x] Tkinter admin dashboard
* [x] Registered people manager
* [x] Attendance controls
* [x] CSV export interface

## Phase 5 — Full-Stack Migration

* [x] FastAPI foundation
* [x] React
* [x] TypeScript
* [x] Vite
* [x] React-to-FastAPI communication

## Phase 6 — Modern Frontend

* [ ] Tailwind CSS
* [ ] shadcn/ui
* [ ] Dark / light / system theme
* [ ] React Router
* [ ] TanStack Query
* [ ] Zod validation
* [ ] Modern application shell
* [ ] Responsive dashboard
* [ ] People management
* [ ] Attendance history
* [ ] Reports
* [ ] Settings

## Phase 7 — Backend Engineering

* [ ] `/api/v1` architecture
* [ ] Service layer
* [ ] Repository layer
* [ ] Pydantic schemas
* [ ] Central configuration
* [ ] Structured logging
* [ ] Error handling
* [ ] API documentation

## Phase 8 — Database Engineering

* [ ] SQLAlchemy
* [ ] Alembic
* [ ] PostgreSQL
* [ ] Database migrations
* [ ] Audit records

## Phase 9 — Security

* [ ] Authentication
* [ ] JWT
* [ ] RBAC
* [ ] Audit logging
* [ ] Secure biometric storage
* [ ] Integration credentials
* [ ] Rate limiting

## Phase 10 — Integration Platform

* [ ] External subject IDs
* [ ] Employee system integration
* [ ] API clients
* [ ] Webhooks
* [ ] Event-driven attendance

## Phase 11 — Testing

* [ ] pytest
* [ ] API tests
* [ ] Vitest
* [ ] React Testing Library
* [ ] Playwright end-to-end testing

## Phase 12 — DevOps

* [ ] Docker
* [ ] Docker Compose
* [ ] GitHub Actions
* [ ] Automated tests
* [ ] CI/CD

## Phase 13 — AWS

* [ ] Frontend deployment
* [ ] Container registry
* [ ] ECS Fargate
* [ ] PostgreSQL on RDS
* [ ] Cognito authentication
* [ ] CloudWatch monitoring
* [ ] Secrets Manager
* [ ] HTTPS
* [ ] Domain configuration

## Phase 14 — Infrastructure as Code

* [ ] AWS CDK or Terraform
* [ ] Reproducible environments
* [ ] Development environment
* [ ] Production environment

---

# Current Development Focus

The current milestone is:

```text
Frontend Architecture & Design System
```

The next implementation stage will introduce:

```text
Tailwind CSS
+
shadcn/ui
+
React Router
+
TanStack Query
+
Dark / Light / System Theme
+
Modern Responsive Application Shell
```

After that, the existing basic React page will be replaced by the new production-style dashboard.

---

# Engineering Goals

This project prioritizes:

* Modularity
* Separation of concerns
* Maintainability
* Security
* Scalability
* Testability
* API-first design
* Integration readiness
* Cloud readiness
* User-friendly UX
* Modern development practices

---

# Author

**Janith Dasanayaka**

Software Engineering Student
Full-Stack Developer
Cloud & AI Learner

---

# Repository

**Smart Face Attendance**

`janithcd/smart-face-attendance`
