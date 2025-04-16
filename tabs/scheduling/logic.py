
from db import get_connection

def fetch_jobs():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM jobs ORDER BY date")
        return c.fetchall()

def refresh_job_list(job_listbox):
    jobs = fetch_jobs()
    job_listbox.delete(0, "end")
    for job in jobs:
        job_listbox.insert("end", f"{job['date']} - {job['customer_name']} - {job['service']}")
    job_listbox.jobs = jobs

def delete_job(job_listbox):
    selected = job_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    job_id = job_listbox.jobs[index]["id"]

    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
    refresh_job_list(job_listbox)
