import random
import math
import matplotlib.pyplot as plt

# 1. Environment
class GuessingEnvironment:
    def __init__(self, low, high, secret=None):
        self.low = low
        self.high = high
        self.secret = random.randint(low, high) if secret is None else secret
        self.attempts = 0

    def give_feedback(self, guess):
        self.attempts += 1
        if guess == self.secret:
            return "correct"
        elif guess < self.secret:
            return "higher"
        else:
            return "lower"

# 2. Agents
class BinarySearchAgent:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.last_guess = None
        self.history = []

    def make_guess(self):
        if self.low > self.high:
            raise ValueError("Range is empty: feedback was inconsistent!")
        self.last_guess = (self.low + self.high) // 2
        return self.last_guess

    def receive_feedback(self, feedback):
        self.history.append((self.last_guess, feedback))
        if feedback == "higher":
            self.low = self.last_guess + 1
        elif feedback == "lower":
            self.high = self.last_guess - 1

class RandomAgent(BinarySearchAgent):
    def make_guess(self):
        self.last_guess = random.randint(self.low, self.high)
        return self.last_guess

class LinearAgent(BinarySearchAgent):
    def make_guess(self):
        self.last_guess = self.low
        return self.last_guess

# 3. Game Loop
def play_game(agent, env, verbose=False):
    while True:
        guess = agent.make_guess()
        feedback = env.give_feedback(guess)
        if verbose:
            print(f"Attempt {env.attempts:>2} | Range [{agent.low}, {agent.high}] | Guess = {guess} | Feedback = {feedback}")
        agent.receive_feedback(feedback)
        if feedback == "correct":
            return env.attempts

# 4. Single Verbose Demo
low, high = 1, 100
env = GuessingEnvironment(low, high, secret=73)
agent = BinarySearchAgent(low, high)
attempts = play_game(agent, env, verbose=True)
print(f"\nThe agent found {env.secret} in {attempts} attempts.")
print(f"Theoretical worst case for n = {high - low + 1}: {math.ceil(math.log2(high - low + 1))} attempts")

# 5. Experiments
def average_attempts(agent_class, low, high, games=2000):
    total = 0
    for _ in range(games):
        env = GuessingEnvironment(low, high)
        agent = agent_class(low, high)
        total += play_game(agent, env)
    return total / games

def worst_case_attempts(agent_class, low, high):
    worst = 0
    for secret in range(low, high + 1):
        env = GuessingEnvironment(low, high, secret=secret)
        agent = agent_class(low, high)
        worst = max(worst, play_game(agent, env))
    return worst

n = high - low + 1
print(f"\nRange: {low}-{high} (n = {n})\n")
for name, cls in [("Binary Search Agent", BinarySearchAgent), ("Random Agent", RandomAgent), ("Linear Agent", LinearAgent)]:
    avg = average_attempts(cls, low, high)
    worst = worst_case_attempts(cls, low, high)
    print(f"{name:<20} average = {avg:>6.2f}   worst case = {worst}")
print(f"\nTheory: ceil(log2({n})) = {math.ceil(math.log2(n))} attempts is the best possible worst case.")

# 6. Plots
sizes = [10, 100, 1000, 10000, 100000]
binary_avg, random_avg, theory = [], [], []
for n in sizes:
    binary_avg.append(average_attempts(BinarySearchAgent, 1, n, games=500))
    random_avg.append(average_attempts(RandomAgent, 1, n, games=500))
    theory.append(math.ceil(math.log2(n)))

plt.figure(figsize=(8, 5))
plt.plot(sizes, binary_avg, marker="o", label="Binary Search Agent (avg)")
plt.plot(sizes, random_avg, marker="s", label="Random Agent (avg)")
plt.plot(sizes, theory, marker="^", linestyle="--", label="ceil(log2 n) bound")
plt.xscale("log")
plt.xlabel("Range size n (log scale)")
plt.ylabel("Attempts needed")
plt.title("Guessing agents: attempts vs. problem size")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

counts = {}
for secret in range(1, 101):
    a = play_game(BinarySearchAgent(1, 100), GuessingEnvironment(1, 100, secret=secret))
    counts[a] = counts.get(a, 0) + 1

plt.figure(figsize=(7, 4))
plt.bar(list(counts.keys()), list(counts.values()))
plt.xlabel("Attempts used")
plt.ylabel("Number of secrets (out of 100)")
plt.title("Binary Search Agent: attempts distribution for 1..100")
plt.show()