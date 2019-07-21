
from app.models import Video

import uuid

print(Video.get_base_columns_str())

# for i in range(13):
# 	print(uuid.uuid1())
video = Video()
print(video.title, video.id, video.__tablename__)


class Person:

	def __init__(self, *args, **kwargs):
		# print(type(kwargs), kwargs)
		self.name = kwargs["name"]
		self.age = kwargs["age"]
		self.gender = kwargs["gender"]
		# for key, value in kwargs.items():
		# 	setattr(self, key, value)

	def __repr__(self):
		return "<Person> name: " + self.name + ", age: " + str(self.age) + ", gender: " + self.gender


person = Person(name="Flouis", age=25, gender="M")
print(person.name)
# print(person["name"]) # TypeError: 'Person' object is not subscriptable

my_dict = {"a": 123, "b": 456, "c": 789}
print(my_dict["a"])
# print(my_dict.a) # AttributeError: 'dict' object has no attribute 'a'

# from werkzeug.security import generate_password_hash
# print(generate_password_hash("123456"))
