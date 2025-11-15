import os
import logging
from typing import Dict, Optional
from threading import RLock
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class MysqlSettings:
    """MySQL 配置设置"""
    
    def __init__(self):
        self.host: str = ""
        self.port: str = ""
        self.user: str = ""
        self.password: str = ""


class TenantDBManager:
    """负责基于 RobotCode 缓存和创建不同的数据库连接"""
    
    def __init__(self):
        self._lock = RLock()
        self._tenants: Dict[str, sessionmaker] = {}
    
    def get_session_maker(self, robot_code: str) -> Optional[sessionmaker]:
        """获取指定 RobotCode 对应的 SessionMaker（带缓存）"""
        if not robot_code:
            raise ValueError("robotCode 为空")
        
        # 读缓存
        with self._lock:
            if robot_code in self._tenants:
                return self._tenants[robot_code]
        
        # 双重检查加锁创建
        with self._lock:
            if robot_code in self._tenants:
                return self._tenants[robot_code]
            
            dsn = self._build_dsn_for_robot(robot_code)
            try:
                engine = create_engine(
                    dsn,
                    poolclass=pool.QueuePool,
                    pool_size=10,
                    max_overflow=40,
                    pool_recycle=3600,  # 60分钟
                    pool_pre_ping=True,
                    echo=False
                )
                
                # 测试连接
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                
                session_maker = sessionmaker(bind=engine)
                self._tenants[robot_code] = session_maker
                return session_maker
                
            except SQLAlchemyError as e:
                logger.error(f"打开数据库失败({robot_code}): {e}")
                raise RuntimeError(f"打开数据库失败({robot_code}): {e}")
    
    def _build_dsn_for_robot(self, robot_code: str) -> str:
        """构建指定 RobotCode 的数据库 DSN"""
        return (
            f"mysql+pymysql://{mysql_settings.user}:{mysql_settings.password}"
            f"@{mysql_settings.host}:{mysql_settings.port}/{robot_code}"
            f"?charset=utf8mb4"
        )


# 全局变量
mcp_server_port: int = 0
mysql_settings = MysqlSettings()
tenant_db_manager = TenantDBManager()


def load_config() -> None:
    """加载配置"""
    _load_env_config()


def _load_env_config() -> None:
    """从环境变量加载配置"""
    global mcp_server_port
    
    # 本地开发模式
    is_dev_mode = os.getenv("GO_ENV", "").lower() == "dev"
    if is_dev_mode:
        if not load_dotenv():
            logger.warning("加载本地环境变量失败，请检查是否存在 .env 文件")
    
    # 加载端口配置
    port_str = os.getenv("MCP_SERVER_PORT")
    if not port_str:
        logger.error("环境变量 [MCP_SERVER_PORT] 未配置")
        raise ValueError("环境变量 [MCP_SERVER_PORT] 未配置")
    
    try:
        port = int(port_str)
    except ValueError:
        logger.error("环境变量 [MCP_SERVER_PORT] 必须是整数")
        raise ValueError("环境变量 [MCP_SERVER_PORT] 必须是整数")
    
    if port == 0:
        port = 9000
    
    if port < 1 or port > 65535:
        logger.error("MCPServerPort 必须在 1 到 65535 之间")
        raise ValueError("MCPServerPort 必须在 1 到 65535 之间")
    
    mcp_server_port = port
    
    # 加载 MySQL 配置
    mysql_settings.host = os.getenv("MYSQL_HOST", "")
    mysql_settings.port = os.getenv("MYSQL_PORT", "")
    mysql_settings.user = os.getenv("MYSQL_USER", "")
    mysql_settings.password = os.getenv("MYSQL_PASSWORD", "")


def get_db_by_robot_code(robot_code: str) -> Session:
    """获取指定 RobotCode 对应的数据库会话（带缓存）"""
    session_maker = tenant_db_manager.get_session_maker(robot_code)
    if session_maker is None:
        raise RuntimeError(f"无法获取 {robot_code} 的数据库会话")
    return session_maker()
