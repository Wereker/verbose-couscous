import asyncio
from app.db.db_helper import db_helper
from app.models import Brand, Service, Car, Role


async def add_brands():
    async for db in db_helper.session_getter():
        brand1 = Brand(name="Mazda")
        brand2 = Brand(name="Toyota")
        brand3 = Brand(name="Honda")

        db.add(brand1)
        db.add(brand2)
        db.add(brand3)

        try:
            await db.commit()
            print("Brands added successfully")
        except Exception as e:
            await db.rollback()
            print(f"An error occurred: {e}")
        finally:
            await db.close()


async def add_cars():
    async for db in db_helper.session_getter():
        car1 = Car(brand_id=1, model="MX-5 Miata")
        car2 = Car(brand_id=1, model="CX-5")
        car3 = Car(brand_id=2, model="Camry")
        car4 = Car(brand_id=2, model="RAV4")
        car5 = Car(brand_id=3, model="Civic")
        car6 = Car(brand_id=3, model="CR-V")

        db.add(car1)
        db.add(car2)
        db.add(car3)
        db.add(car4)
        db.add(car5)
        db.add(car6)

        try:
            await db.commit()
            print("Cars added successfully")
        except Exception as e:
            await db.rollback()
            print(f"An error occurred: {e}")
        finally:
            await db.close()


async def add_roles():
    async for db in db_helper.session_getter():
        role1 = Role(name="Администратор")
        role2 = Role(name="Работник")
        role3 = Role(name="Клиент")

        db.add(role1)
        db.add(role2)
        db.add(role3)

        try:
            await db.commit()
            print("Roles added successfully")
        except Exception as e:
            await db.rollback()
            print(f"An error occurred: {e}")
        finally:
            await db.close()


async def add_services():
    async for db in db_helper.session_getter():
        service1 = Service(name="Комплексная мойка", price=1000000, time=3600)
        service2 = Service(name="Полировка кузова", price=120000, time=4800)
        service3 = Service(name="Быстрая мойка", price=45000, time=1200)

        db.add(service1)
        db.add(service2)
        db.add(service3)

        try:
            await db.commit()
            print("Services added successfully")
        except Exception as e:
            await db.rollback()
            print(f"An error occurred: {e}")
        finally:
            await db.close()


async def main():
    await add_brands()
    await add_cars()
    await add_roles()
    await add_services()


# Запуск асинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())