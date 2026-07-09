from services.cloudflare_service import ask as cf
from services.cerebras_service import ask as cb
from services.openrouter_service import ask as op

providers = [
    ("Cloudflare", cf),
    ("Cerebras", cb),
    ("OpenRouter", op),
]

for name, provider in providers:
    print(f"\n========== {name} ==========")

    try:
        answer = provider(
            1,
            "Say hello in one short sentence."
        )

        print("SUCCESS")
        print(answer)

    except Exception as e:
        print("FAILED")
        print(type(e).__name__)
        print(e)
