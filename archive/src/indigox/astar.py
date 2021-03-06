from heapq import heappop, heappush
from itertools import count as _count
from itertools import product
from time import perf_counter

from indigox.config import (INFINITY, BASIS_LEVEL, TIMEOUT, HEURISTIC,
                           COUNTERPOISE_CORRECTED, ELECTRON_PAIRS,
                           INITIAL_LO_ENERGY)
from indigox.data import atom_enes, bond_enes
from indigox.exception import IndigoMissingParameters
from indigox.lopt import LocalOptimisation
from indigox.misc import (graph_to_dist_graph, electron_spots, electrons_to_add,
                         locs_sort, BondOrderAssignment, graph_setup, HashBitArray,
                         node_energy, bitarray_to_assignment, calculable_nodes)

BSSE = int(not COUNTERPOISE_CORRECTED)

class AStar(BondOrderAssignment):
    def __init__(self, G):
        self.init_G = G
        
    def initialise(self):
        if HEURISTIC.lower() == 'tight':
            self.heuristic = abstemious
        elif HEURISTIC.lower() == 'loose':
            self.heuristic = promiscuous
        else:
            raise IndigoMissingParameters('Unknown A* heuristic type: {}'
                                          ''.format(HEURISTIC))
        self.h_count = 0
        self.c_count = 0
        self.G = graph_to_dist_graph(self.init_G)
        self.target = electrons_to_add(self.init_G)
        self.locs = locs_sort(electron_spots(self.init_G), self.G)
        self.choices = []
        for n in self.locs:
            n_count = self.locs.count(n)
            if (n,n_count) not in self.choices:
                self.choices.append((n,n_count))
        for i in range(len(self.choices)):
            self.choices[i] = self.choices[i][1]
            
        if not INITIAL_LO_ENERGY:
            self.max_queue_energy = INFINITY / 2
        else:
            lo = LocalOptimisation(self.init_G)
            _, self.max_queue_energy = lo.run()
    
    def run(self):
        self.start_time = perf_counter()
        push = heappush
        pop = heappop
        c = _count()
        
        self.initialise()
        
        source = HashBitArray(len(self.locs))
        source.setall(False)
        i_count = 0        
        explored_count = 0;
        enqueued_count = 0;
        start = 0
        try:
            stop = self.choices[0]
        except IndexError:
            stop = 0
        child = 1
        always_calculable = calculable_nodes(self.G, source, 0, self.locs, 
                                             self.target)
        q = [(0, next(c), (source, 0), start, stop, child, 
              self.calc_energy(source, always_calculable, stop), None)]
        enqueued = {}
        explored = {}
        while q:
            qcost, _, curvert, start, stop, child, dist, parent = pop(q)
            i_count += 1
            if i_count < 20:
                print(curvert, start, stop)
#            print(curvert[0])
            if stop >= len(self.locs) and curvert[0].count() == self.target:
                bitarray_to_assignment(self.init_G, curvert[0], self.locs)
                print(i_count + len(q), "items passed through queue")
                print("Explored:", explored_count, "Enqueued:", enqueued_count)
                print("{:.3f} seconds run time".format(perf_counter()-self.start_time))
                return self.init_G, dist
                
#           if curvert in explored:
#               explored_explored += 1
#               continue
            
#           explored[curvert] = parent
            
            for n in self.neighbours(curvert[0], start, stop):
                if i_count < 20:
                    print("     ",n)
#               if n in explored:
#                   explored_count += 1
#                   continue
                calculable = calculable_nodes(self.G, n[0], stop, self.locs, 
                                              self.target)
                ncost = self.calc_energy(n[0], calculable, stop)
#               if n in enqueued:
#                   enqueued_count += 1
#                   qcost, h = enqueued[n]
#                   if qcost <= ncost:
#                       continue
#               else:
#                   self.h_count += 1
                h = self.heuristic(self.G, n[0], calculable, stop,
                                       self.target, self.locs)
                    
                if ncost + h > self.max_queue_energy:
                    continue
                    
#               enqueued[n] = ncost, h
                
                try:
                    push(q, (ncost + h, next(c), n, stop, stop + self.choices[child],
                         child + 1, ncost, curvert))
                except IndexError:
                    push(q, (ncost + h, next(c), n, stop, stop + 1,child, ncost, 
                             curvert))
        print(i_count, "items passed through queue")
        print("{:.3f} seconds run time".format(perf_counter()-self.start_time))
  
    def neighbours(self, a, start, stop):
        num = stop - start
        for i in range(num + 1):
            b = HashBitArray(a.to01())
            j = 0
            while j < i:
                b[start + j] = True
                j += 1
            yield b, stop
                      
    def calc_energy(self, a, calculable, stop, g_info=None):
        self.c_count += 1
        placed = a[:stop].count()
        to_place = self.target - placed
        available_places = a.length() - stop - to_place
        if to_place < 0 or available_places < 0:
            return INFINITY
        if g_info is None:
            graph_setup(self.G, a, self.locs)
        else:
            for n in self.G:
                self.G.node[n]['e-'] = g_info[n]['e-']
                if len(n) == 1:
                    self.G.node[n]['fc'] = g_info[n]['fc']
                
        ene = sum(node_energy(self.G, n) for n in calculable)
        if ene > INFINITY / 2:
            ene = INFINITY
        return round(ene, 5)   
    
# Heuristics
def promiscuous(G, a, calculable, stop, target, locs):
    h_ene = 0
    placed = a[:stop].count()
    to_place = target - placed
    if not to_place:
        return h_ene
    if to_place < 0:
        return INFINITY
    
    # Doesn't worry about charged bonds
    a_enes = atom_enes[BASIS_LEVEL]
    b_enes = bond_enes[BASIS_LEVEL]
    
    for n in G:
        if n in calculable:
            continue
        
        if len(n) == 1:
            h_ene += min(a_enes[G.node[n]['Z']].values())
        elif len(n) == 2:
            a_element = G.node[(n[0],)]['Z']
            b_element = G.node[(n[1],)]['Z']
            if b_element < a_element:
                a_element, b_element = b_element, a_element
            min_ene = 0
            for o in (1,2,3):
                try:
                    o_ene = b_enes[(a_element, b_element, o)][BSSE]
                except KeyError:
                    continue
                if o_ene < min_ene:
                    min_ene = o_ene
            h_ene += min_ene
            
    return h_ene

def abstemious(G, a, calculable, stop, target, locs):
    h_ene = 0
    placed = a[:stop].count()
    to_place = target - placed
    
    if not to_place:
        return h_ene
    if to_place < 0:
        return INFINITY
    
    extra_counts = {k:locs.count(k) for k in set(locs)}
    extra_able = set(locs[stop:])
    graph_setup(G, a, locs)
    
    # note where all the extra electrons can go
    for n in G:
        G.node[n]['h'] = 0
        if n not in extra_able:
            continue
        added = 0
        while added < to_place and added < extra_counts[n]:
            if ELECTRON_PAIRS:
                G.node[n]['h'] += 2
            else:
                G.node[n]['h'] += 1
            added += 1
    # figure out the lowest possible energy attainable for each node
    for n in sorted(G, key=len):
        # atoms formal charges
        if len(n) == 1:
            addable = []
            step = 2 if ELECTRON_PAIRS else 1
            addable.append(range(0, G.node[n]['h'] + 1, step))
            for nb in G[n]:
                addable.append(range(0, G.node[nb]['h'] // 2 + 1))
            fcs = set()
            for x in product(*addable):
                real_sum = (x[0]//2 + sum(x[1:]) if ELECTRON_PAIRS 
                            else x[0] + 2 * sum(x[1:]))
                if real_sum <= to_place:
                    fcs.add((G.node[n]['fc'] - sum(x), real_sum))
            G.node[n]['poss_fcs'] = fcs
            # need all possible formal charges for all atoms
            if n in calculable:
                continue
            
            fcs = set(x[0] for x in fcs)
            
            a_enes = atom_enes[BASIS_LEVEL][G.node[n]['Z']]
            try:
                h_ene += min(v for k, v in a_enes.items() if k in fcs)
            except ValueError:
                h_ene = INFINITY

        if len(n) == 2:
            if n in calculable:
                continue
            step = 2
            bos = {G.node[n]['e-'] + x 
                   for x in range(0, G.node[n]['h'] + 1, step)}
            a_ele = G.node[(n[0],)]['Z']
            b_ele = G.node[(n[1],)]['Z']
            if b_ele < a_ele:
                a_ele, b_ele = b_ele, a_ele
            b_enes = bond_enes[BASIS_LEVEL]
            h_ene += min(b_enes[(a_ele, b_ele, o//2)][BSSE] for o in bos)     
       
    return h_ene
    
