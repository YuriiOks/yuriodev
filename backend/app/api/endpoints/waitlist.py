import csv
import os
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, EmailStr, validator

router = APIRouter()

# Define the path for the CSV file.
# Storing it in the backend root for simplicity in this MVP.
# In a production setup, this should be a configurable path, ideally a mounted volume.
CSV_FILE_PATH = Path(os.getenv("WAITLIST_CSV_PATH", "waitlist_emails.csv"))

class WaitlistEntry(BaseModel):
    email: EmailStr

    @validator("email")
    def email_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        return v

@router.post("/waitlist", status_code=201)
async def add_to_waitlist(entry: WaitlistEntry = Body(...)):
    """
    Adds an email to the waitlist.
    Stores the email and a timestamp in a CSV file.
    """
    email = entry.email.strip() # Ensure leading/trailing whitespace is removed

    # Basic check if email is already in the list (optional, can make file I/O heavy)
    # For this simple MVP, we might skip this to avoid reading the file on every POST.
    # If implementing, ensure efficient reading or use a database for proper checks.

    try:
        file_exists = CSV_FILE_PATH.exists()
        with open(CSV_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists or CSV_FILE_PATH.stat().st_size == 0:
                writer.writerow(["timestamp", "email"])  # Write header if new file
            
            # Check if email already exists (simple check)
            # This is not very efficient for large files.
            if file_exists and CSV_FILE_PATH.stat().st_size > 0 :
                with open(CSV_FILE_PATH, mode="r", newline="", encoding="utf-8") as read_file:
                    reader = csv.reader(read_file)
                    next(reader, None) # skip header
                    for row in reader:
                        if len(row) > 1 and row[1] == email:
                            # Not an error, but indicates already subscribed.
                            # Could return a 200 OK with a specific message.
                            return {"message": "Email already subscribed"}
            
            timestamp = datetime.utcnow().isoformat()
            writer.writerow([timestamp, email])
        
        return {"message": "Successfully subscribed to the waitlist!"}
    except IOError as e:
        # Log the error e.g., logging.error(f"Could not write to CSV: {e}")
        raise HTTPException(status_code=500, detail="Could not save email due to a server error.")
    except Exception as e:
        # Log the error
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Optional: Add a GET endpoint to view waitlist (for admin purposes, protect appropriately in real app)
# @router.get("/waitlist")
# async def get_waitlist():
#     if not CSV_FILE_PATH.exists():
#         return []
#     with open(CSV_FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
#         reader = csv.DictReader(file)
#         return list(reader)
