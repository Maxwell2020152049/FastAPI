"""
数据库相关配置
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_PASSWORD = "hwf333888"
"""
Mysql密码
"""

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{MYSQL_PASSWORD}@127.0.0.1/wanfeng"
"""
Mysql路由
"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)
"""
使用上述路由创建MySQL引擎
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
创建MySQL会话: 
绑定引擎;
关闭自动提交、自动刷新; 
"""
