import os

from dotenv import load_dotenv
#ID категории: ID канала для создания комнат
custom_voice = {
    1193564053541486655: 1193588535450677468
}
role_for_new_member = 1194664356496015460
load_dotenv()
TOKEN = os.getenv("TOKEN")
