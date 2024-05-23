"""
Database configuration for the bookstore application.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """
    Initialize the database and create tables.
    """
    from app import models  # Importing models inside the function to avoid circular imports

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    genres = [
        {"name": "Fiction", "subgenres": [
            {"name": "Fantasy", "subgenres": [
                {"name": "High Fantasy", "subgenres": [
                    {"name": "Epic Fantasy"}
                ]},
                {"name": "Urban Fantasy"}
            ]},
            {"name": "Science Fiction", "subgenres": [
                {"name": "Dystopian"},
                {"name": "Space Opera", "subgenres": [
                    {"name": "Military Sci-Fi"}
                ]}
            ]},
            {"name": "Mystery", "subgenres": [
                {"name": "Detective"},
                {"name": "Cozy Mystery"}
            ]}
        ]},
        {"name": "Non-Fiction", "subgenres": [
            {"name": "Biography", "subgenres": [
                {"name": "Historical Biography"},
                {"name": "Memoir"}
            ]},
            {"name": "Self-Help", "subgenres": [
                {"name": "Personal Development", "subgenres": [
                    {"name": "Motivational"}
                ]},
                {"name": "Psychology"}
            ]},
            {"name": "History", "subgenres": [
                {"name": "Ancient History"},
                {"name": "Modern History", "subgenres": [
                    {"name": "World War II"}
                ]}
            ]}
        ]},
        {"name": "Children's Books", "subgenres": [
            {"name": "Picture Books", "subgenres": [
                {"name": "Bedtime Stories"}
            ]},
            {"name": "Young Adult", "subgenres": [
                {"name": "Fantasy"},
                {"name": "Romance"}
            ]}
        ]},
        {"name": "Romance", "subgenres": [
            {"name": "Contemporary Romance"},
            {"name": "Historical Romance", "subgenres": [
                {"name": "Regency Romance"},
                {"name": "Victorian Romance"}
            ]},
            {"name": "Paranormal Romance", "subgenres": [
                {"name": "Vampire Romance"}
            ]}
        ]},
        {"name": "Horror", "subgenres": [
            {"name": "Gothic Horror"},
            {"name": "Psychological Horror"},
            {"name": "Supernatural Horror", "subgenres": [
                {"name": "Ghost Stories"}
            ]}
        ]}
    ]

    def add_genres(parent, subgenres):
        for subgenre in subgenres:
            genre = models.Genre(name=subgenre['name'], parent=parent)
            session.add(genre)
            session.commit()
            if 'subgenres' in subgenre:
                add_genres(genre, subgenre['subgenres'])

    for genre_data in genres:
        genre = models.Genre(name=genre_data['name'])
        session.add(genre)
        session.commit()
        if 'subgenres' in genre_data:
            add_genres(genre, genre_data['subgenres'])

    session.close()
