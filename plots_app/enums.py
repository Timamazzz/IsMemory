from enum import Enum


class CemeteryPlotStatusEnum(Enum):
    FREE = 'Свободен'
    OCCUPIED = 'Занят'
    INVENTORY = 'Инвентаризация'


class CemeteryPlotTypeEnum(Enum):
    BURIAL = 'Захоронение'
    VACANT = 'Свободное назначение'