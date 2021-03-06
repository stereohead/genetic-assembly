
from genetic.pool import Pool

class Bio(object):
    
    def __init__(self, generations, crossover_rate, mutation_rate, population_size):
        
        self.termination_generations = generations
        self.current_generation = 0
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        
        self.pool = None
        self.tracker = DummyTracker()
    
    
    def is_done(self):
        return self.current_generation >= self.termination_generations
    
    
    def set_pool(self, pool):
        if not isinstance(pool, Pool):
            raise TypeError("'pool' argument must be an instance of Pool")
        
        self.pool = pool
        
    
    def set_tracker(self, tracker):
        self.tracker = tracker
        self.tracker.set_bio(self)
        
        
    def get_tracker(self):
        return self.tracker
    
    
    def __iter__(self):
        return self
    
    
    def __next__(self):
        if self.is_done():
            raise StopIteration()
        
        self.iterate(self.pool)
        
        return self.current_generation

    
    def iterate(self, pool):
        if pool is None:
            raise ValueError("Pool is not set")
        
        elite = pool.fittest()

        # create zombies
        self.do_mutate(pool)
        
        # have fun
        self.do_crossover(pool)
        
        pool.add(elite)
        
        # natural selection
        self.do_selection(pool)
        #pool.select(self.population_size)
        
        # happy birthday!
        self.current_generation += 1
        
        # record new generation
        self.tracker.new_generation()
        self.tracker.set_population(len(pool))
        self.tracker.set_fittest(pool.fittest())
    
    
    def do_selection(self, pool):
        pool.sort()
        pool.skim(self.population_size)
        
        #for _ in range(len(pool)- self.population_size):
        #    pool.remove(pool.pick_random())

            
    
    
    def do_mutate(self, pool):
        count = int(len(pool) * self.mutation_rate)
        
        for _ in range(count):
            old_chrom = pool.pick_random()
            pool.remove(old_chrom)
            
            new_chrom = old_chrom.mutate()
            pool.add(new_chrom)
        
    
    def do_crossover(self, pool):
        count = int(len(pool) * self.crossover_rate)

        for _ in range(count):
            p1 = pool.pick_random()
            p2 = pool.pick_random()
            
            [child1, child2] = p1.crossover(p2)
            
            pool.remove(p1)
            pool.remove(p2)
            
            pool.add(child1)
            pool.add(child2)
            
            
class DummyTracker(object):
    
    def set_bio(self, bio):
        pass
    
    def new_generation(self):
        pass
    
    def set_population(self, pop):
        pass
    
    def set_fittest(self, fitness):
        pass
    