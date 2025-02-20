CREATE SCHEMA levelup;

CREATE TABLE levelup.Users (
	-- account/login info
	user_id SERIAL PRIMARY KEY,
	username VARCHAR(64),
	passwordHash VARCHAR(64),

	-- preferences
	mass_unit ENUM('kg', 'lb'),
	energy_unit ENUM('kJ', 'Cal'),
	visibility ENUM('private', 'public'),

	-- health data
	height_m FLOAT(53),
	mass_kg FLOAT(53),
	age_yr FLOAT(53),
	sex ENUM('male', 'female')
);
