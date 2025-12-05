from typing import List

from recipe_manager.recipe_manager_lv1 import RecipeManager, Recipe


class RecipeManagerV2(RecipeManager):
    def __init__(self):
        super().__init__()
        self.sorted_keys = self.recipe_id_mapping.keys()

    def search_by_name(self, keyword: str) -> List[Recipe]:
        kw = keyword.lower()
        matched = [
            self.recipe_id_mapping[rid]
            for lower_name, rid in self.recipe_name_mapping.items()
            if kw in lower_name
        ]
        RecipeManagerV2._sort(matched)
        return matched

    def scan(self) -> List[Recipe]:
        """
        Return all recipes sorted by:
            1) number of ingredients (ascending)
            2) recipe id (ascending)
        """
        rcps = list(self.recipe_id_mapping.values())
        RecipeManagerV2._sort(rcps)
        return rcps

    @staticmethod
    def _sort(recipes: List[Recipe]) -> None:
        recipes.sort(key=lambda rcp: (len(rcp.ingredients), rcp.rid))


def main() -> None:
    mgr = RecipeManagerV2()
    mgr.add_recipe(1, 'Mapo Tofu', ['spice', 'tofu'])
    mgr.add_recipe(2, 'Hongshao tofu', ['tofu', 'pork', 'egg'])
    mgr.add_recipe(3, 'Jingjiang Rousi', ['pork'])
    mgr.add_recipe(4, 'Tofubao', ['tofu', 'soup'])
    print(mgr.scan())
    print(mgr.search_by_name('tofu'))


if __name__ == "__main__":
    main()