import uuid
from http import HTTPStatus

import pydub
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SETTINGS
from models.models import HTTPErrorDetails
from db.database import get_db
from services.files import allowed_file, save_mp3file_path, check_mp3file_exist_n_owner, get_audiofile_entry
from services.auth import get_user_by_uuid, get_user_by_token

router = APIRouter()


@router.get('/record')
async def download_record(id: uuid.UUID = None, user: uuid.UUID = None, db: AsyncSession = Depends(get_db)):
    """
    Redirect to absolute URL for download mp3 with provided data (nginx serve media). If you want to return FileResponse
    in this endpoint - please uncomment FileResponse
    :param id: uuid of AudioFiles entry
    :param user: uuid of an owner this AudioFiles entry
    :param db:
    :return: Redirect
    """
    if not await check_mp3file_exist_n_owner(audiofile_uuid=id, user_uuid=user, db=db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='This audiofile doesnt exists or wrong owner provided')
    else:
        path = await get_audiofile_entry(audiofile_uuid=id, db=db)
        # return FileResponse(path=f'{SETTINGS.BASE_DIR}/{path.mp3_file}', media_type='application/octet-stream',
        #                     filename=path.mp3_file.rsplit('/', 2)[2])
        return RedirectResponse(f'''{SETTINGS.PROJECT_URL}/api/v1/media/mp3/{path.mp3_file.rsplit('/', 2)[2]}''',
                                status_code=HTTPStatus.SEE_OTHER)


@router.post('/upload')
async def upload_file(user_uuid: uuid.UUID, user_token: uuid.UUID, file: UploadFile = File(),
                      db: AsyncSession = Depends(get_db)) -> str:
    """
    Function take user id, user token, wav file. Checking provided file for expected format, checking users data,
    convert wav file to mp3, store it, generate link for download file.
    If you want to Redirect users browser to download endpoint - please uncomment 'return RedirectResponse(...)'
    :param user_uuid: user unique id
    :param user_token: user unique token
    :param file: wav file
    :param db:
    :return: Url for download converted file
    """
    if not await get_user_by_uuid(user_uuid, db=db) or not await get_user_by_token(user_token, db=db):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPErrorDetails.UNAUTHORIZED.value)
    elif not allowed_file(file):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="File type not allowed")

    audiofile = pydub.AudioSegment.from_wav(file.file)
    audiofile_path_entry = await save_mp3file_path(filename=file.filename, user_uuid=user_uuid, db=db)
    audiofile.export(f'{SETTINGS.BASE_DIR}/{audiofile_path_entry.mp3_file}', format='mp3')
    await db.commit()

    # retrieve_abs_url_url = router.url_path_for('get_absolute_url', id=str(audiofile_path_entry.uuid),
    #                                            user=str(user_uuid))
    # это должно было работать, но в APIRouter().url_path_for() при обработке почему-то ожидаемые параметры
    # эндпоинта /record не забираются должным образом

    # return RedirectResponse(
    #     url=f'{SETTINGS.PROJECT_URL}/api/v1/files/record?id={str(audiofile_path_entry.uuid)}&user={str(user_uuid)}',
    #     status_code=HTTPStatus.SEE_OTHER)

    return f'{SETTINGS.PROJECT_URL}/api/v1/files/record?id={str(audiofile_path_entry.uuid)}&user={str(user_uuid)}'
