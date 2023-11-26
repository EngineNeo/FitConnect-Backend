-- Insert data into goal_bank
INSERT INTO goal_bank (goal_name) VALUES
('Weight Loss'),
('Muscle Gain'),
('Fitness Maintenance');

-- Insert data into muscle_group_bank
INSERT INTO muscle_group_bank (name) VALUES
('Legs'),
('Back'),
('Chest'),
('Arms'),
('Shoulders'),
('Core');

-- Insert data into equipment_bank
INSERT INTO equipment_bank (name) VALUES
('Dumbbells'),
('Barbell'),
('Treadmill'),
('Resistance Bands'),
('Kettlebell');

-- Insert data into exercise_bank
INSERT INTO exercise_bank (name, description, muscle_group_id, equipment_id) VALUES
('Squat', 'Lower body exercise', 1, 1),
('Bench Press', 'Chest exercise', 3, 2),
('Deadlift', 'Full-body exercise', 2, 1),
('Bicep Curl', 'Isolation exercise', 4, 1),
('Plank', 'Core exercise', 6, NULL);

-- Insert data into user
INSERT INTO user (email, first_name, last_name, gender, birth_date, goal_id, has_coach) VALUES
('user1@example.com', 'John', 'Doe', 'Male', '1990-01-15', 1, 1),
('user2@example.com', 'Jane', 'Smith', 'Female', '1985-05-20', 2, 0),
('user3@example.com', 'Bob', 'Johnson', 'Male', '1995-09-03', 3, 1);

-- Insert data into coach
INSERT INTO coach (user_id, goal_id, experience, cost, bio) VALUES
(1, 1, 5, 50.00, 'Experienced coach specializing in weight loss'),
(3, 3, 3, 40.00, 'Certified fitness trainer with a focus on fitness maintenance');

-- Insert data into user_credentials
INSERT INTO user_credentials (user_id, hashed_password) VALUES
(1, 'hashed_password_1'),
(2, 'hashed_password_2'),
(3, 'hashed_password_3');

-- Insert data into workout_plan
INSERT INTO workout_plan (user_id, plan_name) VALUES
(1, 'Weight Loss Plan'),
(2, 'Beginner Fitness Plan'),
(3, 'Maintenance Workout');

-- Insert data into exercise_in_workout_plan
INSERT INTO exercise_in_workout_plan (plan_id, exercise_id, sets, reps, weight, duration_minutes) VALUES
(1, 1, 3, 12, 50, 30),
(1, 2, 4, 10, 60, NULL),
(2, 3, 3, 15, 70, 45),
(3, 5, 2, 20, NULL, 15);

-- Insert data into workout_log
INSERT INTO workout_log (user_id, exercise_in_plan_id, reps, weight, duration_minutes, completed_date) VALUES
(1, 1, 12, 50, 30, '2023-01-10'),
(1, 2, 10, 60, NULL, '2023-01-10'),
(2, 3, 15, 70, 45, '2023-01-10'),
(3, 3, 20, NULL, 15, '2023-01-10');


-- calorie_log, mental_health_log, message_log, physical_health_log, water_log

-- Insert data into calorie_log
INSERT INTO calorie_log (user_id, amount, recorded_date) VALUES
(1, 500, '2023-01-10'),
(2, 700, '2023-01-10'),
(3, 600, '2023-01-10');

-- Insert data into mental_health_log
INSERT INTO mental_health_log (user_id, mood, recorded_date) VALUES
(1, 'Happy', '2023-01-10'),
(2, 'Neutral', '2023-01-10'),
(3, 'Sad', '2023-01-10');

-- Insert data into message_log
INSERT INTO message_log (sender_id, recipient_id, message_text, sent_date) VALUES
(1, 2, 'Hey Jane, how was your workout today?', '2023-01-10 15:30:00'),
(2, 1, 'Hi John, it went well! Thanks for asking.', '2023-01-10 16:00:00'),
(3, 1, 'Hello John, I have a question about my workout plan.', '2023-01-10 17:45:00');

-- Insert data into physical_health_log
INSERT INTO physical_health_log (user_id, weight, height, recorded_date) VALUES
(1, 75.5, 175, '2023-01-10'),
(2, 65.2, 160, '2023-01-10'),
(3, 80.0, 180, '2023-01-10');

-- Insert data into water_log
INSERT INTO water_log (user_id, amount, recorded_date) VALUES
(1, 1500, '2023-01-10'),
(2, 1000, '2023-01-10'),
(3, 1200, '2023-01-10');
