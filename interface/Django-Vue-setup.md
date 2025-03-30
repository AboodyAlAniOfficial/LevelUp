# Commands required to initialize the applications:
## For Django:
> pip install venv\
> ./venv/Scripts/activate ('deactivate' to exit the virtual environment)\
> pip install django\
> pip install django-rest-framework\
> pip install djoser\
> pip install pillow\
> pip install django-cors-headers\
> pip install psycopg2-binary\
> django-admin startproject levelup_django\
> cd levelup_django

Then, copy the settings.py and urls.py files from this repo.
## For Vue:
> npm install @vue/cli (Requires Node.js installed)\
> vue create levelup_vue (Select Babel, Vuex, Router, CSS-Preprocessors, version 3.x, Yes, Sass/SCSS, In dedicated config files, and No)\
> cd levelup_vue\
> npm install axios\
> npm install bulma

Copy App.vue into levelup_vue/src and index.js into levelup_vue/src/router.

*Further tutorial might be added later*
