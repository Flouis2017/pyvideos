
from app.models import Video

import uuid

print(Video.get_base_columns_str())

for i in range(13):
	print(uuid.uuid1())
