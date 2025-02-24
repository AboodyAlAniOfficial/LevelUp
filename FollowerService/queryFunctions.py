from django.db import connection
#this method queries the database for the userID to check if it exists
def get_user_id(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id FROM levelup.Users WHERE username = %s", [username])
        row = cursor.fetchone()
        return row[0] if row else None 