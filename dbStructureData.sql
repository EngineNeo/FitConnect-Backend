DROP SCHEMA IF EXISTS fitness;
CREATE SCHEMA fitness;
USE fitness;
-- Note: I added tables for admin, but I commented them out since we did not discuss them.
--       Rubric for MPP required audit tables for full credit. We need to add later. It 
--       looks like Django may have solutions for audit tables.
-- Static 'Bank' Tables
-- Goals Bank
CREATE TABLE goal_bank (
  goal_id INTEGER NOT NULL AUTO_INCREMENT,
  goal_name VARCHAR(255) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (goal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Muscle Group Bank
CREATE TABLE muscle_group_bank (
  muscle_group_id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (muscle_group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Equipment Bank
CREATE TABLE equipment_bank (
  equipment_id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (equipment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exercise Bank
CREATE TABLE exercise_bank (
  exercise_id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  muscle_group_id INTEGER,
  equipment_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (exercise_id),
  FOREIGN KEY (muscle_group_id) REFERENCES muscle_group_bank (muscle_group_id),
  FOREIGN KEY (equipment_id) REFERENCES equipment_bank (equipment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Type Tables
-- User
CREATE TABLE user (
  user_id INTEGER NOT NULL AUTO_INCREMENT,
  email VARCHAR(254) UNIQUE NOT NULL,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  gender ENUM('Male', 'Female'),
  birth_date DATE,
  goal_id INTEGER,
  has_coach BOOL NOT NULL DEFAULT FALSE, -- `Client requests coach` system
  hired_coach_id INTEGER, -- `Client requests coach` system
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  FOREIGN KEY (goal_id) REFERENCES goal_bank (goal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Coach (coach is also a `User`)
CREATE TABLE coach (
  coach_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  goal_id INTEGER,
  experience INTEGER,
  cost DECIMAL(10, 2),
  bio TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (coach_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id),
  FOREIGN KEY (goal_id) REFERENCES goal_bank (goal_id)
);

-- Add FK Relationship user->coach
ALTER TABLE user ADD FOREIGN KEY (hired_coach_id) REFERENCES coach (coach_id);


-- Admin

CREATE TABLE admin (
  admin_id INTEGER NOT NULL AUTO_INCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Credentials Tables
-- Admin Credentials

CREATE TABLE admin_credentials (
  admin_id INTEGER NOT NULL AUTO_INCREMENT,
  hashed_password VARCHAR(120) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (admin_id),
  FOREIGN KEY (admin_id) REFERENCES admin (admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Credentials
CREATE TABLE user_credentials (
  user_id INTEGER NOT NULL AUTO_INCREMENT,
  hashed_password VARCHAR(120) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Admin Feature Tables
-- Become Coach Requests
CREATE TABLE become_coach_request (
  user_id INTEGER NOT NULL,      -- id of user requesting to become coach
  goal_id INTEGER NOT NULL,      -- coach's goal
  experience INTEGER NOT NULL,   -- coach's experience
  cost DECIMAL(10,2) NOT NULL,   -- coach's cost
  is_approved BOOL DEFAULT NULL, -- boolean to see status of request (null = admin must still decide)
  decided_by INTEGER, -- ID of admin that made approved/declined decision
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id),
  FOREIGN KEY (decided_by) REFERENCES admin (admin_id),
  FOREIGN KEY (goal_id) REFERENCES goal_bank (goal_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- User & Coach Feature Tables
-- Logging Tables
-- Calorie Log
CREATE TABLE calorie_log (
  calorie_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  recorded_date DATE DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (calorie_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Water Log
CREATE TABLE water_log (
  water_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  recorded_date DATE DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (water_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Physical Health Log
CREATE TABLE physical_health_log (
  physical_health_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  weight DECIMAL(5, 2),
  height DECIMAL(5, 2),
  recorded_date DATE  DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (physical_health_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mental Health Log
CREATE TABLE mental_health_log (
  mental_health_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  mood ENUM('Happy', 'Neutral', 'Sad') NOT NULL,
  recorded_date DATE DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (mental_health_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Message Log
CREATE TABLE message_log (
  message_id INTEGER NOT NULL AUTO_INCREMENT,
  sender_id INTEGER NOT NULL,
  recipient_id INTEGER NOT NULL,
  message_text TEXT NOT NULL,
  sent_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (message_id),
  FOREIGN KEY (sender_id) REFERENCES user (user_id),
  FOREIGN KEY (recipient_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Workout Feature Tables
-- Notes: We need to add something for a calendar feature to track which workout plans are for what days of the week.
--        We also might want to add a column in workout_plan that tell who created the plan 
-- Workout Plan
CREATE TABLE workout_plan (
  plan_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  plan_name VARCHAR(255) NOT NULL,
  creation_date DATE DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (plan_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exercise(s) in Workout Plan
CREATE TABLE exercise_in_workout_plan (
  exercise_in_plan_id INTEGER NOT NULL AUTO_INCREMENT,
  plan_id INTEGER NOT NULL,
  exercise_id INTEGER NOT NULL,
  sets INTEGER,
  reps INTEGER,
  weight INTEGER,
  duration_minutes INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (exercise_in_plan_id),
  FOREIGN KEY (plan_id) REFERENCES workout_plan (plan_id),
  FOREIGN KEY (exercise_id) REFERENCES exercise_bank (exercise_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Workout (Exercise) Log
CREATE TABLE workout_log (
  workout_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  exercise_in_plan_id INTEGER NOT NULL,
  reps INTEGER,
  weight INTEGER,
  duration_minutes INTEGER,
  completed_date DATE DEFAULT (CURRENT_DATE) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (workout_id),
  FOREIGN KEY (user_id) REFERENCES user (user_id),
  FOREIGN KEY (exercise_in_plan_id) REFERENCES exercise_in_workout_plan (exercise_in_plan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
