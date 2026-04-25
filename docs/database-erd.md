# Database Entities and Relationships

This project uses MySQL with Django ORM models in `rides/models.py` plus Django's built-in `auth_user` table.

## ER Diagram (Logical)

```mermaid
erDiagram
    USER ||--o{ RIDE : drives
    USER ||--o{ RIDE_PARTICIPANT : joins
    RIDE ||--o{ RIDE_PARTICIPANT : has
    RIDE ||--o{ RIDE_PICKUP_STOP : has

    USER {
        bigint id PK
        varchar username
        varchar email
    }

    RIDE {
        bigint id PK
        bigint driver_id FK
        varchar origin
        varchar destination
        datetime departure_time
        varchar pickup_point
        int seats_total
        int seats_available
        decimal fare_per_seat
        varchar status
        datetime finalized_at
        datetime created_at
        datetime updated_at
    }

    RIDE_PARTICIPANT {
        bigint id PK
        bigint ride_id FK
        bigint user_id FK
        varchar contact_number
        varchar pickup_location
        varchar payment_status
        datetime paid_at
        datetime joined_at
    }

    RIDE_PICKUP_STOP {
        bigint id PK
        bigint ride_id FK
        varchar location
        int stop_order
    }
```

## Relationship Diagram (Cardinality View)

```text
auth_user (1) --------< (many) rides_ride
     |                         |
     |                         +--------< (many) rides_ridepickupstop
     |
     +--------< (many) rides_rideparticipant >-------- (1) rides_ride
```

## Constraints and Keys

- `rides_ride.driver_id -> auth_user.id` (`ForeignKey`, `CASCADE`).
- `rides_rideparticipant.ride_id -> rides_ride.id` (`ForeignKey`, `CASCADE`).
- `rides_rideparticipant.user_id -> auth_user.id` (`ForeignKey`, `CASCADE`).
- `rides_ridepickupstop.ride_id -> rides_ride.id` (`ForeignKey`, `CASCADE`).
- Unique constraint on `rides_rideparticipant(ride_id, user_id)`.
- Unique constraint on `rides_ridepickupstop(ride_id, stop_order)`.

## Table Mapping (Django default names)

- `Ride` -> `rides_ride`
- `RideParticipant` -> `rides_rideparticipant`
- `RidePickupStop` -> `rides_ridepickupstop`
- `User` (Django auth) -> `auth_user`
