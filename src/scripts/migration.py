import motor.motor_asyncio


def main():
    url = "mongodb+srv://cluster0.9k0ry.mongodb.net/palza-market"
    # 
    db = motor.motor_asyncio.AsyncIOMotorClient(url)
    print(db)
    pass





if __name__ == "__main__":
    main()
