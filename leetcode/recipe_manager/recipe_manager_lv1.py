import time
from dataclasses import field, dataclass
from typing import List, Dict


@dataclass
class Recipe:
    rid: int
    name: str
    ingredients: List[str]
    updated_at: int = field(default_factory=lambda: int(time.time()))

class RecipeManager:
    def __init__(self):
        self.recipe_id_mapping: Dict[int, Recipe] = {}
        self.recipe_name_mapping: Dict[str, int] = {}

    def add_recipe(self, rid: int, name: str, ingredients: List[str]) -> bool:
        if self._is_name_conflict(name):
            return False
        if rid in self.recipe_id_mapping:
            return False
        # Add
        rcp = Recipe(rid, name, ingredients)
        self.recipe_id_mapping[rid] = rcp
        self.recipe_name_mapping[RecipeManager._normalize_name(name)] = rid
        return True

    def get_recipe(self, rid: int) -> Recipe | None:
        if rid in self.recipe_id_mapping:
            return self.recipe_id_mapping[rid]
        return None

    def update_recipe(self, rid: int, new_name: str, new_ingredients: List[str]) -> bool:
        if rid not in self.recipe_id_mapping:
            return False
        cur_rcp = self.recipe_id_mapping[rid]
        # Check name conflict
        del self.recipe_name_mapping[RecipeManager._normalize_name(cur_rcp.name)]
        if self._is_name_conflict(new_name):
            self.recipe_name_mapping[RecipeManager._normalize_name(cur_rcp.name)] = rid
            return False
        # Update
        new_rcp = Recipe(rid, new_name, new_ingredients)
        self.recipe_id_mapping[rid] = new_rcp
        self.recipe_name_mapping[RecipeManager._normalize_name(new_name)] = rid
        return True

    def delete_recipe(self, rid: int) -> bool:
        if rid not in self.recipe_id_mapping:
            return False
        # Delete
        del_rcp = self.recipe_id_mapping.pop(rid)
        del self.recipe_name_mapping[RecipeManager._normalize_name(del_rcp.name)]
        return True

    @staticmethod
    def _normalize_name(name: str):
        return name.strip().lower()

    def _is_name_conflict(self, name: str) -> bool:
        return RecipeManager._normalize_name(name) in self.recipe_name_mapping


def main() -> None:
    mgr = RecipeManager()
    mgr.add_recipe(1, 'Mapo Tofu', ['spice', 'tofu'])
    mgr.update_recipe(1, 'mapo Tofu', ['red pepper', 'tofu'])
    mgr.add_recipe(2, 'Kongbao Chicken', ['chicken', 'peanut'])
    mgr.add_recipe(3, 'Jingjiang Rousi', ['pork', 'pancake'])
    mgr.delete_recipe(2)
    print(mgr.get_recipe(1))
    print(mgr.get_recipe(2))
    print(mgr.get_recipe(3))


if __name__ == "__main__":
    main()