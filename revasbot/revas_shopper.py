import os

class RevasShopper:
    resource_script = ''

    def __init__(self, execute_script):
        self.execute_script = execute_script

        with open(
            os.path.join('scripts', 'buyResources.js'),
            'r', encoding='utf-8'
        ) as resource_script_file:
            self.resource_script = ''.join(resource_script_file.readlines())

    def buy_resources(self, resources: list[dict[str, str]]) -> None:
        data = '&'.join([f'{r["id"]}={r["amount"]}' for r in resources])
        self.execute_script(self.resource_script.replace('<data>', data))
