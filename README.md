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

The backend is a Django server than use PostgreSQL as its database.

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
1. **Have the database already set up**  
   (See instructions above on creating the PostgreSQL `levelup` schema and connecting through pgAdmin).

2. **Open the schema and locate the `fooddata` table**  
   In `pgAdmin`, navigate through the left panel under:  
   `Servers → your server → Databases → levelup → Schemas → levelup → Tables → fooddata`

3. **Import the food database CSV**  
   - Right-click on `fooddata` and select **Import/Export Data**.
   - Under the **General** tab, select **Import** as the option.
   - Click the folder icon beside **Filename** and browse to the file named:  
     `food database (updated).csv`  
     This file is located within the **Starter db files** folder inside your `levelup` project directory.
   - Set the **Format** to `"csv"` and the **Encoding** to `"UTF8"`.

4. **Set import options correctly**  
   - Switch to the **Options** tab.
   - Set **Header** to `"Yes"` to indicate that the first row of the CSV file contains column names.

5. **Click OK** to start the import**  
   Once complete, your predefined food database will be populated and ready to use.

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

The frontend is based on Vue.js, which depends on NodeJS.

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
