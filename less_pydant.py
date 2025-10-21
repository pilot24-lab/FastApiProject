from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()
data = {
    'email' : 'acdsf@mail.ru',
    'bio' : None,
    
    
}
data_age = {
    'email' : 'acdsf@mail.ru',
    'bio' : None,
    'age' : 25
}

class UserScheme(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=300)
    model_config = ConfigDict(extra='forbid')

users = []
@app.post('/users')
def add_user(user: UserScheme):
    users.append(user)
    return {'ok': True, 'user': user}

@app.get('/users')
def list_users() -> list[UserScheme]:
    return users


class UserAgeScheme(UserScheme):
    age: int = Field(ge=0, le=150)




