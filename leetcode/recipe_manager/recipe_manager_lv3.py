from typing import Set, List

from recipe_manager.recipe_manager_lv2 import RecipeManagerV2


class RecipeManagerV3(RecipeManagerV2):
    def __init__(self, user_ids: Set[int]):
        super().__init__()
        self.valid_user_ids = user_ids

    def edit_recipe(self, user_id: int, rid: int, new_name: str, new_ingredients: List[str]) -> bool:
        if user_id not in self.valid_user_ids:
            print(f"User id invalid: {user_id}")
            return False

        is_upd = self.update_recipe(rid, new_name, new_ingredients)
        if is_upd:
            rcp = self.recipe_id_mapping[rid]
            # Attach dynamic field to `Recipe` at runtime
            rcp.updated_by = user_id
        return is_upd


def main() -> None:
    mgr = RecipeManagerV3(user_ids={10,20,30})
    mgr.add_recipe(1, 'Mapo Tofu', ['spice', 'tofu'])
    print(mgr.get_recipe(1))
    is_edited = mgr.edit_recipe(11, 1, 'Mapo tofu', ['tofu', 'soup'])
    # User id not found
    print(f"is_edited: {is_edited}")
    is_edited = mgr.edit_recipe(10, 1, 'Mapo tofu', ['tofu', 'soup'])
    print(f"is_edited: {is_edited}")
    print(mgr.get_recipe(1))
    print(f"updated_by: {mgr.get_recipe(1).updated_by}")

if __name__ == "__main__":
    main()