# -*- coding: utf-8 -*-
"""
# @Creation time: 2024/7/28 下午10:28
# @Author       : 郭军
# @Email        : 391350540@qq.com
# @FileName     : Database.py
# @Software     : PyCharm
# @Project      : Automated Testing
# @PRODUCT_NAME : PyCharm
# @PythonVersion: python 3.12
# @Version      : 
# @Description  : 
# @Update Time  : 
# @UpdateContent:  

"""
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session
from common.config import DB_CONNECTION_STRING
from sqlalchemy.exc import SQLAlchemyError
from common.logger import logger
from contextlib import contextmanager


class Database:  # 创建数据库引擎
    _engine = None
    _metadata = MetaData()

    def __init__(self, db_connection_string=DB_CONNECTION_STRING):
        self.db_connection_string = db_connection_string
        self.table = None
        if Database._engine is None:
            Database._engine = create_engine(db_connection_string)
            Database._metadata.reflect(Database._engine)

    # 增加一个类方法，用于获取数据库引擎
    @classmethod
    def get_engine(cls):
        return cls._engine

    def get_tables(self, table=None):
        self.table = table
        # 创建数据库引

        # 使用automap_base创建一个Base类，它会自动为所有表创建一个映射
        Base = automap_base(metadata=Database._metadata)
        # 使用prepare()方法，将数据库引擎与Base类关联
        Base.prepare(autoload_with=Database._engine)

        # 判断表是否存在
        if self.table not in Base.classes.keys():
            return False
        else:
            # 将映射的表名与类关联
            self.table = Base.classes[self.table]
            return self.table

    @contextmanager
    def get_session(self):
        # 创建session
        Session = scoped_session(sessionmaker(bind=Database._engine))
        session = Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"数据库操作失败: {str(e)}")
        finally:
            session.close()


if __name__ == '__main__':
    db = Database()
    tables = db.get_tables("vcloud_session")
    if tables:
        with db.get_session() as session:
            query = session.execute(text('select * from vcloud_session where id =1')).all()
            # query = session.query(tables).first()
            print(query)
    else:
        print("表不存在")
