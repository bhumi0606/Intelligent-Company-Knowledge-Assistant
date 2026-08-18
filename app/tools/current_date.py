from datetime import date
from langsmith import traceable

@traceable(name="get current date", project_name="Intelligent-Company-Knowledge-Assistant")
def get_current_date():
    return date.today().isoformat()