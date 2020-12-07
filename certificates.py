import uuid
import configparser
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Union

from marshmallow import Schema, fields, post_load


class Certificate():
    def __init__(self,
                 name: str,
                 owner_name: str,
                 creation_date: datetime = datetime.now(),
                 expiration: Optional[int] = None,
                 id: str = str(uuid.uuid4)):
        """
        Класс сертификата.

        Parameters
        ----------
        name : str
            Название курса
        owner_name : str
            Имя владельца
        creation_date : datetime
            Время создания
        expiration_date : Optional[int]
            Срок годности сертификата в днях
        id : str
            Id сертификата
        """

        self.id = id
        self.name = name
        self.owner_name = owner_name
        self.creation_date = creation_date
        self.expiration = expiration
        self.active = True

    @property
    def days_before_expiration(self) -> string:
        days = (datetime.now() - (self.creation_date + timedelta(self.expiration))).days
        if days % 10 == 1 and days % 100 != 11:
            russian_day_plural = 'день'
        elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
            russian_day_plural = 'дня'
        else:
            russian_day_plural = 'дней'
        msg_for_user = (
            'Бессрочый' if expiration is None
            else (
                f'До конца {days} {russian_day_plural}.' if days > 0 else f'Истек {russian_day_plural} назад.'
            )
        )
        return msg_for_user

    @property
    def is_expired(self) -> bool:
        """Возвращает False, если срок сертификата истек."""
        return (
            (self.creation_date + timedelta(self.expiration)) < datetime.now()
            if self.expiration is not None else True
        )

    @property
    def certificate_info(self) -> str:
        """Возвращает строку для пользователя."""
        return (
            f'Название курса: {self.name}\nИмя владельца: {self.owner_name}'
            f'Дата создания: {self.creation_date}\nСрок годности: {self.days_before_expiration}'

class CertificateSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    owner_name = fields.Str()
    creation_date = fields.DateTime()
    expiration = fields.Int()
    active = field.Boolean()

    @post_load
    def make_certificate(self, data, **kwargs):
        return Certificate(**data)


config = configparser.ConfigParser()
config.read('config.ini')
path = Path(config['paths']['certificates'])
if not path.exists():
    path.mkdir(parents=True, exist_ok=False)


def get_all_certificates():
    """
    Возвращает все сертификаты
    """
    certificates_path = path / config['paths']['certificates_json']
    with(certificates_path.open('r+')) as outfile:
        all_certificates = CertificateSchema(many=True).loads(outfile.read())
    return all_certificates


def set_all_certificates(all_certificates):
    """
    Устанавливает все сертификаты по значению value

    Parameters
    ----------
    value :
        Список пользователей
    """
    certificates_path = path / config['paths']['certificates_json']
    with(certificates_path.open('w+')) as outfile:
        outfile.write(CertificateSchema(many=True).dumps(all_certificates))
