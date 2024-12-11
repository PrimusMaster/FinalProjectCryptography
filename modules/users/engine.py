from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

# Configuración de la base de datos SQLite (archivo local)
DATABASE_URL = "sqlite:///Users.db"
engine = create_engine(DATABASE_URL)

# Base de SQLAlchemy para definir clases de modelo
Base = declarative_base()

# Definición de la tabla Usuario
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    area = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.name}',contraseña = {self.password} correo='{self.mail}', edad={self.age}, area={self.area})>"

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')

    def create_user(self, name, password, mail, area, age):
        # Crete table
        Base.metadata.create_all(engine)

        #Hashing password
        hashed_password = self.hash_password(password)

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        #Add a new user
        new_user = User(name=name,password=hashed_password, mail=mail, area=area, age=age)
        session.add(new_user)
        session.commit()
        print("Usuario creado con exito")
        session.close()

    def view_users(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        usuarios = session.query(User).all()
        for i in usuarios:
            print(i)
        session.close()

    def update_user(self, user_id, **kwargs):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):  #if feature exist
                    setattr(user, key, value)
            session.commit()
            print(f"Usuario con id={user_id} actualizado con éxito.")
        else:
            print(f"No se encontró el usuario con id={user_id}.")
        session.close()

    def delete_user(self,user_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"Usuario con id={user_id} eliminado con éxito.")
        else:
            print(f"No se encontró el usuario con id={user_id}.")
        session.close()

