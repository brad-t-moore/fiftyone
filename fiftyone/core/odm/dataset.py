"""
Documents that track datasets and their sample schemas in the database.

| Copyright 2017-2021, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from mongoengine import (
    BooleanField,
    EmbeddedDocumentListField,
    ListField,
    StringField,
)

import eta.core.utils as etau

from .document import Document, EmbeddedDocument
from .fields import DictField, TargetsField


class SampleFieldDocument(EmbeddedDocument):
    """Backing document for sample fields."""

    name = StringField()
    ftype = StringField()
    subfield = StringField(null=True)
    embedded_doc_type = StringField(null=True)

    @classmethod
    def from_field(cls, field):
        """Creates a :class:`SampleFieldDocument` from a MongoEngine field.

        Args:
            field: a :class:``fiftyone.core.fields.Field`` instance

        Returns:
            a :class:`SampleFieldDocument`
        """
        return cls(
            name=field.name,
            ftype=etau.get_class_name(field),
            subfield=cls._get_attr_repr(field, "field"),
            embedded_doc_type=cls._get_attr_repr(field, "document_type"),
        )

    @classmethod
    def list_from_field_schema(cls, d):
        """Creates a list of :class:`SampleFieldDocument` objects from a field
        schema.

        Args:
             d: a dict generated by
                :func:`fiftyone.core.dataset.Dataset.get_field_schema`

        Returns:
             a list of :class:`SampleFieldDocument` objects
        """
        return [
            cls.from_field(field) for field in d.values() if field.name != "id"
        ]

    def matches_field(self, field):
        """Determines whether this sample field matches the given field.

        Args:
            field: a :class:``fiftyone.core.fields.Field`` instance

        Returns:
            True/False
        """
        if self.name != field.name:
            return False

        if self.ftype != etau.get_class_name(field):
            return False

        if self.subfield and self.subfield != etau.get_class_name(field.field):
            return False

        if (
            self.embedded_doc_type
            and self.embedded_doc_type
            != etau.get_class_name(field.document_type)
        ):
            return False

        return True

    @staticmethod
    def _get_attr_repr(field, attr_name):
        attr = getattr(field, attr_name, None)
        return etau.get_class_name(attr) if attr else None


class DatasetDocument(Document):
    """Backing document for datasets."""

    meta = {"collection": "datasets"}

    media_type = StringField()
    name = StringField(unique=True, required=True)
    sample_collection_name = StringField(unique=True, required=True)
    persistent = BooleanField(default=False)
    info = DictField(default=dict)
    sample_fields = EmbeddedDocumentListField(
        document_type=SampleFieldDocument
    )
    default_targets = TargetsField(null=True)
    field_targets = DictField(default=dict, field=TargetsField(default=dict))
    frame_fields = EmbeddedDocumentListField(document_type=SampleFieldDocument)
    version = StringField(required=True, null=True)
