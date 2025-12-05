# Design an object-oriented battle simulator for two teams.
# 1. Basic Entities
# 	•	There are two teams: Team A and Team B.
# 	•	Each team has multiple fighters (team members).
# 	•	Each fighter has at least:
# 	•	name
# 	•	health (current HP)
# 	•	attackStrength (base damage)
# 	•	(for follow-up) type / element to determine weaknesses & resistances.
#
# 2. Battle Rules (Base Version)
# 	•	Implement a function, e.g. simulateBattle(teamA, teamB), that makes the two teams fight until one team wins.
# 	•	In each turn:
# 	•	Choose an attacker from one team and a defender from the other team (only from still-alive fighters).
# 	•	The attacker deals damage equal to its attackStrength to the defender.
# 	•	The defender’s health is reduced accordingly.
# 	•	If a fighter’s health drops to 0 or below, that fighter is dead and can no longer act.
# 	•	The battle ends when:
# 	•	All fighters on one team are dead.
# 	•	The other team is declared the winner.
#
# (The exact turn order/target selection strategy can be defined by you or specified by the interviewer — e.g., round-robin, random, always first alive, etc.)
#
# 3. Logging Requirements
# During the battle, you must record a detailed action log in order:
# 	•	Each attack:
# 	•	Which fighter attacked whom.
# 	•	How much damage was dealt.
# 	•	The defender’s health before and after the attack (optional but nice).
# 	•	Death events:
# 	•	When a fighter dies, log something like:
# "[Alice] has been defeated."
# 	•	Battle result:
# 	•	At the end, log which team won:
# "Team A wins" or "Team B wins".
#
# The function should return this log (e.g., as a list of strings).
#
# Follow-up: Weakness / Resistance System
# Extend the design so that type matchups affect damage:
# 	•	Each fighter has a type (or element), e.g. "Fire", "Water", "Grass", etc.
# 	•	For each fighter, define:
# 	•	A set of weakness types → when attacked by these types, they take double damage.
# 	•	A set of resistant types (or “counter types”) → when attacked by these types, they take half damage.
#
# Updated Damage Rule
# 	•	Base damage: attackStrength
# 	•	If the attacker’s type is in the defender’s weakness list:
# 	•	effectiveDamage = attackStrength * 2
# 	•	Else if the attacker’s type is in the defender’s resistance list:
# 	•	effectiveDamage = attackStrength * 0.5
# 	•	Else:
# 	•	effectiveDamage = attackStrength
#
# Apply effectiveDamage to defender’s health.
#
# Extra Logging for Follow-up
# When type interactions happen, the log should explain it:
# 	•	If weakness triggers (2× damage):
# "[FireMage] attacks [IceWarrior] for 40 damage (weakness: Fire > Ice, damage doubled)."
# 	•	If resistance triggers (0.5× damage):
# "[WaterKnight] attacks [GrassRogue] for 10 damage (resistance: Grass resists Water, damage halved)."
#
# And still log deaths & final winner as before.

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Tuple, Optional, Protocol, Literal


EventType = Literal["battle_start", "battle_end", "round_start", "attack", "death", "warning"]

@dataclass
class BattleEvent:
    type: EventType
    message: str                  # human-readable
    attacker: Optional[str] = None
    defender: Optional[str] = None
    damage: Optional[float] = None
    round_num: Optional[int] = None
    extra: dict = None

# class FighterType(Enum):
#     FIRE: int
#     WATER: int
#     GRASS: int

@dataclass
class Fighter:
    name: str
    max_health: int
    # a computed field that derived from a constructor parameter
    health: int = field(init=False)
    attack_strength: int
    type_: str
    # extended
    weaknesses: Set[str] = field(default_factory=set)
    resistances: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.health = self.max_health

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def _damage_multiplier(self, attacker_type: str) -> Tuple[float, Optional[str]]:
        """
        Returns (multiplier, reason_string_or_None)
        multiplier:
          - 2.0 if attacker_type in weaknesses
          - 0.5 if attacker_type in resistances
          - 1.0 otherwise
        """
        if attacker_type in self.weaknesses:
            return 2.0, f"weakness: {attacker_type} > {self.type_}"
        if attacker_type in self.resistances:
            return 0.5, f"resistance: {self.type_} resists {attacker_type}"
        return 1.0, None

    def take_attack(self, attacker: "Fighter") -> List[BattleEvent]:
        """
        Apply damage from `attacker` to self, return (effective_damage, logs).
        """
        # logs: List[str] = []
        events: List[BattleEvent] = []
        if not self.is_alive:
            # Usually shouldn't happen, but let's be safe.
            # logs.append(f"[WARN] {self.name} is already defeated.")
            # return 0.0, logs
            events.append(BattleEvent(
                type="warning",
                message=f"{self.name} is already defeated.",
                attacker=attacker.name,
                defender=self.name,
            ))
            return events

        # TODO: peel off damage calc logic to: DamageCalculator.compute_damage(attacker: Fighter, defender: Fighter)
        # so I can plug in different combat systems (e.g., crits, armor, random variance) without touching Fighter or the simulator.
        base_damage = attacker.attack_strength
        multiplier, reason = self._damage_multiplier(attacker.type_)
        effective_damage = base_damage * multiplier

        before_hp = self.health
        self.health = max(0, self.health - int(effective_damage))
        after_hp = self.health

        msg = (
            f"{attacker.name} ({attacker.type_}) attacks {self.name} ({self.type_}) "
            f"for {effective_damage:.1f} damage. HP: {before_hp} -> {after_hp}"
        )
        if reason:
            msg = (
                f"{attacker.name} ({attacker.type_}) attacks {self.name} ({self.type_}) "
                f"for {effective_damage:.1f} damage ({reason}, base={base_damage}). "
                f"HP: {before_hp} -> {after_hp}"
            )
        #     logs.append(
        #         f"{attacker.name} ({attacker.type_}) attacks {self.name} ({self.type_}) "
        #         f"for {effective_damage:.1f} damage ({reason}, base={base_damage}). "
        #         f"HP: {before_hp} -> {after_hp}"
        #     )
        # else:
        #     logs.append(
        #         f"{attacker.name} ({attacker.type_}) attacks {self.name} ({self.type_}) "
        #         f"for {effective_damage:.1f} damage. HP: {before_hp} -> {after_hp}"
        #     )
        events.append(BattleEvent(
            type="attack",
            message=msg,
            attacker=attacker.name,
            defender=self.name,
            damage=effective_damage,
            extra={
                "attacker_type": attacker.type_,
                "defender_type": self.type_,
                "before_hp": before_hp,
                "after_hp": after_hp,
                "reason": reason,
            }
        ))

        if after_hp == 0:
            # logs.append(f"{self.name} has been defeated.")
            events.append(BattleEvent(
                type="death",
                message=f"{self.name} has been defeated.",
                defender=self.name,
            ))

        # return effective_damage, logs
        return events

# NOTE: AttackOrderStrategy is defined as a Protocol instead of an ABC.
# A Protocol in Python provides *structural typing*: any object that has a
# compatible `get_attackers(team)` method is considered a valid strategy,
# even if it does NOT explicitly inherit from AttackOrderStrategy.
#
# Inheriting from the Protocol (as DefaultAttackOrder does) is optional.
# It does not create a runtime requirement; it only makes the developer’s
# intent clearer and improves IDE/type-checker hints.
class AttackOrderStrategy(Protocol):
    # Quoted type names (such as "Team" and "Fighter") are *forward references*.
    # They prevent NameError if the referenced classes have not been defined yet
    # and are fully supported by type checkers.
    def get_attackers(self, team: "Team") -> List["Fighter"]:
        # this Protocol only declares the method signature, not an implementation.
        # `...` is commonly used in stub files and Protocol definitions to indicate "no implementation here".
        ...

class TargetSelectionStrategy(Protocol):
    def choose_target(
            self, attacker: "Fighter", defenders: List["Fighter"]
    ) -> Optional["Fighter"]:
        ...

class BattleFlowStrategy(Protocol):
    def choose_next_teams(
            self,
            team_a: "Team",
            team_b: "Team",
            last_attacker: Optional["Team"],
            last_turn_had_kill: bool,
    ) -> Optional[Tuple["Team", "Team"]]:
        """
        Return (attacker_team, defender_team) for the next turn,
        or None if the battle should end (no more turns).
        """
        ...

class DefaultAttackOrder(AttackOrderStrategy):
    def get_attackers(self, team: "Team") -> List["Fighter"]:
        # simple: all alive fighters in team order
        return team.alive_fighters

class RandomAttackOrder(AttackOrderStrategy):
    def get_attackers(self, team: "Team") -> List["Fighter"]:
        fighters = team.alive_fighters[:]
        random.shuffle(fighters)
        return fighters

class FirstAliveTarget(TargetSelectionStrategy):
    def choose_target(
            self, attacker: "Fighter", defenders: List["Fighter"]
    ) -> Optional["Fighter"]:
        return defenders[0] if defenders else None

class RandomTarget(TargetSelectionStrategy):
    def choose_target(
            self, attacker: "Fighter", defenders: List["Fighter"]
    ) -> Optional["Fighter"]:
        if not defenders:
            return None
        return random.choice(defenders)

class AlternatingFlow(BattleFlowStrategy):
    def choose_next_teams(
            self,
            team_a: "Team",
            team_b: "Team",
            last_attacker: Optional["Team"],
            last_turn_had_kill: bool,
    ) -> Optional[Tuple["Team", "Team"]]:
        # First turn: let team_a start
        if last_attacker is None:
            return team_a, team_b

        # After that, just alternate
        if last_attacker is team_a:
            return team_b, team_a
        else:
            return team_a, team_b

class ExtraTurnOnKillFlow(BattleFlowStrategy):
    def choose_next_teams(
            self,
            team_a: "Team",
            team_b: "Team",
            last_attacker: Optional["Team"],
            last_turn_had_kill: bool,
    ) -> Optional[Tuple["Team", "Team"]]:
        # First turn: team_a starts
        if last_attacker is None:
            return team_a, team_b

        # If you killed someone, you keep the initiative
        if last_turn_had_kill:
            attacker = last_attacker
            defender = team_b if last_attacker is team_a else team_a
            return attacker, defender

        # Otherwise, alternate
        if last_attacker is team_a:
            return team_b, team_a
        else:
            return team_a, team_b

@dataclass
class Team:
    name: str
    fighters: List[Fighter]

    @property
    def alive_fighters(self) -> List[Fighter]:
        return [f for f in self.fighters if f.is_alive]

    @property
    def is_defeated(self) -> bool:
        return len(self.alive_fighters) == 0

class BattleSimulator:
    def __init__(
            self,
            attack_order_strategy: AttackOrderStrategy | None = None,
            target_selection_strategy: TargetSelectionStrategy | None = None,
            flow_strategy: Optional[BattleFlowStrategy] = None,
    ):
        # Decouple who acts when and who they hit from the core battle loop by injecting strategy objects.
        # That lets us plug in smarter AI later (e.g., focus lowest HP, focus healer, etc.)
        # without changing the simulator itself.
        self.attack_order_strategy = attack_order_strategy or DefaultAttackOrder()
        self.target_selection_strategy = target_selection_strategy or FirstAliveTarget()
        self.flow_strategy = flow_strategy or AlternatingFlow()

    def simulate_battle(self, team_a: Team, team_b: Team) -> List[BattleEvent]:
        """
        Simulate the battle between team_a and team_b.
        Returns a chronological list of log strings.
        """
        # logs: List[str] = []
        events: List[BattleEvent] = []
        # logs.append(f"Battle starts: {team_a.name} vs {team_b.name}")
        events.append(BattleEvent(
            type="battle_start",
            message=f"Battle starts: {team_a.name} vs {team_b.name}",
        ))

        # Simple deterministic turn order: A then B then A then B...
        # attacker_team, defender_team = team_a, team_b
        last_attacker: Optional[Team] = None
        last_turn_had_kill = False
        round_num = 1

        while not team_a.is_defeated and not team_b.is_defeated:
            pair = self.flow_strategy.choose_next_teams(
                team_a, team_b, last_attacker, last_turn_had_kill
            )
            if pair is None:
                break
            attacker_team, defender_team = pair

            # logs.append(f"--- Round {round_num}: {attacker_team.name} attacks ---")
            events.append(BattleEvent(
                type="round_start",
                message=f"--- Round {round_num}: {attacker_team.name} attacks ---",
                round_num=round_num,
            ))
            self._do_team_turn(attacker_team, defender_team, events)

            last_attacker = attacker_team
            # Check victory after this half-round
            if defender_team.is_defeated:
                # logs.append(f"All members of {defender_team.name} have been defeated.")
                # logs.append(f"{attacker_team.name} wins the battle!")
                events.append(BattleEvent(
                    type="battle_end",
                    message=f"{attacker_team.name} wins the battle!",
                ))
                break

            # Swap roles for next round
            # attacker_team, defender_team = defender_team, attacker_team
            round_num += 1

        # return logs
        return events

    def _do_team_turn(self, attackers: Team, defenders: Team, events: List[BattleEvent]) -> None:
        """
        One "turn" for attackers team: each alive attacker hits one alive defender.
        Strategy:
            - Iterate attackers in order.
            - Each attacker attacks the first alive defender of the other team.
        """
        attacker_list = self.attack_order_strategy.get_attackers(attackers)
        if not attacker_list:
            # logs.append(f"{attackers.name} has no fighters left to attack.")
            events.append(
                BattleEvent(
                    type="warning",
                    message=f"{attackers.name} has no fighters left to attack.",
                )
            )
            return

        for attacker in attacker_list:
            # Re-check if defenders still have someone alive
            defender_list = defenders.alive_fighters
            if not defender_list:
                # logs.append(f"No defenders left for {attackers.name} to attack.")
                events.append(
                    BattleEvent(
                        type="warning",
                        message=f"No defenders left for {attackers.name} to attack.",
                    )
                )
                break

            target = self.target_selection_strategy.choose_target(attacker, defender_list)
            if target is None:
                # logs.append(f"{attacker.name} has no valid target.")
                events.append(
                    BattleEvent(
                        type="warning",
                        message=f"{attacker.name} has no valid target.",
                        attacker=attacker.name,
                    )
                )
                continue

            # _, attack_logs = target.take_attack(attacker)
            attack_events = target.take_attack(attacker)
            # logs.extend(attack_logs)
            events.extend(attack_events)

            # TODO: introduce WinConditionStrategy.check_winner(team_a: Team, team_b: Team)
            if defenders.is_defeated:
                break

def render_text_log(events: List[BattleEvent]) -> List[str]:
    return [e.message for e in events]

# ----- Example usage -----
if __name__ == "__main__":
    # Define some fighters with types, weaknesses, and resistances
    # Example "Pokemon-ish" setup
    alice = Fighter(
        name="Alice",
        max_health=50,
        attack_strength=12,
        type_="Fire",
        weaknesses={"Water"},
        resistances={"Grass"},
    )
    bob = Fighter(
        name="Bob",
        max_health=45,
        attack_strength=10,
        type_="Water",
        weaknesses={"Electric"},
        resistances={"Fire"},
    )
    charlie = Fighter(
        name="Charlie",
        max_health=40,
        attack_strength=15,
        type_="Grass",
        weaknesses={"Fire"},
        resistances={"Water"},
    )

    diana = Fighter(
        name="Diana",
        max_health=55,
        attack_strength=11,
        type_="Electric",
        weaknesses={"Ground"},
        resistances=set(),
    )
    eric = Fighter(
        name="Eric",
        max_health=35,
        attack_strength=13,
        type_="Fire",
        weaknesses={"Water"},
        resistances={"Grass"},
    )

    team_a = Team(name="Team A", fighters=[alice, bob, charlie])
    team_b = Team(name="Team B", fighters=[diana, eric])

    sim = BattleSimulator(
        attack_order_strategy=RandomAttackOrder(),
        target_selection_strategy=RandomTarget(),
    )
    events = sim.simulate_battle(team_a, team_b)
    text_log = render_text_log(events)

    for line in text_log:
        print(line)