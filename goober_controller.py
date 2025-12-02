import time
import random

class Goober:
    """
    Represents a single Goober creature with various needs.
    Needs are stored as dictionary values, where a HIGHER value means a 
    MORE URGENT need.
    """
    def __init__(self, name="Goo-Bot"):
        self.name = name
        # Initial needs: 0 = fully satisfied, 100 = critical
        self.needs = {
            "hunger": 50,
            "thirst": 30,
            "sleepiness": 60,
            "reproduction": 10
        }
        self.energy = 100
        self.status = "Idle"
        print(f"--- {self.name} created! ---")

    def display_needs(self):
        """Prints the current state of all needs."""
        print(f"\n--- {self.name}'s Current Needs ---")
        # Sort needs from highest (most urgent) to lowest
        sorted_needs = sorted(self.needs.items(), key=lambda item: item[1], reverse=True)
        for need, value in sorted_needs:
            # Use color-coding based on urgency (simple text version)
            urgency = ""
            if value > 75: urgency = "(CRITICAL)"
            elif value > 50: urgency = "(High)"
            elif value > 25: urgency = "(Medium)"
            else: urgency = "(Low)"
            
            print(f"  - {need.capitalize()}: {value:03d} {urgency}")
        print(f"  - Energy: {self.energy}")
        print("---------------------------------")

    def _perform_task(self, need_key, action_description, satisfaction_amount, energy_cost):
        """Generic method to handle task execution and need adjustment."""
        self.status = f"Performing: {action_description}"
        print(f"[{self.name}] AI DECISION: Highest need is {need_key.capitalize()} ({self.needs[need_key]}).")
        print(f"[{self.name}] ACTION: Starting to {action_description}...")

        # Decrease the primary need
        self.needs[need_key] = max(0, self.needs[need_key] - satisfaction_amount)
        # Decrease energy
        self.energy = max(0, self.energy - energy_cost)
        
        # Adjusting other needs slightly (as time passes during the action)
        for key in self.needs:
            if key != need_key:
                # Other needs increase slightly while busy
                self.needs[key] = min(100, self.needs[key] + 1) 

        print(f"[{self.name}] Finished {action_description}. {need_key.capitalize()} is now {self.needs[need_key]}. Energy remaining: {self.energy}.")
        self.status = "Idle"

    # --- Task Methods ---
    def eat(self):
        """The Goober eats, decreasing hunger."""
        self._perform_task("hunger", "Eat Food", 30, 5)

    def drink(self):
        """The Goober drinks, decreasing thirst."""
        self._perform_task("thirst", "Find Water Source", 25, 3)

    def sleep(self):
        """The Goober sleeps, decreasing sleepiness and recovering energy."""
        # Sleep is a special action that restores energy
        restored_energy = 50 
        self.energy = min(100, self.energy + restored_energy)
        self._perform_task("sleepiness", "Take a Nap", 40, 0)
        
    def find_mate(self):
        """The Goober seeks reproduction."""
        self._perform_task("reproduction", "Seek a Companion", 20, 8)
        
    def idle(self):
        """No urgent task, Goober rests slightly."""
        self.status = "Idling"
        self.energy = min(100, self.energy + 1)
        print(f"[{self.name}] AI DECISION: All needs are low. Idling to conserve energy.")


class AI_Controller:
    """
    The brain that decides the Goober's next action based on need prioritization.
    """
    def __init__(self, goober):
        self.goober = goober
        # Maps the need key to the corresponding Goober method
        self.task_map = {
            "hunger": goober.eat,
            "thirst": goober.drink,
            "sleepiness": goober.sleep,
            "reproduction": goober.find_mate
        }
        
    def decide_and_act(self):
        """
        The main AI logic:
        1. Find the need with the maximum value (highest urgency).
        2. Check for critical energy levels.
        3. Execute the corresponding task.
        """
        # 1. Find the most urgent need
        most_urgent_need = max(self.goober.needs, key=self.goober.needs.get)
        max_need_value = self.goober.needs[most_urgent_need]
        
        # 2. Critical Energy Check (Overriding Priority)
        # If energy is too low, the Goober must sleep, regardless of other needs.
        if self.goober.energy < 15 and self.goober.needs["sleepiness"] < 100:
            print(f"[{self.goober.name}] CRITICAL OVERRIDE: Energy is too low ({self.goober.energy})! Must sleep!")
            self.goober.sleep()
            return

        # 3. Execute the task
        if max_need_value > 25: # Only act if the need is above a threshold
            action = self.task_map[most_urgent_need]
            action()
        else:
            self.goober.idle()

# --- Simulation Setup ---

# Initialize the Goober and the AI
my_goober = Goober("Ploopy")
goober_ai = AI_Controller(my_goober)

# Simulation loop
max_cycles = 15
print(f"\n--- Starting {max_cycles} Goober AI Cycles ---\n")

for cycle in range(1, max_cycles + 1):
    print(f"\n======== CYCLE {cycle} ========")
    
    # 1. Display current state
    my_goober.display_needs()
    
    # 2. AI decides and acts
    goober_ai.decide_and_act()
    
    # 3. Time passes (Needs passively increase)
    for need in my_goober.needs:
        # Needs increase randomly between 1 and 5 each cycle
        my_goober.needs[need] = min(100, my_goober.needs[need] + random.randint(1, 5))
        
    # Energy slowly drains over time
    my_goober.energy = max(0, my_goober.energy - 2)

    time.sleep(0.5) # Pause to make the simulation readable

print("\n--- Simulation Complete ---")
