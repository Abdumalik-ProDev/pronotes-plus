import asyncio
import logging
from app.core.database import AsyncSessionLocal, create_db_and_tables
from app.models import User, Note
from app.repositories import UserRepo, NoteRepo

async def seed_data():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    await create_db_and_tables()
    async with AsyncSessionLocal() as session:

        user_repo = UserRepo(session)
        if user_repo is None:
            logger.error("UserRepository is not initialized properly.")
            return "Initialization Error"
        
        note_repo = NoteRepo(session)
        if note_repo is None:
            logger.error("NoteRepository is not initialized properly.")
            return "Initialization Error"

        # Check if users already exist
        existing_users = await user_repo.get_all()
        if existing_users:
            logger.info("Users already exist, skipping seeding.")
            return "Users already exist"

        # Create sample users
        users = [
            User(username="ProDev", email="abdumalikbakhtiyorov007@gmail.com",
                  hashed_password="hashedpassword1"),
            User(username="JaneDoe", email="janedoneorg@gmail.com",
                  hashed_password="hashedpassword2")
        ]
        for user in users:
            await user_repo.create(user)
            logger.info(f"Created user: {user.username}")

        # Create sample notes
        notes = [
            Note(title="ProDev`s Note", content="This is ProDev's note content.", user_id=1),
            Note(title="Jane's Note", content="This is Jane's note content.", user_id=2)
        ]
        for note in notes:
            await note_repo.create(note)
            logger.info(f"Created note: {note.title}")

        await session.commit()
        logger.info("Database seeding completed.")
        return "Seeding completed"
    
if __name__ == "__main__":
    asyncio.run(seed_data())