import glob

class Weapon:
    weapons = {}
    shots = []
    def create(weapon,pos):
        Weapon.weapons[weapon](pos)
    def add_weapon(name, value):
        Weapon.weapons[name] = value
        Weapon.shots = list(Weapon.weapons.keys())
        print(f"{Weapon.shots}")
    def init():
        for k,v in Weapon.weapons.items():
            if hasattr(v,"init"):
                getattr(v,"init")()

def auto_import():
    # 武器の自動インポート
    # weapon 下のディレクトリに__init__.pyがあると自動的に読み込む
    for fname in glob.glob('./weapon/*/__init__.py'):
        __import__(f"weapon.{fname.split('/')[2]}")
auto_import()
