from .tasks import update_product_search_vector
from django_lifecycle import AFTER_SAVE, LifecycleModelMixin, hook
from django_lifecycle.conditions import WhenFieldHasChanged


class ProductMixin(LifecycleModelMixin):
    @hook(
        AFTER_SAVE,
        condition=(
            WhenFieldHasChanged("name_en", True)
            | WhenFieldHasChanged("name_ar", True)
            | WhenFieldHasChanged("description_en", True)
            | WhenFieldHasChanged("description_ar", True)
        ),
    )
    def update_search_vector_async(self):
        update_product_search_vector.delay(self.id)
