import json
import logging
from django.conf import settings

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save

logger = logging.getLogger('django')

class TaxonomyTerms(models.Model):
    taxonomy_id = models.CharField(max_length=255, unique=True)
    terms_json = models.TextField()

@receiver(post_save, sender=TaxonomyTerms)
def update_taxonomy_terms_on_blobstore(sender, instance, **kwargs):
    try:
        data = json.loads(instance.terms_json)
        terms_with_vocab = get_terms_from_terms_json(data)
        vocabs = get_vocabs_from_terms_json(data)
        content = dict()
        content['vocabs'] = vocabs
        content['terms'] = terms_with_vocab

        blobPath = f'taxonomy/{instance.taxonomy_id}.json'
        blobFile = ContentFile (to_json (content).encode ())
        default_storage.save (blobPath, blobFile)
        logger.info('Successfully wrote taxonomy json to BlobStore %s', blobPath)

    except Exception as e:
        logger.info('Could not build taxonomy json and send to BlobStore %s', e)
        raise

def get_terms_from_terms_json(data):
    terms = dict()
    level = 1
    for obj in data:
        if obj.get('type') == 'vocabulary':
            vocab_code = obj.get('code')
            children = obj.get('children', None)
            if children:
                child_terms = get_terms_from_children(children, vocab_code, '', level)
                terms.update(child_terms)
    return terms

def get_terms_from_children(children, vocab_code, index_path, level):
    terms = dict()
    for obj in children:
        if obj.get('type') == 'term':
            index_path_for_level = obj.get('code') if index_path == '' else "%s|%s" % (index_path, obj.get('code'))
            terms[obj.get('code')] = { "label": obj.get('label'), "vocabCode": vocab_code, "indexPath": index_path_for_level, "level": level }
            children = obj.get('children', None)
            if children:
                next_level = level + 1
                child_terms = get_terms_from_children(children, vocab_code, index_path_for_level, next_level)
                terms.update(child_terms)
    return terms

def get_vocabs_from_terms_json(data):
    vocabs = dict()
    for obj in data:
        if obj.get('type') == 'vocabulary':
            vocab_code = obj.get('code')
            vocab_label = obj.get('label')
            vocabs[vocab_code] = vocab_label
    return vocabs

def to_json(data):
    return json.dumps(data)

class TaxonomyMixin(models.Model):
    taxonomy_json = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

class PageTaxonomyPermissionsMixin(models.Model):
    global_permission = models.CharField(max_length=100, null=True, blank=True, default='public')
    inherit_permission = models.CharField(max_length=100, null=True, blank=True)
    permissions_json = models.TextField(null=True, blank=True)
    permissions_json_formatted = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

class ModelTaxonomyPermissionsMixin(models.Model):
    permissions_json = models.TextField(null=True, blank=True)
    permissions_json_formatted = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

# @receiver(pre_save, sender=PageTaxonomyPermissionsMixin)
def format_permissions_json(sender, instance, **kwargs):
    permissions_json_formatted = {}
    for group_key, groups in (json.loads(instance.permissions_json)).items():
        permissions_json_formatted[group_key] = []
        for action_key, vocs in groups.items():
            permissions_json_formatted[group_key].extend(['{0}.{1}'.format(action_key, voc) for voc in vocs])
    instance.permissions_json_formatted = permissions_json_formatted
    return instance
