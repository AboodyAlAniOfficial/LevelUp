CREATE SCHEMA levelup;

CREATE TYPE sex as ENUM ('male', 'female');
CREATE TYPE visibility as ENUM ('private', 'public');

CREATE TABLE levelup.Users (
	-- account/login info
	user_id SERIAL PRIMARY KEY,
	username VARCHAR(64) UNIQUE,
	passwordHash VARCHAR(64),

	-- preferences
	mass_unit VARCHAR(16) DEFAULT 'kg',
	energy_unit VARCHAR(16) DEFAULT 'kJ',
	visibility visibility DEFAULT 'private',

	-- health data
	height_m FLOAT(53),
	mass_kg FLOAT(53),
	age_yr FLOAT(53),
	sex sex
);