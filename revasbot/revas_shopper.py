import os

from revasbot.revas_console import RevasConsole as console
from revasbot.revas_cache import RevasCache
from revasbot.revas_pandas import RevasPandas

class RevasShopper:
    resource_script = ''

    def __init__(self, execute_script):
        self.execute_script = execute_script

        with open(
            os.path.join('scripts', 'buyResources.js'), 'r', encoding='utf-8'
        ) as resource_script_file:
            self.resource_script = ''.join(resource_script_file.readlines())

    def buy_resources(self, resources: list[dict[str, str]]) -> None:
        data = '&'.join([f'partSupplierHasPartID_{r["id"]}={r["amount"]}' for r in resources])
        self.execute_script(self.resource_script.replace('<data>', data))

    @classmethod
    def filter_resources(cls, resource: dict[str, str], cached: dict[str, str]):
        return \
            resource['name'] in cached['name'] and \
            resource['quality'] == cached['quality'] and \
            resource['supplier'] == cached['supplier']

    @classmethod
    def get_first_resource(
        cls, resource: dict[str, str], cached_resources: dict[str, dict[str, str]]
    ):
        return next(filter(
            lambda index: cls.filter_resources(
                resource, cached_resources[index]
            ),
            cached_resources
        ))

    def buy_resources_from_file(self, game_name: str) -> None:
        try:
            shopping_list = RevasPandas.read_csv('shop/resources.csv')
            cached_resources = RevasCache.cache_loader(game_name)['resources']
            length = len(list(shopping_list.values())[0])

            resources_list = [
                {
                    key: value[i]       # type: ignore
                    for key, value in shopping_list.items()
                } for i in range(length)
            ]

            to_buy_list = [
                {
                    'id': self.get_first_resource(resource, cached_resources),
                    'amount': resource['amount']
                } for resource in resources_list
            ]

            self.buy_resources(to_buy_list)

        except FileNotFoundError:
            console.error('Cannot buy resources - no resources.csv found')

            with open('shop/resources.csv', 'w', encoding='utf-8') as resource_csv:
                resource_csv.write('name,supplier,quality,amount\n')
