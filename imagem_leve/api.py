from ninja import NinjaAPI
from optimizer.api import optimizer_router

api = NinjaAPI()
api.add_router('/', optimizer_router)