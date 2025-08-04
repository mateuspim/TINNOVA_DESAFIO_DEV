from app.db.database import SessionLocal, engine, Base, create_tables
from app.models.brand import Brand

vehicle_brands = [
    "Toyota",
    "Ford",
    "Chevrolet",
    "Honda",
    "Nissan",
    "Volkswagen",
    "Hyundai",
    "Kia",
    "Subaru",
    "Mazda",
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Lexus",
    "Jeep",
    "Dodge",
    "Ram",
    "GMC",
    "Buick",
    "Cadillac",
    "Chrysler",
    "Acura",
    "Infiniti",
    "Lincoln",
    "Volvo",
    "Porsche",
    "Jaguar",
    "Land Rover",
    "Mini",
    "Mitsubishi",
    "Fiat",
    "Alfa Romeo",
    "Genesis",
    "Tesla",
    "Polestar",
    "Suzuki",
    "Peugeot",
    "Renault",
    "Citroën",
    "Skoda",
    "Seat",
    "Saab",
    "Opel",
    "Holden",
    "Isuzu",
    "Dacia",
    "SsangYong",
    "Mahindra",
    "Tata",
    "Great Wall",
]


def seed_brands():
    session = SessionLocal()
    for name in vehicle_brands:
        if not session.query(Brand).filter_by(name=name).first():
            session.add(Brand(name=name))
    session.commit()
    session.close()


if __name__ == "__main__":
    create_tables()
    seed_brands()
