import time
import random
from celery import group

from project import celery
from project.models import Status


@celery.task
def add(x, y):
    print(f"Inside ADD Function: {x} + {y} = {x+y}")
    return x + y

@celery.task
def tsum(numbers):
    print(f"Inside TSUM Function: sum({numbers}) = {sum(numbers)}")
    return sum(numbers)

@celery.task(bind=True)
def run_celery_group_task_example(self, i, verb, adjective, noun, message, total):
    if not message or random.random() < 0.25:
        message = '{0} {1} {2}...'.format(random.choice(verb),
                                            random.choice(adjective),
                                            random.choice(noun))

    Status(message=f"Group task: {message}", state=i).save()
    # celery receives task updates
    self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': total,
                            'status': message})
    time.sleep(1)


@celery.task(bind=True)
def long_task(self, group_task):
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
    message = ""
    total = random.randint(10, 50)

    if group_task:
        result = group(
            run_celery_group_task_example.s(i, verb, adjective, noun, message, total)
            for i in range(total)
        ).apply_async()
        while not result.ready():
            time.sleep(1)
    else:

        for i in range(total):
            if not message or random.random() < 0.25:
                message = "{0} {1} {2}...".format(
                    random.choice(verb), random.choice(adjective), random.choice(noun)
                )

            Status(message=message, state=i).save()
            # celery receives task updates
            self.update_state(
                state="PROGRESS", meta={"current": i, "total": total, "status": message}
            )
            time.sleep(1)

    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}
