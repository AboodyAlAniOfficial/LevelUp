--QUERY 1, to create a temporary table.
CREATE TEMP TABLE temp_nutrientAmount (
    FoodID INT,
    NutrientID INT,
    NutrientValue FLOAT,
    StandardError FLOAT,
    NumberofObservations FLOAT,
    NutrientSourceID INT,
    NutrientDateOfEntry DATE
);

--QUERY 2, to copy data to the main table. ENSURE that the import was succesful before running this query.
INSERT INTO nutrientAmount (FoodID, NutrientID, NutrientValue, StandardError, NumberofObservations, NutrientSourceID, NutrientDateOfEntry)
SELECT FoodID, NutrientID, NutrientValue, StandardError, NumberofObservations, NutrientSourceID, NutrientDateOfEntry
FROM temp_nutrientAmount
WHERE NutrientID IN (203, 204, 205, 208);


--QUERY 3, to drop the temporary table. It's a good idea to run the corresponding select query before dropping this table.
DROP TABLE temp_nutrientAmount;

--Select Queries: 
select * from levelup.fooddata;

select * from levelup.nutrientsname;

select * from levelup.nutrientamount;

