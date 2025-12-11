import operator
import random

class Species:
    def __init__(self, bird):
        self.birds = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.birds.append(bird)
        self.benchmark_fitness = bird.fitness
        self.benchmark_brain = bird.brain.clone()
        self.champion = bird.clone()
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(brain_1, brain_2):
        total_weight_difference = 0
        for i in range(0, len(brain_1.connections)):
            for j in range(0, len(brain_2.connections)):
                if i == j:
                    total_weight_difference += abs(brain_1.connections[i].weight - brain_2.connections[j].weight)

        return total_weight_difference

    def add_to_species(self, bird):
        self.birds.append(bird)

    def sort_players_by_fitness(self):
        self.birds.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.birds[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.birds[0].fitness
            self.champion = self.birds[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for b in self.birds:
            total_fitness += b.fitness
        if self.birds:
            self.average_fitness = int(total_fitness / len(self.birds))
        else:
            self.average_fitness = 0

    def offspring(self):
        baby = self.birds[random.randint(1, len(self.birds)) - 1].clone()
        baby.brain.mutate()
        return baby