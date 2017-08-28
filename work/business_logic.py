from work.models import Work
from .tasks import create_work as create_work_async

import logging

logger = logging.getLogger(__name__)

def create_work_and_enqueue(worktype, customer , address, time, description, asap):
    work = Work(worktype = worktype, customer = customer, 
                address = address, time = time, 
                description = description,
                asap = asap)
    work.save()
    logger.info('work created for customer ' + customer.user.username + ', work id: ' + str(work.id))
    try:
        create_work_async.delay(work.id)
        logger.info('succesfully created work for customer ' + customer.user.username)
        return work
    except:
        logger.error('queue not found, trying to enqueue work id: ' + str(work.id))
        return work
