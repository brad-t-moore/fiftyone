"""
Evaluation documents.

| Copyright 2017-2021, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from mongoengine import DictField, ListField, StringField

from .document import EmbeddedDocument


class EvaluationDocument(EmbeddedDocument):
    """Description of an evaluation result."""

    name = StringField()
    gt_field = StringField()
    pred_field = StringField()
    config = DictField()
    view = ListField(DictField())
