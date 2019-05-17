# -*- coding: utf-8 -*-


class UnsupportedDBTypeError(Exception):
    """不支持的数据源类型."""

    def __str__(self):
        return repr('不支持的数据源类型!')


class DatasourceConfigError(Exception):
    """数据源配置参数错误."""

    def __str__(self):
        return repr('数据源配置参数错误!')


class DrillDBConfig():

    db_type = None
    config_name = ["ip", "port", "db_name", "username", "password"]

    def drill_config(self, config):
        """
        实现每种数据库Drill配置生成器。
        """
        pass

    def check_config(self, config):
        """
        检测某些属性是否在config实例中。
        """
        if self.config_name is not None:
            for attr_name in self.config_name:
                if attr_name not in config:
                    return False
        return True


class MySQLDrillDBConfig(DrillDBConfig):

    db_type = "mysql"

    def drill_config(self, config):
        """
        {
            "ip": "192.168.7.250",
            "port": "3306",
            "db_name": "main",
            "username": "root",
            "password": "root"
        }
        {
            "type": "jdbc",
            "driver": "com.mysql.jdbc.Driver",
            "url": "jdbc:mysql://localhost:3306",
            "username": "root",
            "password": "mypassword",
            "enabled": true
        }
        """
        return {
            "type": "jdbc",
            "driver": "com.mysql.jdbc.Driver",
            "url": "jdbc:mysql://{}:{}/{}".format(config['ip'], config['port'], config['db_name']),
            "username": config['username'],
            "password": config['password'],
            "caseInsensitiveTableNames": False,
            "enabled": True
        }


class OracleDrillDBConfig(DrillDBConfig):

    db_type = "oracle"

    def drill_config(self, config):
        """
        {
            "ip": "192.168.7.250",
            "port": "3306",
            "db_name": "main",
            "username": "root",
            "password": "root"
        }
        {
            type: "jdbc",
            enabled: true,
            driver: "oracle.jdbc.OracleDriver",
            url:"jdbc:oracle:thin:user/password@1.2.3.4:1521/ORCL"
        }
        """
        return {
            "type": "jdbc",
            "enabled": True,
            "driver": "oracle.jdbc.OracleDriver",
            "url": "jdbc:oracle:thin:{}/{}@{}:{}/{}".format(config['username'],
                                                            config['password'],
                                                            config['ip'],
                                                            config['port'],
                                                            config['db_name']),
        }


class SQLServerDrillDBConfig(DrillDBConfig):

    db_type = "sqlserver"

    def drill_config(self, config):
        """
        {
            "ip": "192.168.7.250",
            "port": "3306",
            "db_name": "main",
            "username": "root",
            "password": "root"
        }
        {
            type: "jdbc",
            enabled: true,
            driver: "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            url:"jdbc:sqlserver://1.2.3.4:1433;databaseName=mydatabase",
            username:"user",
            password:"password"
        }
        """
        return {
            "type": "jdbc",
            "enabled": True,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "url": "jdbc:sqlserver://{}:{};databaseName={}".format(config['ip'], config['port'], config['db_name']),
            "username": config['username'],
            "password": config['password'],
        }


class PostgresqlDrillDBConfig(DrillDBConfig):

    db_type = "postgresql"

    def drill_config(self, config):
        """
        {
            "ip": "192.168.7.250",
            "port": "3306",
            "db_name": "main",
            "username": "root",
            "password": "root"
        }
        {
            type: "jdbc",
            enabled: true,
            driver: "org.postgresql.Driver",
            url: "jdbc:postgresql://1.2.3.4/mydatabase",
            username: "user",
            password: "password"
        }
        """
        return {
            "type": "jdbc",
            "enabled": True,
            "driver": "org.postgresql.Driver",
            "url": "jdbc:postgresql://{}:{}/{}".format(config['ip'], config['port'], config['db_name']),
            "username": config['username'],
            "password": config['password'],
        }


DrillConfig = {
    "mysql": MySQLDrillDBConfig(),
    "oracle": OracleDrillDBConfig(),
    "sqlserver": SQLServerDrillDBConfig(),
    "postgresql": PostgresqlDrillDBConfig()


}


def get_support_db_type():
    db_type = []
    for item in DrillConfig:
        db_type.append(item.db_type)
    return db_type


def get_support_drill_config(type_name):
    return DrillConfig.get(type_name.lower())
