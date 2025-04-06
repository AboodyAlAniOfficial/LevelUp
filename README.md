# LevelUp

## Project Authors

This project was created by the following people:
- Abood Al-Ani (218938993) <aboodyaa@my.yorku.ca>  
- Nikhil Arora (220874947) <narora46@my.yorku.ca>  
- Adrien Hopkins (217267550) <ahopk127@my.yorku.ca>  
- Hamad Iqbal (217296393) <hamadi8@my.yorku.ca>  
- Bilal Jameel (216567380) <bilaljameel665@gmail.com>/<bilal665@my.yorku.ca>  
- Tan Khoa Tran (218060541) <rickt02@my.yorku.ca>

## Backend

### Dependencies

- [Python 3](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

### Installation Instructions

1. Setup the dependencies above if you haven't already.
2. Clone the repository if you haven't already.  The directory where your LevelUp repository is stored shall henceforth be referred to as "[LEVELUP]".
3. The backend requires you to set your database information in environment variables.  Set `LEVELUP_DBUSER` and `LEVELUP_DBPASS` to the username and password of the postgresql account you want to use.
4. Run the following commands to setup Django and the database, from [LEVELUP]:

Windows:
```powershell
cd .\interface\levelup_django\levelup_django
python -m venv .venv
.venv\Scripts\activate
pip install django django-rest-framework djoser pillow django-cors-headers psycopg2-binary
python manage.py migrate
```

Unix:
```sh
cd interface/levelup_django/levelup_django
python -m venv .venv
.venv/bin/activate
pip install django django-rest-framework djoser pillow django-cors-headers psycopg2-binary
python manage.py migrate
```

To populate the database, do the following:
1. Have the database already set up (See Above).
2. On `pgAdmin`, and on the "Object Explorer" page, go to servers ->your server->Databases->Schemas->levelup->Tables->fooddata. Right-click it, and then select "import/export data". Import the file [FOOD_NAME_UTF8_CLEANED.csv](./FOOD_NAME_UTF8_CLEANED.csv). Make sure the format is "csv" and the encoding is "UTF8".
3. Go to servers ->your server->Databases->Schemas->levelup->Tables->nutrientsname. Right-click it, and then select "import/export data". Import the file [NUTRIENT NAME.csv](./NUTRIENT_NAME.csv). Ensure the format is "csv" and the encoding is "LATIN1".
4. To import the nutrient amounts, we first need to make a temporary table to insert all the values into and then insert the necessary values into our main table. First, run the first query given in the [setup queries.sql](./setup_queries.sql) file, to create the temp table.
5. Go to servers ->your server->Databases->Schemas->levelup->Tables->temp_nutrientamount. Right-click it, and then select "import/export data". Import the file [NUTRIENT AMOUNT.csv](./NUTRIENT_AMOUNT.csv). Ensure the format is "csv" and the encoding is "LATIN1".
6. Run the second query given in the [setup queries.sql](./setup_queries.sql) file to copy the necessary tuples into the main table (i.e., the tuples for protein, carbs, fats, and calories).
7. Run the third query given in the [setup queries.sql](./setup_queries.sql) file to drop the temp_nutrientamount table, as it is no longer needed.
8. Ensure everything is done correctly by running the select queries given in the setup queries.sql file to list all the tuples.

### Execution

1. Go to the same directory you installed LevelUp in (`[LEVELUP]`).
2. Run the following commands:

Windows:
```powershell
cd .\interface\levelup_django\levelup_django
.venv\Scripts\activate
python manage.py runserver
```

Unix:
```powershell
cd ./interface/levelup_django/levelup_django
.venv/bin/activate
python manage.py runserver
```

## Frontend

### Dependencies

- [NodeJS](https://nodejs.org/)

### Setup & Execution Instructions

1. Go to `interface/levelup_vue/levelup_vue`.
2. Run `npm install`.

To run the frontend, run `npm run serve` from the same directory.  Your website should be at http://localhost:8080/.

## Documentation Instructions

We are using Markdown files to create our documentation, as they can be stored in our git repository and edited and reviewed by the same means as our code.

To turn a markdown file into a pdf, we can use the program [Pandoc](https://pandoc.org/).  Run the following command to turn the markdown file `doc.md` into `doc.pdf`:

```shell
pandoc doc.md -o doc.pdf --variable colorlinks=true
```

Don't bother storing PDF files in the repository; that's just a waste of space and they can easily be created with the command.

Here is a guide to Markdown syntax, in case anyone needs it:  
[The Markdown Guide](https://www.markdownguide.org/)
