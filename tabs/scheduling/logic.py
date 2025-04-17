from db import get_connection

# Original scheduling tab logic
def fetch_jobs():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM jobs ORDER BY date")
        return c.fetchall()

def delete_job(job_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()

# Calendar-specific job logic
def get_jobs_for_day(year, month, day):
    date = f"{year:04d}-{month:02d}-{day:02d}"
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT job FROM calendar_jobs WHERE date = ?", (date,))
        return [row["job"] for row in c.fetchall()]

def save_job_for_day(year, month, day, job):
    date = f"{year:04d}-{month:02d}-{day:02d}"
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS calendar_jobs (id INTEGER PRIMARY KEY, date TEXT, job TEXT)")
        c.execute("INSERT INTO calendar_jobs (date, job) VALUES (?, ?)", (date, job))
        conn.commit()