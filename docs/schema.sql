-- ============================================================================
-- UniCarpool Database Schema (MySQL)
-- Generated from Django ORM models in rides/models.py
-- ============================================================================

-- Note: The `auth_user` table is created by Django's default auth app.
-- This schema focuses on the custom carpool models.

-- ============================================================================
-- TABLE: rides_ride
-- Django Model: Ride
-- ============================================================================
CREATE TABLE IF NOT EXISTS `rides_ride` (
    `id` bigint AUTO_INCREMENT PRIMARY KEY,
    `driver_id` bigint NOT NULL,
    `origin` varchar(120) NOT NULL,
    `destination` varchar(120) NOT NULL,
    `departure_time` datetime NOT NULL,
    `pickup_point` varchar(120) NOT NULL,
    `seats_total` int UNSIGNED NOT NULL DEFAULT 1,
    `seats_available` int UNSIGNED NOT NULL DEFAULT 1,
    `fare_per_seat` decimal(7, 2) NOT NULL,
    `notes` longtext NOT NULL DEFAULT '',
    `status` varchar(16) NOT NULL DEFAULT 'OPEN',
    `finalized_at` datetime NULL DEFAULT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key: driver -> auth_user
    CONSTRAINT `rides_ride_driver_id_fk` 
        FOREIGN KEY (`driver_id`) REFERENCES `auth_user`(`id`) ON DELETE CASCADE,
    
    -- Indexes for common queries
    INDEX `rides_ride_driver_id` (`driver_id`),
    INDEX `rides_ride_departure_time` (`departure_time`),
    INDEX `rides_ride_status` (`status`),
    INDEX `rides_ride_created_at` (`created_at`)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: rides_ridepickupstop
-- Django Model: RidePickupStop
-- ============================================================================
CREATE TABLE IF NOT EXISTS `rides_ridepickupstop` (
    `id` bigint AUTO_INCREMENT PRIMARY KEY,
    `ride_id` bigint NOT NULL,
    `location` varchar(120) NOT NULL,
    `stop_order` int UNSIGNED NOT NULL DEFAULT 1,
    
    -- Foreign Key: ride -> rides_ride (CASCADE DELETE)
    CONSTRAINT `rides_ridepickupstop_ride_id_fk` 
        FOREIGN KEY (`ride_id`) REFERENCES `rides_ride`(`id`) ON DELETE CASCADE,
    
    -- Unique constraint: (ride_id, stop_order)
    -- Ensures no duplicate stop orders per ride
    UNIQUE KEY `rides_ridepickupstop_ride_stop_order_unique` 
        (`ride_id`, `stop_order`),
    
    -- Indexes for queries
    INDEX `rides_ridepickupstop_ride_id` (`ride_id`),
    INDEX `rides_ridepickupstop_stop_order` (`stop_order`)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLE: rides_rideparticipant
-- Django Model: RideParticipant
-- ============================================================================
CREATE TABLE IF NOT EXISTS `rides_rideparticipant` (
    `id` bigint AUTO_INCREMENT PRIMARY KEY,
    `ride_id` bigint NOT NULL,
    `user_id` bigint NOT NULL,
    `contact_number` varchar(20) NOT NULL,
    `pickup_location` varchar(120) NOT NULL,
    `payment_status` varchar(12) NOT NULL DEFAULT 'PENDING',
    `paid_at` datetime NULL DEFAULT NULL,
    `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key: ride -> rides_ride (CASCADE Delete)
    CONSTRAINT `rides_rideparticipant_ride_id_fk` 
        FOREIGN KEY (`ride_id`) REFERENCES `rides_ride`(`id`) ON DELETE CASCADE,
    
    -- Foreign Key: user -> auth_user (CASCADE Delete)
    CONSTRAINT `rides_rideparticipant_user_id_fk` 
        FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`) ON DELETE CASCADE,
    
    -- Unique constraint: (ride_id, user_id)
    -- Ensures a user cannot join the same ride twice
    UNIQUE KEY `rides_rideparticipant_ride_user_unique` 
        (`ride_id`, `user_id`),
    
    -- Indexes for queries
    INDEX `rides_rideparticipant_ride_id` (`ride_id`),
    INDEX `rides_rideparticipant_user_id` (`user_id`),
    INDEX `rides_rideparticipant_payment_status` (`payment_status`),
    INDEX `rides_rideparticipant_joined_at` (`joined_at`)
) 
ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SUMMARY OF CONSTRAINTS AND RELATIONSHIPS
-- ============================================================================
-- 
-- Foreign Keys (all with CASCADE ON DELETE):
--   1. rides_ride.driver_id -> auth_user.id
--   2. rides_ridepickupstop.ride_id -> rides_ride.id
--   3. rides_rideparticipant.ride_id -> rides_ride.id
--   4. rides_rideparticipant.user_id -> auth_user.id
--
-- Unique Constraints:
--   1. rides_ridepickupstop(ride_id, stop_order)
--   2. rides_rideparticipant(ride_id, user_id)
--
-- Cardinality:
--   - User (1) drives (many) Rides
--   - User (1) joins (many) RideParticipants
--   - Ride (1) has (many) RidePickupStops
--   - Ride (1) has (many) RideParticipants
--
-- ============================================================================
