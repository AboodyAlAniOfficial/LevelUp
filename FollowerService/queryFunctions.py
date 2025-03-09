from django.db import connection
#this method queries the database for the userID to check if it exists
def get_user_id(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id FROM levelup.Users WHERE username = %s", [username])
        row = cursor.fetchone()
        return row[0] if row else None 
def get_global_leaderboard():
    #gets global usernames and ranks it with top 50 exercise time to display in a global leaderboard
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.username,
                   COALESCE(SUM(e.duration_minutes), 0) AS total_exercise_time
            FROM levelup.Users u
            LEFT JOIN levelup.Exercises e ON u.user_id = e.user_id
            GROUP BY u.user_id
            ORDER BY total_exercise_time DESC
            LIMIT 50;
        """)
        return cursor.fetchall()
