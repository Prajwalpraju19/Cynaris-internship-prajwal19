from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from train import vn

app = FastAPI(
    title="Vanna AI SQL Analyst",
    description="Natural Language to SQL API",
    version="1.0"
)


class SQLRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Vanna AI SQL Analyst is running"
    }


@app.post("/cia/sql-analyst")
def sql_analyst(request: SQLRequest):

    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        # Generate SQL
        sql = vn.generate_sql(question=question)

        if not sql:
            raise HTTPException(
                status_code=400,
                detail="SQL generation failed"
            )

        # Basic read-only check
        normalized_sql = sql.strip().lower()

        if not normalized_sql.startswith("select"):
            raise HTTPException(
                status_code=400,
                detail="Only SELECT queries are allowed"
            )

        # Execute SQL
        result = vn.run_sql(sql)

        return {
            "question": question,
            "generated_sql": sql,
            "results": result.to_dict(orient="records")
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )