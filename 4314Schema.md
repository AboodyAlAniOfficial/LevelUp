# Schema
`
CREATE TABLE Meals (
    meal_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    meal_name VARCHAR(255),
    calories INT CHECK (calories >= 0),
    macronutrients JSONB, -- Stores fats, carbs, proteins
    ingredients JSONB -- Stores the weight of each ingredient 
);
`
`
CREATE TABLE HealthGoals (
    goal_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    target_weight DECIMAL(5,2),
    daily_calorie_goal INT CHECK (daily_calorie_goal >= 0),
    daily_steps_goal INT CHECK (daily_steps_goal >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
`
`
CREATE TABLE Exercises (
    exercise_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    exercise_type VARCHAR(100),
    duration_minutes INT CHECK (duration_minutes >= 0),
    calories_burnt INT CHECK (calories_burnt >= 0),
);
`
`
CREATE TABLE Followers (
    follower_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE, -- This is the 'followers'
    follows_user_id INT REFERENCES Users(user_id) ON DELETE CASCADE -- This is the 'following',
    UNIQUE (user_id, follows_user_id) -- Prevents duplicate follow relationships
);
`
`
CREATE TABLE Leaderboard (
    leaderboard_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    total_distance_km DECIMAL(5,2),
    total_calories_burnt INT,
    weekly_net_weight_change DECIMAL(5,2),
    ranking_position INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
`



