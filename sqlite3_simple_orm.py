import sqlite3


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != 'Model':
            table_name = attrs.get('__tablename__', name.lower())
            columns = {}
            for attr_name, attr_value in attrs.items():
                if isinstance(attr_value, Column):
                    columns[attr_name] = attr_value
            attrs['__table__'] = table_name
            attrs['__columns__'] = columns
        return super().__new__(cls, name, bases, attrs)


class Column:
    def __init__(self, column_type, primary_key=False):
        self.column_type = column_type
        self.primary_key = primary_key


class Model(metaclass=ModelMeta):
    _connection = sqlite3.connect('sqlite3.db')
    _cursor = _connection.cursor()

    @classmethod
    def create_table(cls):
        columns_def = []
        for col_name, col_obj in cls.__columns__.items():
            col_def = f"{col_name} {col_obj.column_type}"
            if col_obj.primary_key:
                col_def += " PRIMARY KEY"
            columns_def.append(col_def)
        columns_str = ", ".join(columns_def)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {cls.__table__} ({columns_str})"
        cls._cursor.execute(create_table_sql)
        cls._connection.commit()

    @classmethod
    def insert(cls, **kwargs):
        columns = ', '.join(kwargs.keys())
        values = ', '.join(['?' for _ in kwargs.values()])
        insert_sql = f"INSERT INTO {cls.__table__} ({columns}) VALUES ({values})"
        cls._cursor.execute(insert_sql, tuple(kwargs.values()))
        cls._connection.commit()
        return cls._cursor.lastrowid

    @classmethod
    def select_all(cls):
        select_sql = f"SELECT * FROM {cls.__table__}"
        cls._cursor.execute(select_sql)
        rows = cls._cursor.fetchall()
        result = []
        column_names = [desc[0] for desc in cls._cursor.description]
        for row in rows:
            obj = cls()
            for col_name, value in zip(column_names, row):
                setattr(obj, col_name, value)
            result.append(obj)
        return result

    @classmethod
    def select_by_id(cls, id):
        select_sql = f"SELECT * FROM {cls.__table__} WHERE id = ?"
        cls._cursor.execute(select_sql, (id,))
        row = cls._cursor.fetchone()
        if row:
            obj = cls()
            column_names = [desc[0] for desc in cls._cursor.description]
            for col_name, value in zip(column_names, row):
                setattr(obj, col_name, value)
            return obj
        return None

    @classmethod
    def update(cls, id, **kwargs):
        set_clause = ', '.join([f"{col} = ?" for col in kwargs.keys()])
        values = tuple(kwargs.values()) + (id,)
        update_sql = f"UPDATE {cls.__table__} SET {set_clause} WHERE id = ?"
        cls._cursor.execute(update_sql, values)
        cls._connection.commit()
        return cls._cursor.rowcount

    @classmethod
    def close_connection(cls):
        cls._connection.close()


# 示例使用
class User(Model):
    __tablename__ = 'users'
    id = Column('INTEGER', primary_key=True)
    name = Column('TEXT')
    age = Column('INTEGER')


if __name__ == "__main__":
    # 创建表
    User.create_table()

    # 插入数据
    user_id = User.insert(name='John', age=30)
    print(f"Inserted user with ID: {user_id}")

    # 查询所有数据
    users = User.select_all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

    # 关闭数据库连接
    User.close_connection()