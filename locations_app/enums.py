from enum import Enum


class CemeteryStatusEnum(Enum):
    OPENED = 'Открыто'
    CLOSED = 'Закрыто'


class CemeteryPlotStatusEnum(Enum):
    FREE = 'Свободен'
    OCCUPIED = 'Занят'
    INVENTORY = 'Инвентаризация'


class CemeteryPlotTypeEnum(Enum):
    BURIAL = 'Захоронение'
    VACANT = 'Свободное назначение'
