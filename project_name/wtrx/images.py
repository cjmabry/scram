from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    """
    Custom image model.

    Empty subclass of AbstractImage so future projects can add fields
    (alt text defaults, image credit, copyright, etc.) without migrating
    away from Wagtail's built-in Image — which would require rewriting all
    FK references and rebuilding the rendition cache.

    WAGTAILIMAGES_IMAGE_MODEL in settings/base.py points to this model.

    Extend this class to add project-specific image fields.
    """

    admin_form_fields = (
        "title",
        "file",
        "description",
        "collection",
        "tags",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
    )

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"

    @property
    def object_position_style(self):
        """
        Returns a full CSS object-position declaration derived from the focal point.
        Use in templates: style="{{ page.hero_image.object_position_style }}"
        Mirrors the convention of Wagtail's built-in background_position_style property.
        """
        if self.has_focal_point() and self.width and self.height:
            fp = self.get_focal_point()
            x = round(fp.centroid_x / self.width * 100)
            y = round(fp.centroid_y / self.height * 100)
            return f"object-position: {x}% {y}%;"
        return "object-position: center center;"


class CustomRendition(AbstractRendition):
    """Custom rendition for CustomImage."""

    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
