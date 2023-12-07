from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import UploadJob


@registry.register_document
class DocumentJob(Document):
    class Index:
        name = 'main'
        search = {'number_of_shards': 1, 'number_of_replicas': 0}

    # Autocompletion
    company_name = fields.TextField(
        attr='company_name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    job_title = fields.TextField(
        attr='job_title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    experience = fields.TextField(
        attr='experience',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })

    class Django:
        model = UploadJob
