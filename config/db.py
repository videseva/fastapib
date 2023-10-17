from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://root:12345@mysql_host:3306/cloudtaller", echo=True)

meta = MetaData()

conn = engine.connect()