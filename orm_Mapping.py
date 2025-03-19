from sqlalchemy import (
    create_engine, Column, Integer, String, Text, ForeignKey, Date,
    Double, DECIMAL, TIMESTAMP, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Database connection details
DATABASE_URL = "postgresql+psycopg2://postgres:newpassword@localhost:5432/test"


# Create database engine
engine = create_engine(DATABASE_URL)

# Specify schema globally
SCHEMA_NAME = "levelup"

# Define base for ORM models
Base = declarative_base()

# Define ORM model for 'users' table in 'levelup' schema
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "levelup"}  # Specify schema

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, unique=True)
    passwordhash = Column(String(64), nullable=False)
    mass_unit = Column(String(16))  # kg, lb
    energy_unit = Column(String(16))  # kJ, cal
    visibility = Column(String(16))  # public/private
    height_m = Column(Double)  # Height in meters
    mass_kg = Column(Double)  # Mass in kg
    age_yr = Column(Double)  # Age in years
    sex = Column(String(16))  # male/female

    # Relationships
    health_goals = relationship("HealthGoal", back_populates="user", cascade="all, delete")
    exercises = relationship("Exercise", back_populates="user", cascade="all, delete")
    followers = relationship("Follower", foreign_keys="[Follower.user_id]", back_populates="user",
                             cascade="all, delete")
    following = relationship("Follower", foreign_keys="[Follower.follows_user_id]", back_populates="followed_user",
                             cascade="all, delete")
   # meals = relationship("Meal", back_populates="user", cascade="all, delete")


# ================================
# HealthGoals Table
# ================================
class HealthGoal(Base):
    __tablename__ = "healthgoals"
    __table_args__ = {"schema": "levelup"}

    goal_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("levelup.users.user_id", ondelete="CASCADE"))
    target_weight = Column(DECIMAL(5, 2))
    daily_calorie_goal = Column(Integer, CheckConstraint("daily_calorie_goal >= 0"))
    daily_steps_goal = Column(Integer, CheckConstraint("daily_steps_goal >= 0"))
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationship
    user = relationship("User", back_populates="health_goals")
# ================================
# Exercises Table
# ================================
class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = {"schema": "levelup"}

    exercise_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("levelup.users.user_id", ondelete="CASCADE"))
    exercise_type = Column(String(100))
    duration_minutes = Column(Integer, CheckConstraint("duration_minutes >= 0"))
    calories_burnt = Column(Integer, CheckConstraint("calories_burnt >= 0"))

    # Relationship
    user = relationship("User", back_populates="exercises")

# ================================
# Followers Table
# ================================
class Follower(Base):
    __tablename__ = "followers"
    __table_args__ = {"schema": "levelup"}

    follower_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("levelup.users.user_id", ondelete="CASCADE"))  # Follower
    follows_user_id = Column(Integer, ForeignKey("levelup.users.user_id", ondelete="CASCADE"))  # Following

    # Unique constraint to prevent duplicate follow relationships
    __table_args__ = (
        UniqueConstraint("user_id", "follows_user_id"),
        {"schema": "levelup"}
    )

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="followers")
    followed_user = relationship("User", foreign_keys=[follows_user_id], back_populates="following")

# ================================
# FoodData Table
# ================================
class FoodData(Base):
    __tablename__ = "fooddata"
    __table_args__ = {"schema": "levelup"}

    foodid = Column(Integer, primary_key=True)
    foodcode = Column(Integer)
    foodgroupid = Column(Integer)
    foodsourceid = Column(Integer)
    fooddescription = Column(Text)
    fooddescriptionf = Column(Text)
    fooddateofentry = Column(Date)
    fooddateofpublication = Column(Date)
    countrycode = Column(Integer)
    scientificname = Column(Text)
# ================================
# NutrientsName Table
# ================================
class NutrientsName(Base):
    __tablename__ = "nutrientsname"
    __table_args__ = {"schema": "levelup"}

    nutrient_id = Column(Integer, primary_key=True)
    nutrient_code = Column(Integer)
    nutrient_symbol = Column(String(50))
    nutrient_unit = Column(String(50))
    nutrient_name = Column(String(255))
    nutrient_name_f = Column(String(255))
    tag_name = Column(String(50))
    nutrient_decimal = Column(Integer)

# ================================
# NutrientAmount Table
# ================================
class NutrientAmount(Base):
    __tablename__ = "nutrientamount"
    __table_args__ = {"schema": "levelup"}

    foodid = Column(Integer, ForeignKey("levelup.fooddata.food_id", ondelete="CASCADE"), primary_key=True)
    nutrientid = Column(Integer, ForeignKey("levelup.nutrientsname.nutrient_id", ondelete="CASCADE"), primary_key=True)
    nutrientvalue = Column(Double)
    standarderror = Column(Double)
    numberofobserv = Column(Double)
    nutrientsourceid = Column(Integer)
    nutrientdateofen = Column(Date)

class Meal(Base):
    __tablename__ = 'meals'
    __table_args__ = {"schema": "levelup"}

    meal_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    food_id = Column(Integer, nullable=True)
    meal_name = Column(String(255), nullable=True)
    calories = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)
    fats = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

# ================================
# Example of insertion into meals table
# ================================

# Create session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


#Replace 1 with user's corresponding user ID
#Using first() returns 1 tuple so we don't need to iterate the value through a loop
user = session.query(User).filter(User.user_id == 1).first()
print(user.user_id, user.username)


#Replace 2 with the user's choice of food
food = session.query(FoodData).filter(FoodData.foodid == 2).first()
print(food.fooddescription)



#Replace 2 with the user's choice of food
#Using all() returns a list of tuples, so it is necessary to iterate through a loop to grab the values
nuts = session.query(NutrientAmount).filter(NutrientAmount.foodid == 2).all()
for nut in nuts:
    if nut.nutrientid == 203:
        protein = nut.nutrientvalue
    if nut.nutrientid == 204:
        fats = nut.nutrientvalue
    if nut.nutrientid == 205:
        carbs = nut.nutrientvalue
    if nut.nutrientid == 208:
        calories = nut.nutrientvalue

print("protein: " + str(protein) +
      " fats: " + str(fats) +
      " carbs: " + str(carbs) +
      " calories: " + str(calories))

#Alternative method of grabbing same data, little less straightforward IMO, but gets rid of the squiggly lines
#You will want to replace the 2 with the users chosen food
protein2 = session.query(NutrientAmount.nutrientvalue).filter(NutrientAmount.foodid == 2, NutrientAmount.nutrientid == 203).scalar()
fats2 = session.query(NutrientAmount.nutrientvalue).filter(NutrientAmount.foodid == 2, NutrientAmount.nutrientid == 204).scalar()
carbs2 = session.query(NutrientAmount.nutrientvalue).filter(NutrientAmount.foodid == 2, NutrientAmount.nutrientid == 205).scalar()
calories2 = session.query(NutrientAmount.nutrientvalue).filter(NutrientAmount.foodid == 2, NutrientAmount.nutrientid == 208).scalar()
print("protein: " + str(protein2) +
      " fats: " + str(fats2) +
      " carbs: " + str(carbs2) +
      " calories: " + str(calories2))

new_meal = Meal(
    meal_id=2,
    user_id=user.user_id,
    food_id=2,
    meal_name="", #Replace this with the users chosen name for the meal
    calories=calories2,
    protein=protein,
    carbs=carbs,
    fats=fats2,
    description= food.fooddescription
)

# Add to session and commit
session.add(new_meal)
session.commit()


meals = session.query(Meal).all()
for meal in meals:
    print(meal.meal_id, meal.meal_name, meal.calories, meal.protein, meal.carbs, meal.fats, meal.description)



session.close()
