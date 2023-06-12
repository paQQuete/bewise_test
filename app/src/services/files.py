import uuid

import magic

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SETTINGS
from models.models import AudioFiles


def allowed_file(file: UploadFile, allowed_extensions: set = SETTINGS.ALLOWED_EXTENSIONS,
                 allowed_mimetypes: set = SETTINGS.ALLOWED_MIMETYPES) -> bool:
    """
    Check file extension and mimetype (with read 2048 kb of file)
    :param file: Starlet UploadFile instance
    :param allowed_extensions: expected file extensions
    :param allowed_mimetypes: expected file mimetype
    :return:
    """
    file_extension = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else ''
    mimetype = magic.from_buffer(file.file.read(2048), mime=True)
    return (file_extension in allowed_extensions) and (mimetype in allowed_mimetypes)


async def save_mp3file_path(filename: str, user_uuid: uuid.UUID, db: AsyncSession) -> AudioFiles:
    """
    Save record for new mp3 file, return created entity of AudioFiles model
    :param filename: full original filename with an extension
    :param user_uuid: owner of audiofile
    :param db:
    :return: Created AudioFiles entity
    """
    filename_wo_ext = filename.rsplit(".", 1)[0]
    new_entity_uuid = uuid.uuid4()
    new_filename = f'{SETTINGS.MP3_CONTENT_PATH}/{filename_wo_ext}_{new_entity_uuid}.mp3'
    db_audiofile = AudioFiles(user_uuid=user_uuid,
                              mp3_file=new_filename,
                              uuid=new_entity_uuid)
    db.add(db_audiofile)
    await db.flush()
    return db_audiofile


async def check_mp3file_exist_n_owner(audiofile_uuid: uuid.UUID, user_uuid: uuid.UUID,
                                      db: AsyncSession) -> AudioFiles | None:
    """
    Check if AudioFiles entry exists with provided data
    :param audiofile_uuid: uuid of stored audiofile entry
    :param user_uuid: uuid of an owner this entry
    :param db:
    :return: AudioFiles entry or None if doesn't exist
    """
    db_audiofile = await db.execute(
        select(AudioFiles).where(
            (AudioFiles.uuid == audiofile_uuid) & (AudioFiles.user_uuid == user_uuid)
        ))
    db_audiofile = db_audiofile.scalar()
    if db_audiofile:
        return db_audiofile
    else:
        return None


async def get_audiofile_entry(audiofile_uuid: uuid.UUID, db: AsyncSession) -> AudioFiles:
    """Get entry of AudioFiles model"""
    db_audiofile = await db.execute(select(AudioFiles).where(AudioFiles.uuid == audiofile_uuid))
    db_audiofile = db_audiofile.scalar()
    return db_audiofile
