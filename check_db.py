import asyncio
from sqlalchemy import select
from src.database.session import AsyncSessionLocal
from src.database.models import PredictionLog

async def check_logs():
    async with AsyncSessionLocal() as session:
        # Query all logs, ordered by newest first
        result = await session.execute(select(PredictionLog).order_by(PredictionLog.id.desc()))
        logs = result.scalars().all()
        
        print(f"\nFound {len(logs)} prediction logs in database:\n")
        for log in logs:
            print(f"ID: {log.id}")
            print(f"Text: '{log.input_text}'")
            print(f"Scores: {log.prediction_scores}")
            print(f"Time: {log.created_at}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(check_logs())