from gacha import GachaSystem
from config import config

gacha = GachaSystem()
gacha.setup(config)

print("ID:")
ID = str(input())
print("times:")
gacha_times = int(input())

if gacha_times == 1:
    rank, value = gacha.pull(user_id= ID)
    print(f"Single Pull: {rank} - {value}")
elif gacha_times != 1:
    results = gacha.pull_multiple(count=gacha_times, user_id=ID)
    for i, (rank, value) in enumerate(results, 1):
        print(f"  {i}. {rank} - {value}")