import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils
from bird import Bird
from . import species
import math
import operator


class Population:
    def __init__(self, size):
        self.birds = []
        self.generation = 1
        self.species = []
        self.size = size
        # Track the best score seen across all generations for display purposes
        self.historical_best = 0
        for i in range(0, self.size):
            self.birds.append(Bird())

    def update_live_players(self, pipes=None):
        for b in self.birds:
            if b.alive:
                b.look(pipes)
                b.think()
                b.draw(utils.window)
                b.update({}, pipes)

    def natural_selection(self):
        print('SPECIATE')
        self.speciate()

        print('CALCULATE FITNESS')
        self.calculate_fitness()

        print('KILL EXTINCT')
        self.kill_extinct_species()

        print('KILL STALE')
        self.kill_stale_species()

        print('SORT BY FITNESS')
        self.sort_species_by_fitness()

        print('CHILDREN FOR NEXT GEN')
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.birds = []

        for b in self.birds:
            add_to_species = False
            for s in self.species:
                if s.similarity(b.brain):
                    s.add_to_species(b)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(b))

    def calculate_fitness(self):
        for b in self.birds:
            b.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()
        # Update historical best score
        try:
            current_best = max(getattr(b, 'score', 0) for b in self.birds)
            if current_best > self.historical_best:
                self.historical_best = current_best
                print(f'[Gen {self.generation}] New best score: {self.historical_best}')
        except Exception:
            pass

    def kill_extinct_species(self):
        species_bin = []
        for s in self.species:
            if len(s.birds) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        birds_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for b in s.birds:
                        birds_bin.append(b)
                else:
                    s.staleness = 0
        for b in birds_bin:
            self.birds.remove(b)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for _ in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.birds = []
        for child in children:
            self.birds.append(child)
        self.generation += 1

    # Return true if all players are dead
    def extinct(self):
        extinct = True
        for b in self.birds:
            if b.alive:
                extinct = False
        return extinct