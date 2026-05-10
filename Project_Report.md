# UniCarpool

**A University Ride-Sharing Web Application**

*Project Report*

**Submitted by:**

- **Muhammad Umer** – 24K-0894
- **Ahmed Khan** – 24K-0629
- **Muhammad Hammad Yousuf** – 24K-0597

**Course:** Database Systems  
**Instructor:** Talha Shahid  
**Submission Date:** 10 May 2025

---

## Table of Contents

- [Abstract](#abstract)
- [1. Introduction](#1-introduction)
- [2. Literature Review](#2-literature-review)
- [3. System Analysis and Requirements](#3-system-analysis-and-requirements)
- [4. System Design](#4-system-design)
- [5. Implementation](#5-implementation)
- [6. Testing and Results](#6-testing-and-results)
- [7. Database Analysis](#7-database-analysis)
- [8. Discussion](#8-discussion)
- [9. Future Enhancements](#9-future-enhancements)
- [Conclusion](#conclusion)

---

## Abstract

UniCarpool is a web-based university ride-sharing application built using Django 5 and MySQL, designed to address the commuting challenges faced by students and faculty at Pakistani universities. The platform provides a minimalistic yet fully functional environment in which users may register, post available rides, join existing rides as passengers, track active trips, and simulate fare payments — all through a clean, mobile-responsive interface.

The system implements a relational database architecture comprising four core tables: `auth_user` (Django's built-in user model), `rides_ride`, `rides_ridepickupstop`, and `rides_rideparticipant`. These tables are carefully normalized and linked via foreign key constraints with cascading deletes, ensuring referential integrity throughout the lifecycle of every ride.

Key technical highlights include atomic database transactions for concurrent seat-booking operations, Django ORM query optimization with `select_related` and `prefetch_related`, a multi-stop pickup system per ride, and a payment simulation workflow gated behind ride finalization. The frontend leverages Bootstrap 5 and a custom dark-themed CSS layer, delivering a professional user experience.

| **Attribute** | **Details** |
|---|---|
| Project Title | UniCarpool — University Ride-Sharing Web Application |
| Technology Stack | Django 5, MySQL 8, Bootstrap 5, PyMySQL, Python 3.13 |
| Database | MySQL with Django ORM; 4 core tables |
| Key Features | User auth, ride creation, seat booking, pickup stops, finalization, payment simulation |
| Architecture | MVC (Django MVT pattern), relational RDBMS backend |

---

## 1. Introduction

### 1.1 Background

Transportation is one of the most persistent day-to-day challenges for university students, particularly in large urban centers like Karachi, Pakistan. Students and faculty commuting from various districts of the city often travel alone in private vehicles or rely on public transport systems that are frequently unreliable, unsafe, and overcrowded. This results in higher commuting costs, increased carbon emissions, and a diminished sense of campus community.

Carpooling — the practice of sharing a private vehicle with others traveling in the same direction — represents a practical and well-proven solution to these challenges. Digital carpool platforms have seen significant adoption in Western universities; however, purpose-built platforms tailored to the social and logistical dynamics of South Asian universities remain relatively rare.

UniCarpool was developed to bridge this gap by delivering a lightweight, full-stack ride-sharing application specifically designed for university environments. Built upon the Django web framework and backed by a MySQL relational database, the application manages the complete lifecycle of a shared ride — from posting and discovery to seat booking, driver confirmation, and payment settlement.

### 1.2 Problem Statement

University students at FAST-NUCES Karachi face significant commuting difficulties. Public transport schedules are inconsistent, and private ride-hailing platforms such as Careem and inDrive can be prohibitively expensive for students on limited budgets. Additionally, no centralized university-internal platform currently exists to allow students to coordinate shared rides based on mutual routes, departure times, and trusted community membership.

The absence of such a system forces students to organize informal carpools through WhatsApp groups or word-of-mouth — methods that are neither scalable nor safe, offering no structured coordination, seat-availability tracking, or payment management.

### 1.3 Motivation

The primary motivation for UniCarpool lies in the potential to make daily commuting more affordable, safer, and environmentally conscious for the university community. By creating a shared digital platform, students who drive can offset fuel and maintenance costs, while passengers benefit from door-to-door convenience at a fraction of typical ride-hailing prices.

From an academic perspective, the project serves as a practical exercise in relational database design, Django ORM usage, web application security (CSRF protection, authentication), and scalable backend architecture.

### 1.4 Objectives

The primary objectives of this project are as follows:

- Design and implement a fully normalized relational database schema for a carpool management system.
- Develop a secure, session-based user authentication system using Django's built-in auth framework.
- Build a ride-posting module enabling drivers to specify routes, departure times, fares, seat capacity, and multiple pickup stops.
- Implement a seat-booking system with concurrency protection using atomic database transactions.
- Provide a ride-finalization workflow that allows drivers to close rides and trigger the payment simulation phase.
- Create a clean, responsive frontend using Bootstrap 5 and a custom dark-themed CSS layer.
- Demonstrate database integrity through foreign key constraints, unique constraints, and indexed queries.

### 1.5 Scope of the Project

UniCarpool covers the following functional scope:

- User registration, login, and logout via Django's authentication framework.
- Ride creation with full route details, departure scheduling, fare specification, seat capacity management, and multi-stop pickup points.
- Ride discovery and browsing for authenticated users, filtered to show only available future rides posted by other users.
- Ride joining with contact and pickup location capture, protected against duplicate bookings and race conditions.
- Driver-side ride management including finalization of active rides.
- Passenger-side payment simulation after ride finalization.
- Recent ride history for both drivers and passengers.

The project does **not** currently include: real-time geolocation or map integration, push notification systems, actual payment gateway integration, in-app messaging between users, or mobile native applications.

### 1.6 Existing System Overview

Currently, ride coordination at the university level is handled informally. Students post in WhatsApp groups or Facebook communities asking for carpool partners. This approach has several drawbacks: there is no structured seat availability tracking, no formal agreement on fare, no contact verification, and no ride history. Nationally, platforms like Careem Pool and Bykea offer carpooling features but are not scoped to university communities and charge commercial rates.

### 1.7 Proposed System Overview

UniCarpool proposes a closed, university-branded ride-sharing platform. The system uses a three-tier architecture: a MySQL relational database at the persistence layer, Django as the application server handling business logic, and a Bootstrap 5 / custom CSS frontend rendered through Django's Jinja2-compatible template engine. The platform enforces community trust by requiring account registration before any ride interaction, and uses database-level constraints to guarantee data consistency.

### 1.8 Benefits of the Proposed System

- Cost reduction for students through fare-sharing on regular commutes.
- Structured ride management replacing informal communication channels.
- Data integrity and consistency via RDBMS constraints and atomic transactions.
- Reduced environmental footprint through vehicle consolidation.
- Foundation for future enhancements including GPS tracking and real payment gateways.

### 1.9 Project Constraints

- No real-time location services are integrated in the current version.
- Payment processing is simulated and not connected to any financial institution.
- The application currently relies on server-side session authentication rather than JWT-based APIs.
- Deployment is scoped for local development (`localhost:8000`); production hardening (HTTPS, `SECRET_KEY` rotation, `DEBUG=False`) is deferred.

### 1.10 Assumptions

- All users are affiliated with the university and register using verifiable credentials.
- MySQL 8.x is installed and accessible at the configured host and port.
- Python 3.13 and the packages listed in `requirements.txt` are available.
- Users operate within the same or nearby campus zones, making geographic matching implicit rather than algorithmic.

---

## 2. Literature Review

### 2.1 Relational Database Systems and the MySQL Ecosystem

Relational database management systems (RDBMS), introduced by Edgar F. Codd in his landmark 1970 paper, form the theoretical foundation of this project. MySQL 8.x, used in this project, supports full ACID compliance with the InnoDB storage engine, window functions, JSON data types, and utf8mb4 character encoding.

The project employs MySQL's InnoDB engine exclusively, leveraging its row-level locking capabilities to support the concurrent seat-booking transactions that are central to the ride-joining workflow.

### 2.2 Django as a Web Application Framework

Django is a high-level Python web framework that follows the Model-View-Template (MVT) architectural pattern, a variant of the classical MVC paradigm. First released in 2005 and now at version 5.2, Django provides an ORM that abstracts SQL generation, a built-in authentication framework, a forms library for input validation, a powerful admin interface, and a templating engine for HTML rendering.

Django's ORM translates Python class definitions (models) into SQL table definitions via a migration system, making schema versioning reproducible and team-friendly.

### 2.3 Similar Existing Systems

Several digital carpool platforms informed the design of UniCarpool:

- **BlaBlaCar** (France, 2006): The global leader in intercity carpooling, offering route matching, driver ratings, and real payment integration.
- **Zimride / Lyft for Commuters**: University-focused carpool service later acquired by Lyft; demonstrated the viability of closed-community carpooling.
- **RideShare apps at MIT/Stanford**: Several institutions have deployed pilot carpool platforms using Django or Ruby on Rails, confirming Django is a suitable choice for university-scale applications.

### 2.4 Related Technologies

Bootstrap 5 was selected for the frontend due to its extensive responsive grid system and component library. PyMySQL serves as the Python-to-MySQL adapter, replacing the deprecated MySQLdb library. Django's `select_related` and `prefetch_related` ORM optimization techniques are employed extensively in the view layer to eliminate N+1 query problems.

### 2.5 Comparative Analysis

| **Feature** | **UniCarpool** | **BlaBlaCar** | **Informal WhatsApp Groups** |
|---|---|---|---|
| University-targeted | Yes | No | Yes (informal) |
| Structured seat management | Yes | Yes | No |
| Payment integration | Simulated | Real (Stripe) | No |
| Ride history | Yes | Yes | No |
| Multi-stop pickup | Yes | Limited | No |
| Open-source / academic | Yes | No | N/A |
| RDBMS-backed | MySQL (ACID) | PostgreSQL | No |

---

## 3. System Analysis and Requirements

### 3.1 Functional Requirements

| **FR-ID** | **Description** | **Priority** |
|---|---|---|
| FR-01 | System shall allow new users to register with first name, last name, username, email, and password. | High |
| FR-02 | System shall authenticate registered users using username and password. | High |
| FR-03 | Authenticated users shall be able to post a ride with origin, destination, departure time, pickup point, seats, fare, and notes. | High |
| FR-04 | System shall support multiple additional pickup stops per ride (ordered list). | Medium |
| FR-05 | Authenticated users shall view all available rides posted by other users with future departure times. | High |
| FR-06 | Users shall be able to join a ride by providing a contact number and selecting a pickup location. | High |
| FR-07 | System shall prevent a user from joining their own ride. | High |
| FR-08 | System shall prevent duplicate ride-joins (same user joining same ride twice). | High |
| FR-09 | System shall decrement seat availability atomically upon a successful join. | High |
| FR-10 | Driver shall be able to view all passengers and their contact details for their active rides. | High |
| FR-11 | Driver shall be able to finalize a ride, transitioning its status to FINALIZED. | High |
| FR-12 | Passenger shall be able to simulate payment for finalized rides. | Medium |
| FR-13 | System shall display ride history (completed rides) for both drivers and passengers. | Medium |
| FR-14 | System shall display the count of pending payments to the passenger. | Low |

### 3.2 Non-Functional Requirements

| **NFR-ID** | **Requirement** | **Metric** |
|---|---|---|
| NFR-01 | Security: All forms protected with CSRF tokens. | Django middleware enforced on every POST request |
| NFR-02 | Concurrency: Seat booking must be race-condition-free. | Achieved via SELECT FOR UPDATE in atomic transactions |
| NFR-03 | Usability: Interface must be responsive on mobile and desktop. | Bootstrap 5 responsive grid; tested on 375px and 1440px viewports |
| NFR-04 | Performance: Ride listing queries must not produce N+1 queries. | `select_related` + `prefetch_related` on all list views |
| NFR-05 | Reliability: System must enforce referential integrity at DB layer. | InnoDB with CASCADE foreign keys on all relations |
| NFR-06 | Maintainability: Database schema must be versioned via migrations. | Django migrations (`0001_initial.py`, `0002_ridepickupstop.py`) |

### 3.3 Software Requirements

| **Component** | **Technology** | **Version** |
|---|---|---|
| Web Framework | Django | >= 5.0, < 6.0 |
| Programming Language | Python | 3.13 |
| Database Server | MySQL | 8.x |
| Python-MySQL Adapter | PyMySQL | >= 1.1.1 |
| Frontend Framework | Bootstrap | 5.3.3 (CDN) |
| Version Control | Git | Latest |
| Development OS | Windows 10/11 | PowerShell 7+ |

### 3.4 Hardware Requirements

| **Component** | **Minimum** | **Recommended** |
|---|---|---|
| Processor | Dual-core 2.0 GHz | Quad-core 2.5 GHz or higher |
| RAM | 4 GB | 8 GB |
| Storage | 2 GB free disk space | 10 GB SSD |
| Network | Local LAN (development) | Broadband (production deployment) |
| Display | 1024x768 | 1920x1080 |

### 3.5 Feasibility Study

#### 3.5.1 Technical Feasibility

The project employs mature, well-documented technologies. Django 5 is production-ready and widely used in enterprise applications. MySQL is the most popular open-source RDBMS with native Python support via PyMySQL. The chosen stack is well within the technical capabilities of the development team, making the project technically feasible.

#### 3.5.2 Economic Feasibility

All technologies used are open-source and freely available. MySQL Community Edition, Python, and Django carry no licensing costs. Bootstrap is loaded via CDN. The total development cost is limited to developer time and hardware — both of which are already available.

#### 3.5.3 Operational Feasibility

The web-based interface requires no client-side software installation. Users access the application via a standard web browser. Core workflows (signup, post ride, join ride, finalize, pay) each require no more than three user interactions.

### 3.6 User Requirements

Three primary user roles were identified during requirements analysis:

- **Guest** (unauthenticated visitor): Can access the public landing page and navigate to login/signup.
- **Driver**: Authenticated user who posts a ride, manages it (views passengers, finalizes the ride), and reviews their driving history.
- **Passenger**: Authenticated user who browses available rides, joins a ride, and simulates payment after the ride is finalized.

A single user account may act as both Driver and Passenger across different rides, as the role is ride-specific rather than account-level.

---

## 4. System Design

### 4.1 Overall System Architecture

UniCarpool follows Django's Model-View-Template (MVT) pattern, a server-side rendering (SSR) architecture organized in three tiers:

- **Tier 1 — Presentation (Browser)**: HTML rendered from Django templates, styled with Bootstrap 5 and `theme.css`. No JavaScript framework is used; all interactivity is driven by standard HTML forms and server redirects.
- **Tier 2 — Application (Django Server)**: Python views handle HTTP requests, invoke ORM queries, validate form data, enforce business rules, and return rendered templates or HTTP redirects.
- **Tier 3 — Data (MySQL Server)**: Stores all persistent application data in four tables. The InnoDB engine enforces ACID compliance and foreign key constraints.

The request-response cycle: Browser → Django URL Router → View Function → ORM (queries MySQL) → View renders Template → HTML Response → Browser.

### 4.2 Database Design

The database design centers on four tables: `auth_user` (provided by Django's authentication framework) and three custom tables defined in `rides/models.py`. The schema was designed to be in Third Normal Form (3NF) and has been verified against Boyce-Codd Normal Form (BCNF) criteria.

### 4.3 ER Diagram Explanation

The logical ER diagram defines the following entities and relationships:

- **USER** (`auth_user`): Represents a registered platform user. A user may drive zero or more rides and join zero or more rides as a passenger.
- **RIDE** (`rides_ride`): Represents a single carpool trip. Belongs to exactly one driver. May have zero or more pickup stops and zero or more participants.
- **RIDE_PICKUP_STOP** (`rides_ridepickupstop`): Represents an ordered intermediate pickup location. Belongs to exactly one RIDE. The `(ride_id, stop_order)` pair is unique.
- **RIDE_PARTICIPANT** (`rides_rideparticipant`): Represents a passenger's booking on a ride. Links exactly one USER to exactly one RIDE. The `(ride_id, user_id)` pair is unique, preventing double-booking.

**Cardinality summary:** USER (1) → RIDE (many); RIDE (1) → RIDE_PICKUP_STOP (many); RIDE (1) → RIDE_PARTICIPANT (many); USER (1) → RIDE_PARTICIPANT (many).

### 4.4 Tables and Relationships

All foreign keys use `ON DELETE CASCADE`, meaning deletion of a parent record automatically removes all dependent child records.

### 4.5 Data Dictionary

#### Table 4.1 — rides_ride

| **Column** | **Type** | **Constraints** | **Description** |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Unique ride identifier |
| driver_id | BIGINT | FK → auth_user.id, NOT NULL | The user who created and drives this ride |
| origin | VARCHAR(120) | NOT NULL | Starting location of the ride |
| destination | VARCHAR(120) | NOT NULL | Ending location of the ride |
| departure_time | DATETIME | NOT NULL, INDEX | Scheduled departure date and time |
| pickup_point | VARCHAR(120) | NOT NULL | Primary pickup location |
| seats_total | INT UNSIGNED | NOT NULL, DEFAULT 1 | Total passenger capacity declared by driver |
| seats_available | INT UNSIGNED | NOT NULL, DEFAULT 1 | Remaining joinable seats; decremented on booking |
| fare_per_seat | DECIMAL(7,2) | NOT NULL | Cost per passenger seat in PKR |
| notes | LONGTEXT | NOT NULL, DEFAULT '' | Optional driver notes visible to passengers |
| status | VARCHAR(16) | NOT NULL, DEFAULT 'OPEN', INDEX | Ride lifecycle state: OPEN \| ACTIVE \| FINALIZED |
| finalized_at | DATETIME | NULL | Timestamp when driver finalized the ride |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| updated_at | DATETIME | NOT NULL, DEFAULT NOW() ON UPDATE | Last modification timestamp |

#### Table 4.2 — rides_rideparticipant

| **Column** | **Type** | **Constraints** | **Description** |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Unique participant record identifier |
| ride_id | BIGINT | FK → rides_ride.id, NOT NULL | The ride being joined |
| user_id | BIGINT | FK → auth_user.id, NOT NULL | The passenger user |
| contact_number | VARCHAR(20) | NOT NULL | Passenger contact number visible to driver |
| pickup_location | VARCHAR(120) | NOT NULL | The specific stop selected by the passenger |
| payment_status | VARCHAR(12) | NOT NULL, DEFAULT 'PENDING' | Payment state: PENDING \| PAID |
| paid_at | DATETIME | NULL | Timestamp of simulated payment |
| joined_at | DATETIME | NOT NULL, DEFAULT NOW() | Timestamp when the user joined the ride |

#### Table 4.3 — rides_ridepickupstop

| **Column** | **Type** | **Constraints** | **Description** |
|---|---|---|---|
| id | BIGINT | PK, AUTO_INCREMENT | Unique stop record identifier |
| ride_id | BIGINT | FK → rides_ride.id, NOT NULL | Parent ride for this stop |
| location | VARCHAR(120) | NOT NULL | Stop location name or description |
| stop_order | INT UNSIGNED | NOT NULL, DEFAULT 1 | Ordering sequence of stop along route (1 = first) |

### 4.6 Module Design

The application is organized into two primary modules:

- **`config/`** — Project configuration: `settings.py`, `urls.py` (root URL dispatcher), `asgi.py` and `wsgi.py`.
- **`rides/`** — Core application: `models.py`, `views.py`, `forms.py`, `urls.py`, `admin.py`, `tests.py`, `migrations/`.

### 4.7 Input / Output Design

**Input surfaces** include: Sign-Up form, Login form, Create Ride form (origin, destination, departure time, pickup stops, seats, fare, notes), and Join Ride inline form (contact number, pickup location).

**Output surfaces** include: landing page, home page (available rides grid), current rides dashboard (driver and passenger views), and recent rides page (finalized rides with payment simulation buttons).

### 4.8 User Interface Design

The UI employs a dark-themed aesthetic using a deep navy/charcoal background (`#090b10`) with yellow accent colors (`#FFD249`). Bootstrap 5 provides the responsive grid, while custom CSS variables in `theme.css` define the color palette, frosted-glass panel effect (`backdrop-filter: blur`), hover animations on ride cards, and custom form styling. The interface is fully responsive, supporting mobile viewports down to 375px wide.

---

## 5. Implementation

### 5.1 Technologies Used

| **Category** | **Technology** | **Purpose** |
|---|---|---|
| Backend Framework | Django 5.2 | MVC web application server, ORM, auth, forms, templating |
| Database | MySQL 8.x via InnoDB | Relational data storage with ACID guarantees |
| DB Adapter | PyMySQL 1.1.1+ | Pure-Python MySQL connector |
| Frontend CSS | Bootstrap 5.3.3 (CDN) | Responsive layout, components, utility classes |
| Custom CSS | static/css/theme.css | Dark theme, glass-morphism panels, animated blobs |
| Version Control | Git + GitHub | Source code management and collaboration |
| Scripting | PowerShell | Local dev setup, phone demo script |

### 5.2 Project File Structure

```
carpool-app/                  # repository root
├── config/                   # Django project package (settings, URLs, WSGI/ASGI)
├── rides/                    # Django application package (models, views, forms, URLs, admin, tests, migrations)
├── templates/                # HTML templates (base.html; rides/ and registration/ subdirectories)
├── static/css/theme.css      # custom UI theme
├── docs/                     # project documentation (schema.sql, database-erd.md)
├── scripts/                  # utility scripts (run_phone_demo.ps1)
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management CLI entry point
└── db.sqlite3                # SQLite fallback for offline development
```

### 5.3 Model Layer (rides/models.py)

#### 5.3.1 Ride Model

The `Ride` model uses an inner `Status` TextChoices enum to constrain the `status` field to `OPEN`, `ACTIVE`, or `FINALIZED`. The `finalize()` method transitions status to `FINALIZED` and stamps `finalized_at` with the current UTC time using `timezone.now()`, with a targeted `save(update_fields=...)` to avoid full-row updates.

#### 5.3.2 RidePickupStop Model

This model extends the ride data model to support a variable-length ordered sequence of pickup stops. The `unique_together = ("ride", "stop_order")` Meta constraint generates a composite `UNIQUE KEY` at the database level.

#### 5.3.3 RideParticipant Model

Records each passenger booking. The `unique_together = ("ride", "user")` constraint prevents the same user from booking the same ride twice, enforced both by the ORM and by a MySQL `UNIQUE KEY`.

### 5.4 View Layer (rides/views.py)

All authenticated views use the `@login_required` decorator. Transactional views use `@transaction.atomic` with `select_for_update()` on the Ride object to acquire a row-level lock before seat decrement, preventing race conditions.

#### 5.4.1 URL Routes

| **URL Pattern** | **View Function** | **Description** |
|---|---|---|
| `/` | landing_view | Public landing page; redirects authenticated users |
| `/signup/` | signup_view | User registration; auto-logs in after successful signup |
| `/home/` | home_view | Available rides listing + inline join forms |
| `/rides/create/` | create_ride_view | Ride creation form with pickup stop input |
| `/rides/current/` | current_rides_view | Driver and passenger dashboards for active rides |
| `/rides/recent/` | recent_rides_view | Completed ride history + payment simulation |
| `/rides/<id>/join/` | join_ride_view | POST endpoint: join a specific ride |
| `/rides/<id>/finalize/` | finalize_ride_view | POST endpoint: driver finalizes ride |
| `/rides/<id>/pay/` | simulate_payment_view | POST endpoint: passenger simulates payment |
| `/accounts/login/` | Django auth LoginView | Session-based login form |
| `/accounts/logout/` | Django auth LogoutView | POST-only logout |
| `/admin/` | Django admin site | Admin panel for all three models |

### 5.5 Form Layer (rides/forms.py)

Four form classes implement input validation:

- **StyledAuthenticationForm**: Extends Django's `AuthenticationForm`, adding Bootstrap CSS classes to widgets.
- **SignUpForm**: Extends `UserCreationForm` with an additional `email` field.
- **RideCreateForm**: Extends `ModelForm` for the Ride model. Adds a `pickup_stops_text` Textarea for free-text stop entry. The `save()` override handles creation of `RidePickupStop` records in the same transaction.
- **JoinRideForm**: A simple non-model Form with `contact_number` and `pickup_location` fields.

### 5.6 Authentication and Authorization

Authentication is handled entirely by Django's `django.contrib.auth` framework. Passwords are stored as PBKDF2-SHA256 hashed strings. CSRF protection is enforced on every POST request through Django's `CsrfViewMiddleware`. Authorization at the object level is enforced in views (e.g., only the ride's driver can finalize it).

### 5.7 Key Algorithms

#### 5.7.1 Atomic Seat Booking

The `join_ride_view` uses `select_for_update()` combined with an F-expression update to decrement `seats_available` atomically. The `F("seats_available") - 1` pattern executes as `UPDATE ... SET seats_available = seats_available - 1 WHERE seats_available > 0`, preventing negative seat counts under concurrent load.

#### 5.7.2 Pickup Stop Parsing

The `RideCreateForm.clean_pickup_stops_text()` method normalizes user-entered stop text by replacing carriage returns and commas with newlines, splitting the result, stripping whitespace, and filtering empty strings. Results are deduplicated before `RidePickupStop` records are created.

#### 5.7.3 Payment State Machine

Payment follows a strict two-state machine: `PENDING → PAID`. The `simulate_payment_view()` enforces that payment can only be triggered when the ride's status is `FINALIZED`, and a second guard prevents re-payment if `payment_status` is already `PAID`.

---

## 6. Testing and Results

### 6.1 Testing Methodology

The project uses Django's built-in `TestCase` framework, which wraps each test in a database transaction that is rolled back after the test completes, ensuring test isolation. Django's test client (`self.client`) simulates HTTP requests without requiring a running server.

### 6.2 Unit Test Cases

| **TC-ID** | **Test Name** | **Scenario** | **Expected Outcome** | **Status** |
|---|---|---|---|---|
| UT-01 | test_passenger_can_join_ride | Authenticated passenger posts valid join data | seats_available decrements by 1; RideParticipant created | PASS |
| UT-02 | test_driver_can_finalize_ride | Authenticated driver posts finalize request | status == FINALIZED; finalized_at is non-null | PASS |
| UT-03 | test_passenger_can_simulate_payment_after_finalization | Passenger attempts payment after finalization | payment_status == PAID; paid_at is non-null | PASS |
| UT-04 | test_driver_can_add_multiple_pickup_stops | Driver creates ride with comma/newline-separated stops | stops ordered correctly | PASS |

### 6.3 Integration Test Cases

| **TC-ID** | **Scenario** | **Modules Tested** | **Expected Outcome** |
|---|---|---|---|
| IT-01 | Unauthenticated access to /home/ is redirected to login | Middleware + URL routing + auth | HTTP 302 redirect to /accounts/login/?next=/home/ |
| IT-02 | User signs up and is automatically logged in | signup_view + SignUpForm + Django auth | User record created; session active; redirect to /home/ |
| IT-03 | Driver posts to /rides/<id>/finalize/ for a ride not owned by them | finalize_ride_view + get_object_or_404 | HTTP 404 returned; ride not modified |
| IT-04 | Passenger attempts to join a FINALIZED ride | join_ride_view + Ride.Status | Error message displayed; no RideParticipant created |
| IT-05 | Passenger attempts to join their own ride | join_ride_view + driver ID check | Error message displayed; no RideParticipant created |

### 6.4 System Test Cases

| **TC-ID** | **End-to-End Scenario** | **Expected Result** |
|---|---|---|
| ST-01 | Full ride lifecycle: Create → Browse → Join → Finalize → Pay | All state transitions complete; DB records consistent at each step |
| ST-02 | Concurrent booking attempt by two passengers for last available seat | Only one booking succeeds; second user receives "No seats left" error |
| ST-03 | Ride with departure time in the past cannot be created | Form validation error; no Ride record created |
| ST-04 | Mobile viewport (375px): all pages render without horizontal overflow | Bootstrap responsive grid handles layout correctly |

### 6.5 Result Analysis

All four automated unit tests pass consistently across clean database states. Manual testing confirmed that the concurrent booking protection functions correctly: when two browser tabs simultaneously submit join requests for a ride with one remaining seat, exactly one succeeds and the other receives the "No seats left" error message — validating the `SELECT FOR UPDATE` implementation.

---

## 7. Database Analysis

### 7.1 Normalization

#### 7.1.1 First Normal Form (1NF)

All tables satisfy 1NF: every cell contains a single atomic value, there are no repeating groups, and every row is uniquely identified by a primary key. The multi-stop requirement was correctly extracted into a separate `rides_ridepickupstop` table, eliminating repeating groups.

#### 7.1.2 Second Normal Form (2NF)

Since all custom tables use single-column surrogate keys (bigint AUTO_INCREMENT), there are no partial dependencies, and 2NF is trivially satisfied.

#### 7.1.3 Third Normal Form (3NF)

In `rides_ride`, all non-key attributes depend solely on `id`. In `rides_rideparticipant`, `contact_number` and `pickup_location` depend on the `(ride_id, user_id)` booking. No transitive dependencies are present; 3NF is satisfied throughout.

#### 7.1.4 Boyce-Codd Normal Form (BCNF)

BCNF is satisfied in all tables. Each table has exactly one candidate key (the surrogate primary key), and every functional dependency is of the form `{PK} → {attribute}`.

### 7.2 Relationships and Keys

| **Relationship** | **Type** | **Foreign Key** | **ON DELETE** |
|---|---|---|---|
| auth_user → rides_ride | One-to-Many | rides_ride.driver_id → auth_user.id | CASCADE |
| rides_ride → rides_ridepickupstop | One-to-Many | rides_ridepickupstop.ride_id → rides_ride.id | CASCADE |
| rides_ride → rides_rideparticipant | One-to-Many | rides_rideparticipant.ride_id → rides_ride.id | CASCADE |
| auth_user → rides_rideparticipant | One-to-Many | rides_rideparticipant.user_id → auth_user.id | CASCADE |

### 7.3 Unique Constraints

| **Table** | **Unique Constraint** | **Business Rule Enforced** |
|---|---|---|
| rides_ridepickupstop | (ride_id, stop_order) | Each stop position within a ride is unique |
| rides_rideparticipant | (ride_id, user_id) | A user cannot book the same ride twice |

### 7.4 Indexing

| **Table** | **Index Column(s)** | **Type** | **Purpose** |
|---|---|---|---|
| rides_ride | driver_id | B-Tree | Fast lookup of rides by driver |
| rides_ride | departure_time | B-Tree | Efficient range filtering for future rides |
| rides_ride | status | B-Tree | Fast filtering by ride lifecycle state |
| rides_ride | created_at | B-Tree | Ordering/pagination by creation time |
| rides_rideparticipant | ride_id | B-Tree | FK join performance |
| rides_rideparticipant | user_id | B-Tree | Lookup of all rides joined by a user |
| rides_rideparticipant | payment_status | B-Tree | Filter pending payments |
| rides_ridepickupstop | ride_id | B-Tree | FK join performance for stop listing |

### 7.5 Transactions

Two views use explicit database transactions:

- **`join_ride_view`**: Wraps `RideParticipant` creation + `seats_available` decrement in `@transaction.atomic`. The `select_for_update()` call acquires a row-level lock on the Ride record.
- **`finalize_ride_view`**: Wraps ride status update in `@transaction.atomic` to ensure the `finalize()` call is atomic.
- **`simulate_payment_view`**: Wrapped in `@transaction.atomic` to ensure `payment_status` and `paid_at` are updated as a single unit.

### 7.6 Security Considerations

- **Parameterized queries**: Django's ORM exclusively generates parameterized SQL, making SQL injection attacks impossible.
- **CSRF tokens**: Every HTML form includes `{% csrf_token %}`.
- **Object-level authorization**: Views verify ownership before allowing mutations.
- **Environment-variable configuration**: Database credentials are loaded from environment variables, not hardcoded.
- **Password hashing**: Django stores passwords using PBKDF2-SHA256 with per-user salts.

---

## 8. Discussion

### 8.1 Challenges Faced

- **Concurrency in seat booking**: Early prototypes used a simple read-then-write pattern vulnerable to TOCTOU race conditions. The solution — wrapping the operation in `@transaction.atomic` with `select_for_update()` — required understanding MySQL's InnoDB row locking semantics.
- **Multi-stop input design**: Designing a user-friendly input for an ordered list of stops without JavaScript-based dynamic form fields was challenging. The solution — a free-text Textarea accepting comma or newline-separated stops — balances simplicity with usability.
- **PyMySQL compatibility**: PyMySQL must be installed as MySQLdb before Django initializes, handled in `config/__init__.py` via `pymysql.install_as_MySQLdb()`.
- **Status lifecycle management**: Ensuring seat availability decrements, status transitions (OPEN → ACTIVE → FINALIZED), and payment gating remained consistent required careful ordering of operations in each view.

### 8.2 Problems Encountered and Solutions

The most significant problem was designing the pickup stop system. The naive approach of storing a comma-delimited string in a text field was rejected because it violates 1NF. The correct solution — introducing a separate `RidePickupStop` table (migration `0002_ridepickupstop.py`) — required a second migration and backward-compatibility handling in the `Ride.pickup_locations` property.

### 8.3 Learning Outcomes

- **Database design**: Practical application of normalization up to BCNF, constraint design, and indexing strategy.
- **ORM usage**: Deep familiarity with Django's ORM including `select_related`, `prefetch_related`, `select_for_update`, F expressions, and `update_fields` optimization.
- **Transaction management**: Understanding of ACID properties and practical implementation of atomic transactions to prevent race conditions.
- **Django architecture**: Comprehensive understanding of the MVT pattern, URL routing, form validation lifecycle, and session-based authentication.

---

## 9. Future Enhancements

### 9.1 Scalability Improvements

- Connection pooling via PgBouncer or `django-db-geventpool` to handle traffic spikes.
- Database read replicas for read-heavy query offloading.
- Redis-based caching layer for available-rides queries using Django's cache framework.
- Horizontal scaling with load balancing (e.g., Nginx + Gunicorn worker pool).

### 9.2 Security Enhancements

- University email verification during signup (restricting registration to `.edu.pk` addresses).
- Rate limiting on join and payment endpoints.
- Production `SECRET_KEY` management using Django-Environ or AWS Secrets Manager.
- HTTPS enforcement via `SECURE_SSL_REDIRECT = True` and HSTS headers.
- Two-factor authentication (2FA) for sensitive operations.

### 9.3 Cloud Deployment

Recommended cloud targets include:

- **AWS EC2 + RDS MySQL**: Production-grade deployment with managed database backups.
- **Railway.app or Render.com**: Zero-configuration PaaS deployment.
- **Docker containerization**: `Dockerfile` + `docker-compose.yml` for consistent environment packaging and CI/CD pipeline integration.

### 9.4 AI and Smart Matching

- **Route matching algorithm**: Use geographic APIs (Google Maps Distance Matrix) to automatically suggest rides with routes passing near a passenger's origin.
- **Demand forecasting**: Analyze historical ride data to predict peak commute times.
- **Smart fare suggestion**: ML model trained on route distance, time of day, and historical fares to recommend fair pricing.

### 9.5 Feature Improvements

- Real-time seat availability updates using Django Channels (WebSockets).
- In-app messaging between driver and passengers post-booking.
- Star ratings and reviews for drivers and passengers after ride completion.
- Actual payment gateway integration (JazzCash, EasyPaisa, or Stripe).
- Push notifications via Firebase Cloud Messaging.
- Mobile native app using React Native or Flutter consuming a Django REST Framework (DRF) API backend.
- University ID verification at signup using FAST-NUCES student portal API.

---

## Conclusion

UniCarpool was conceived as a solution to a genuine commuting challenge faced by university students in Karachi and developed as a full-stack demonstration of database systems principles in a real-world application context. The project successfully delivers a functional, tested, and well-documented ride-sharing platform that covers the complete lifecycle of a shared commute — from ride posting and passenger discovery to seat booking, driver finalization, and payment settlement.

The relational database design reflects careful application of normalization theory, constraint design, and indexing strategy. The four-table schema — centered on `rides_ride`, `rides_rideparticipant`, `rides_ridepickupstop`, and Django's `auth_user` — models the carpooling domain accurately while maintaining BCNF compliance and referential integrity through CASCADE foreign keys.

On the application side, the project demonstrates mature use of the Django ORM including atomic transactions, row-level locking, and N+1 query elimination. All stated functional objectives were accomplished: user authentication, ride creation with multi-stop support, seat-booking with concurrency protection, driver finalization, passenger payment simulation, and ride history display. Four automated unit tests provide a regression test suite covering the critical happy paths.

With the addition of real geolocation matching, real payment processing, and cloud deployment, UniCarpool could realistically serve as a production-grade campus mobility tool. Its open-source codebase, environment-variable configuration, and clean Django architecture ensure that such extensions can be pursued with minimal friction.
