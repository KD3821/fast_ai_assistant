import copy
import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from src.data.db_loader import DBLoader
from src.data.itinerary_builder import ItineraryBuilder
from src.settings import fast_ai_settings
from src.utils import create_json_file

router = APIRouter(prefix="/storage", tags=["Data Storage"])


@router.post("/cruises-upload")
async def upload_cruises(
    background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)
):
    missing_files = {"ships.json", "destinations.json"}

    file_exc = HTTPException(
        status_code=400,
        detail="Please upload two files: 'ships.json' and 'destinations.json'",
    )
    if len(files) != 2:
        raise file_exc

    for file in files:
        if not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=400,
                detail=f"file: {file.filename} \nFile type not supported. Only JSON files are accepted.",
            )
        if file.filename not in ("ships.json", "destinations.json"):
            raise HTTPException(
                status_code=400,
                detail=f"file: {file.filename} \nWrong filename. Should be 'ships.json' or 'destinations.json'",
            )
        try:
            missing_files.remove(file.filename)
        except KeyError:
            raise file_exc

    if missing_files:
        raise file_exc

    for file in files:
        if file.filename == "ships.json":
            ships_data = json.load(file.file)
        elif file.filename == "destinations.json":
            destinations_data = json.load(file.file)

    builder = ItineraryBuilder(
        ships=ships_data.get("ships"),
        destinations=destinations_data.get("destinations"),
    )

    itinerary = builder.build(7)  # define number of cruises

    itinerary_data = copy.deepcopy(itinerary)
    ships_file_data = copy.deepcopy(ships_data)
    destinations_file_data = copy.deepcopy(destinations_data)

    db_loader = DBLoader(db_name=fast_ai_settings.db_name)

    await db_loader.upload_data(itinerary, "itineraries")

    await db_loader.upload_data(destinations_data.get("destinations"), "destinations")

    await db_loader.upload_data(ships_data.get("ships"), "ships")  # try

    ships_collection = await db_loader.load_vectors(ships_data.get("ships"), "ships")
    ships_collection.create_index([("name", "text")])

    itinerary_collection = await db_loader.load_vectors(itinerary_data, "itineraries")
    itinerary_collection.create_index([("itinerary", "text")])

    date = datetime.utcnow()
    file_date_str = date.strftime("%H_%M_%S(%d-%m-%Y)")

    background_tasks.add_task(
        create_json_file,
        file_data=ships_file_data,
        file_name=f"ships_{file_date_str}.json",
        dir_name="cruises",
    )
    background_tasks.add_task(
        create_json_file,
        file_data=destinations_file_data,
        file_name=f"destinations_{file_date_str}.json",
        dir_name="cruises",
    )

    return {"itineraries:": itinerary_data}
