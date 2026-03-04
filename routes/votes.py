from fastapi import APIRouter, Depends
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.votes import UserController
from dto.create import ResultCreate
from _config.db import getDb

router = APIRouter(prefix="/votes")

async def get_item_controller(db: AsyncSession = Depends(getDb)):
    return UserController(db)


@router.get("/")
async def list_votes(controller: UserController = Depends(get_item_controller)):
    return await controller.allPollingResult()

@router.get("/{id}")
async def local_govt_count(id:int, controller: UserController = Depends(get_item_controller)):
    return await controller.sumTotal(id)

@router.post("/new-result")
async def new_result(item: ResultCreate, controller: UserController = Depends(get_item_controller)):
    return await controller.storePollingRes(item.polling_unit_uniqueid, item.party_abbreviation, item.party_score, item.entered_by_user, item.date_entered, item.user_ip_address)