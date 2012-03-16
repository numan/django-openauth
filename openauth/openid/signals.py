from django.contrib.auth.hashers import make_password

import time
import random
import utils


def generate_hash(sender, instance, **kwargs):
    if instance.pk is None and instance.identifier:
        instance.timestamp = int(time.time())
        instance.salt = make_password(str(random.random()), \
            salt=str(random.random()), hasher='sha1').split("$")[-1][:10]

def make_association(sender, instance, **kwargs):
    if not instance.server_url or not instance.assoc_type:
        raise Exception('association.server_url or association.assoc_type is None')

    response = utils.generate(instance.server_url, assoc_type=instance.assoc_type)
    instance.handle = response['handle']
    instance.secret = response['secret']
    instance.lifetime = response['lifetime']
    instance.issued = int(time.time())
