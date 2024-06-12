from fastapi import FastAPI, HTTPException
import sqlite3
import openai
from openai import OpenAI
import uvicorn

# Import data from the database
conn = sqlite3.connect('candidates.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM candidates')
rows = cursor.fetchall()

for row in rows:
    print(row)

app = FastAPI()

# OpenAI API key setup
client = OpenAI(
    api_key = "Insert the key here",
)


# Function to get candidate details from the database
def get_candidate(candidate_id):
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, status, comments FROM candidates WHERE id=?', (candidate_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Endpoint to get personalized email
@app.get("/generate-email/{candidate_id}")
async def generate_email(candidate_id: int):
    candidate = get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    name, status, comments = candidate
    # Use OpenAI to generate a more personalized email
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"""Create a simple mail for {name} including the candidate status, which is {status}, and including the comments given by the hiring team, which is {comments}. This mail is created by Mathew from the hiring team at AVONOV info for the role of data science internship. """,
        max_tokens=500
    )

    personalized_email = response.choices[0].text.strip()
    print(personalized_email)
    return {"email": personalized_email}

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)