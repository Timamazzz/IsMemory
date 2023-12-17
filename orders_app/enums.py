from enum import Enum


class OrderStatusEnum(Enum):
    CANCELLED = 'Отменен'
    AWAITING_PAYMENT = 'Ожидание оплаты'
    IN_QUEUE = 'В очереди'
    #ASSIGNING_EXECUTOR = 'Подбор исполнителя'
    WORK_IN_PROGRESS = 'Ведутся работы'
    COMPLETED = 'Завершено'
    CONFIRMED = 'Подтверждено'
    EXECUTED = 'Выполнено'
