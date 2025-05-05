from uuid import UUID

from diary.application.interfaces import TimeGenerator, TXManager, UserReader, UserWriter, UUIDGenerator
from diary.domain.models import User
from .dto import NewUserDTO, UpdateUserDTO
from .exceptions import EmailAlreadyExistsError, UserNotFoundError


class GetUserInteractor:
    def __init__(self, user_reader: UserReader) -> None:
        self._user_reader = user_reader

    async def get(self, user_id: UUID) -> User | None:
        return await self._user_reader.get_by_id(user_id)


class CreateUserInteractor:
    def __init__(
        self,
        user_reader: UserReader,
        user_writer: UserWriter,
        uuid_generator: UUIDGenerator,
        time_generator: TimeGenerator,
        tx: TXManager,
    ) -> None:
        self._user_reader = user_reader
        self._user_writer = user_writer
        self._uuid_generator = uuid_generator
        self._time_generator = time_generator
        self._tx = tx

    async def create(self, user: NewUserDTO) -> User:
        is_email_exists = await self._user_reader.email_exists(user.email)
        if is_email_exists:
            raise EmailAlreadyExistsError(email=user.email)

        now = self._time_generator()
        new_id = self._uuid_generator()
        new_user = User(
            id=new_id,
            name=user.name,
            email=user.email,
            timezone=user.timezone,
            birthday=user.birthday,
            created_at=now,
            updated_at=now,
        )

        await self._user_writer.save(new_user)
        await self._tx.commit()
        return new_user


class UpdateUserInteractor:
    def __init__(
        self,
        user_reader: UserReader,
        user_writer: UserWriter,
        time_generator: TimeGenerator,
        tx: TXManager,
    ) -> None:
        self._user_reader = user_reader
        self._user_writer = user_writer
        self._time_generator = time_generator
        self._tx = tx

    async def update(self, user: UpdateUserDTO) -> User:
        exist_user = await self._user_reader.get_by_id(user.id)
        if exist_user is None:
            raise UserNotFoundError(user_id=user.id)

        if exist_user.email != user.email:
            is_email_exists = await self._user_reader.email_exists(user.email)
            if is_email_exists:
                raise EmailAlreadyExistsError(email=user.email)

        now = self._time_generator()
        updated_user = User(
            id=exist_user.id,
            name=user.name,
            email=user.email,
            timezone=user.timezone,
            birthday=user.birthday,
            created_at=exist_user.created_at,
            updated_at=now,
        )

        await self._user_writer.save(updated_user)
        await self._tx.commit()
        return updated_user
