import json
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    scripts_dir = Path(__file__).resolve().parent
    rewards_path = scripts_dir / "rewards.json"
    plot_path = scripts_dir / "reward_curve.png"

    rewards = json.loads(rewards_path.read_text(encoding="utf-8"))
    episodes = list(range(1, len(rewards) + 1))

    plt.figure(figsize=(8, 4))
    plt.plot(episodes, rewards, linewidth=1.5, color="blue")
    plt.title("TaskMeshEnv Training Reward Curve")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"Saved reward curve to: {plot_path}")


if __name__ == "__main__":
    main()
