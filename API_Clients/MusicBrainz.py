import musicbrainzngs as musicb
import os
import nltk

from typing import Union, List, Optional

EMAIL = os.getenv("email")


class MusicBrainzObject(object):
    musicb.set_useragent("no-app", "v0", EMAIL)
    id: Optional[Union[str, int]] = None
    entity: Optional[str] = None
    name: Optional[str] = None
    mb_data_str: Optional[str] = None

    def __init__(
        self, entity: str, name: str = None, id: Optional[Union[str, int]] = None
    ) -> None:
        if (id is None) and (name is None):
            raise Exception("Both name and ID cannot be empty")
        self.entity = entity
        self.name = name
        self.id = id
        if id:
            self._get_mb_data_from_id(id)
        if name:
            self._get_mb_data_from_name(name)

    def _get_mb_data_from_name(self, name: str, *args, **kwargs) -> None:
        data = getattr(musicb, f"search_{self.entity}s")(name, *args, **kwargs)

        self.mb_data = self._distance_check(data[f"{self.entity}-list"], name)
        self.id = self.mb_data["id"]
        return None

    def _get_mb_data_from_id(self, id: Union[str, int], *args, **kwargs) -> None:
        self.mb_data = getattr(musicb, f"get_{self.entity}_by_id")(id, *args, **kwargs)[
            self.entity
        ]

        self.name = self.mb_data["name"]

        return None

    def __repr__(self) -> str:
        return f"{self.entity.capitalize()}: {self.name}"

    def _distance_check(
        self, data_list: List[str], reference: str, item_name: Optional(str) = "name"
    ):
        closest = (None, 10**10)
        for item in data_list:
            _distance = nltk.edit_distance(reference, item[item_name])
            if _distance < closest[1]:
                closest = (item, _distance)
            if _distance == 0:
                break

        return closest[0]

    def __eq__(self, right):
        return self.id == right.id
