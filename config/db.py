from sqlalchemy import create_engine, MetaData



engine = create_engine("mysql+pymysql://admin:12345@localhost:3306/cloudtaller",echo=True)


meta = MetaData()

conn = engine.connect()