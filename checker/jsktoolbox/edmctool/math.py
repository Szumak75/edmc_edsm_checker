# -*- coding: utf-8 -*-
"""
  math.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2024, 13:00:50
  
  Purpose: 
"""

import math
import time
import random

from inspect import currentframe
from queue import Queue, SimpleQueue
from typing import Optional, List, Tuple, Union, Any, Dict
from types import FrameType, MethodType
from abc import ABC, abstractmethod
from itertools import permutations
from sys import maxsize

from types import FrameType

from ..attribtool import ReadOnlyClass
from ..raisetool import Raise
from .base import BLogClient
from .logs import LogClient
from .data import RscanData
from .stars import StarsSystem
from .edsm_keys import EdsmKeys

try:
    import numpy as np  # type: ignore
except ModuleNotFoundError:
    pass

try:
    from scipy.spatial import distance  # type: ignore
except ModuleNotFoundError:
    pass


class IAlg(ABC):
    """Interface for algorithm class ."""

    @abstractmethod
    def run(self) -> None:
        """Run the work."""

    @abstractmethod
    def debug(self, currentframe, message) -> None:
        """Debug formatter for logger."""

    @property
    @abstractmethod
    def get_final(self) -> list:
        """Return final data."""


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    E_METHODS: str = "__e_methods__"
    R_DATA: str = "__e_r_data__"


class Euclid(BLogClient):
    """Euclid.

    A class that calculates the length of a vector in Cartesian space.
    """

    def __init__(self, queue: Union[Queue, SimpleQueue], r_data: RscanData) -> None:
        """Create class object."""

        self._set_data(
            key=_Keys.E_METHODS,
            set_default_type=List,
            value=[
                self.__numpy_l2,
                self.__numpy,
                self.__einsum,
                self.__scipy,
                self.__math,
                self.__core,
            ],
        )

        # init log subsystem
        if isinstance(queue, (Queue, SimpleQueue)):
            self.logger = LogClient(queue)
        else:
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(queue)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )

        if isinstance(r_data, RscanData):
            self._set_data(
                key=_Keys.R_DATA,
                set_default_type=RscanData,
                value=r_data,
            )
            self.debug(currentframe(), f"{r_data}")
        else:
            raise Raise.error(
                f"RscanData type expected, '{type(r_data)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )

        self.debug(currentframe(), "Initialize dataset")

    @property
    def __r_data(self) -> RscanData:
        """Return data."""
        return self._get_data(key=_Keys.R_DATA)  # type: ignore

    @property
    def __euclid_methods(self) -> List[MethodType]:
        """Return test list."""
        return self._get_data(key=_Keys.E_METHODS)  # type: ignore

    def benchmark(self) -> None:
        """Do benchmark test.

        Compare the computational efficiency of functions for real data
        and choose the right priority of their use.
        """
        p_name: str = f"{self.__r_data.plugin_name}"
        c_name: str = f"{self._c_name}"

        if self.logger:
            self.logger.info = f"{p_name}->{c_name}: Warming up math system..."
        data1: List[List[float]] = [
            [641.71875, -536.06250, -6886.37500],
            [10.31250, -160.53125, 74.18750],
            [51.40625, -54.40625, -30.50000],
            [45.59375, -51.90625, -39.46875],
            [22.28125, -43.40625, -36.18750],
            [11.18750, -37.37500, -31.84375],
            [5.90625, -30.50000, -36.37500],
            [11.18750, -37.37500, -31.84375],
            [5.62500, -36.65625, -33.87500],
            [-0.56250, -43.71875, -30.81250],
        ]
        data2: List[List[float]] = [
            [67.50000, -74.90625, -93.68750],
            [134.12500, 15.09375, -63.87500],
            [124.50000, 4.31250, -49.12500],
            [118.93750, -8.53125, -33.46875],
            [105.96875, -20.87500, -22.21875],
            [95.40625, -33.50000, -11.40625],
            [78.34375, -42.96875, -2.21875],
            [66.84375, -60.65625, -3.84375],
            [60.93750, -75.25000, 10.87500],
            [58.28125, -92.09375, 23.71875],
        ]

        # build test
        test = []
        bench_out = {}

        for item in self.__euclid_methods:
            if item(data1[0], data2[0]) is not None:
                test.append(item)

        # start test
        for item in test:
            t_start: float = time.time()
            for idx in range(0, len(data1)):
                item(data1[idx], data2[idx])
            t_stop: float = time.time()
            bench_out[t_stop - t_start] = item

        # optimize list of the methods
        self.__euclid_methods.clear()
        for idx in sorted(bench_out.keys()):
            self.__euclid_methods.append(bench_out[idx])
            self.debug(currentframe(), f"{idx}: {bench_out[idx]}")

        if self.logger:
            self.logger.info = f"{p_name}->{c_name}: done."

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.__r_data.plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = (
            f"{currentframe.f_code.co_name}" if currentframe is not None else ""
        )
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"

    def __core(self, point_1: List[float], point_2: List[float]) -> float:
        """Do calculations without math libraries.

        The method iterates over each pair of vector elements,
        performs calculations on it and sums up the intermediate results.
        """
        return sum((i - j) ** 2 for i, j in zip(point_1, point_2)) ** 0.5
        # return math.sqrt(sum((i - j) ** 2 for i, j in zip(point_1, point_2)))

    def __math(self, point_1: List[float], point_2: List[float]) -> Optional[float]:
        """Try to use math lib."""
        try:
            return math.dist(point_1, point_2)
        except Exception as ex:
            self.debug(currentframe(), f"{ex}")
        return None

    def __numpy_l2(self, point_1: List[float], point_2: List[float]) -> Optional[float]:
        """Try to use numpy lib.

        The method uses the fact that the Euclidean distance of two vectors
        is nothing but the L^2 norm of their difference.
        """
        try:
            return np.linalg.norm(np.array(point_1) - np.array(point_2))  # type: ignore
        except Exception as ex:
            self.debug(currentframe(), f"{ex}")
        return None

    def __numpy(self, point_1: List[float], point_2: List[float]) -> Optional[float]:
        """Try to use numpy lib.

        The method is an optimization of the core method using numpy
        and vectorization.
        """
        try:
            return np.sqrt(np.sum((np.array(point_1) - np.array(point_2)) ** 2))
        except Exception as ex:
            self.debug(currentframe(), f"{ex}")
        return None

    def __einsum(self, point_1: List[float], point_2: List[float]) -> Optional[float]:
        """Try to use numpy lib.

        Einstein summation convention.
        """
        try:
            tmp = np.array(point_1) - np.array(point_2)
            return np.sqrt(np.einsum("i,i->", tmp, tmp))
        except Exception as ex:
            self.debug(currentframe(), f"{ex}")
        return None

    def __scipy(self, point_1: List[float], point_2: List[float]) -> Optional[float]:
        """Try to use scipy lib.

        The scipy library has a built-in function to calculate
        the Euclidean distance.
        """
        try:
            return distance.euclidean(point_1, point_2)
        except Exception as ex:
            self.debug(currentframe(), f"{ex}")
        return None

    def distance(self, point_1: List[float], point_2: List[float]) -> float:
        """Find the first working algorithm and do the calculations."""
        out: float = None  # type: ignore
        i = 0

        while out is None:
            if i < len(self.__euclid_methods):
                out = self.__euclid_methods[i](point_1, point_2)
            else:
                break
            i += 1

        return out


class AlgAStar(IAlg, BLogClient):

    __plugin_name: str = None  # type: ignore
    __math: Euclid = None  # type: ignore
    __data: List[StarsSystem] = None  # type: ignore
    __jump_range: int = None  # type: ignore
    __final: List[StarsSystem] = None  # type: ignore
    __start: StarsSystem = None  # type: ignore

    def __init__(
        self,
        start: StarsSystem,
        systems: List[StarsSystem],
        jump_range: int,
        log_queue: Optional[Union[Queue, SimpleQueue]],
        euclid_alg: Euclid,
        plugin_name: str,
    ) -> None:

        self.__plugin_name = plugin_name
        # init log subsystem
        if isinstance(log_queue, (Queue, SimpleQueue)):
            self.logger = LogClient(log_queue)
        else:
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(log_queue)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        # Euclid's algorithm for calculating the length of vectors
        if isinstance(euclid_alg, Euclid):
            self.__math = euclid_alg
        else:
            raise Raise.error(
                f"Euclid type expected, '{type(euclid_alg)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if isinstance(jump_range, int):
            self.__jump_range = jump_range
        else:
            raise Raise.error(
                f"Int type expected, '{type(jump_range)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(start, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(start)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(systems, List):
            raise Raise.error(
                f"list type expected, '{type(systems)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.debug(currentframe(), "Initialize dataset")

        self.__start = start
        self.__data = systems
        self.__final = []

    def __get_neighbors(self, point: StarsSystem) -> List[StarsSystem]:
        """Zwraca sąsiadów, którzy są w zasięgu max_range."""
        neighbors: List[StarsSystem] = []
        for p in self.__data:
            if (
                p not in self.__final
                and self.__math.distance(point.star_pos, p.star_pos)
                <= self.__jump_range
            ):
                neighbors.append(p)
        return neighbors

    def __reconstruct_path(
        self, came_from: dict, current: StarsSystem
    ) -> List[StarsSystem]:
        """Rekonstruuje ścieżkę od punktu startowego do celu."""
        path: List[StarsSystem] = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.__plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"

    def run(self) -> None:
        """Implementacja algorytmu A*."""
        open_set: List[StarsSystem] = [self.__start]
        came_from: Dict = {}
        g_score: Dict[StarsSystem, float] = {self.__start: 0.0}
        f_score: Dict[StarsSystem, float] = {
            self.__start: self.__math.distance(
                self.__start.star_pos, self.__data[0].star_pos
            )
        }

        while open_set:
            current: StarsSystem = min(
                open_set, key=lambda point: f_score.get(point, float("inf"))
            )
            if current in self.__data:
                self.__final = self.__reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor in self.__get_neighbors(current):
                tentative_g_score: float = g_score[current] + self.__math.distance(
                    current.star_pos, neighbor.star_pos
                )

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.__math.distance(
                        neighbor.star_pos, self.__data[0].star_pos
                    )
                    if neighbor not in open_set:
                        open_set.append(neighbor)

        self.__final = []

    @property
    def get_final(self) -> List[StarsSystem]:
        """Return final data."""
        return [point for point in self.__final if point != self.__start]


class AlgTsp(IAlg, BLogClient):
    """Travelling salesman problem."""

    __plugin_name: str = None  # type: ignore
    __math: Euclid = None  # type: ignore
    __data: List[StarsSystem] = None  # type: ignore
    __tmp: List[Any] = None  # type: ignore
    __jump_range: int = None  # type: ignore
    __final: List[StarsSystem] = None  # type: ignore

    def __init__(
        self,
        start: StarsSystem,
        systems: List[StarsSystem],
        jump_range: int,
        log_queue: Optional[Union[Queue, SimpleQueue]],
        euclid_alg: Euclid,
        plugin_name: str,
    ) -> None:
        """Construct instance object.

        params:
        start: StarsSystem - object with starting position.
        systems: list(StarsSystem,...) - list with point of interest to visit
        jump_range: int - jump range in ly
        log_queue: queue for LogClient
        euclid_alg: Euclid - object of initialized vectors class
        plugin_name: str - name of plugin for debug log
        """
        self.__plugin_name = plugin_name
        # init log subsystem
        if isinstance(log_queue, (Queue, SimpleQueue)):
            self.logger = LogClient(log_queue)
        else:
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(log_queue)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        # Euclid's algorithm for calculating the length of vectors
        if isinstance(euclid_alg, Euclid):
            self.__math = euclid_alg
        else:
            raise Raise.error(
                f"Euclid type expected, '{type(euclid_alg)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if isinstance(jump_range, int):
            self.__jump_range = jump_range
        else:
            raise Raise.error(
                f"Int type expected, '{type(jump_range)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(start, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(start)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(systems, list):
            raise Raise.error(
                f"list type expected, '{type(systems)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.debug(currentframe(), "Initialize dataset")

        self.__data = []
        self.__tmp = []
        self.__final = []
        self.__data.append(start)
        for item in systems:
            self.__data.append(item)

    def run(self) -> None:
        """Run algorithm."""
        # stage 1: generate a cost table
        self.__stage_1_costs()
        # stage 2: search the solution
        self.__stage_2_solution()
        # finalize
        self.__final_update()

    def __stage_1_costs(self) -> None:
        """Stage 1: generate a cost table."""
        count: int = len(self.__data)
        for idx in range(count):
            self.__tmp.append([])
            for idx2 in range(count):
                self.__tmp[idx].append(
                    self.__math.distance(
                        self.__data[idx].star_pos, self.__data[idx2].star_pos
                    )
                )
        self.debug(currentframe(), f"{self.__tmp}")

    def __stage_2_solution(self) -> None:
        """Stage 2: search the solution."""
        out: List[Any] = []
        vertex: List[int] = []
        start: int = 0
        for i in range(len(self.__data)):
            if i != start:
                vertex.append(i)
        # store minimum weight Hamilton Cycle
        min_path: float = float(maxsize)
        next_permutation = permutations(vertex)

        for i in next_permutation:
            # store current Path weight
            current_path_weight: float = 0.0
            # compute current path weight
            k: int = start
            for j in i:
                current_path_weight += self.__tmp[k][j]
                k = j
            current_path_weight += self.__tmp[k][start]

            # update minimum
            if min_path > current_path_weight:
                out = [current_path_weight, i]
                min_path = current_path_weight

        # best solution
        if self.logger:
            self.logger.debug = f"DATA: {self.__data}"
        if self.logger:
            self.logger.debug = f"PATH: {out}"
        # add start system as first
        self.__tmp = [0]
        # and merge with output
        self.__tmp.extend(list(out[1]))

    def __final_update(self) -> None:
        """Build final dataset."""
        self.__final = []
        d_sum = 0
        if self.logger:
            self.logger.debug = f"TMP: {self.__tmp}"
        for idx in range(1, len(self.__tmp)):
            system = self.__data[self.__tmp[idx]]
            system.data[EdsmKeys.DISTANCE] = self.__math.distance(
                self.__data[self.__tmp[idx - 1]].star_pos,
                self.__data[self.__tmp[idx]].star_pos,
            )
            d_sum += system.data[EdsmKeys.DISTANCE]
            self.__final.append(system)
        if self.logger:
            self.logger.debug = f"FINAL Distance: {d_sum:.2f} ly"
        if self.logger:
            self.logger.debug = f"INPUT: {self.__data}"
        if self.logger:
            self.logger.debug = f"OUTPUT: {self.__final}"

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.__plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"

    @property
    def get_final(self) -> List[StarsSystem]:
        """Return final data."""
        return self.__final


class AlgGenetic(IAlg, BLogClient):
    """Genetic algorithm solving the problem of finding the best path."""

    __plugin_name: str = None  # type: ignore
    __math: Euclid = None  # type: ignore
    __final: List[StarsSystem] = None  # type: ignore

    __points: List[StarsSystem] = None  # type: ignore
    __start_point: StarsSystem = None  # type: ignore
    __max_distance: int = None  # type: ignore
    __population_size: int = None  # type: ignore
    __generations: int = None  # type: ignore
    __mutation_rate: float = None  # type: ignore
    __crossover_rate: float = None  # type: ignore

    def __init__(
        self,
        start: StarsSystem,
        systems: List[StarsSystem],
        jump_range: int,
        log_queue: Optional[Union[Queue, SimpleQueue]],
        euclid_alg: Euclid,
        plugin_name: str,
    ) -> None:
        """Construct instance object.

        params:
        start: StarsSystem - object with starting position.
        systems: list(StarsSystem,...) - list with point of interest to visit
        jump_range: int - jump range in ly
        log_queue: queue for LogClient
        euclid_alg: Euclid - object of initialized vectors class
        plugin_name: str - name of plugin for debug log
        """

        self.__plugin_name = plugin_name
        # init log subsystem
        if isinstance(log_queue, (Queue, SimpleQueue)):
            self.logger = LogClient(log_queue)
        else:
            raise Raise.error(
                f"Queue or SimpleQueue type expected, '{type(log_queue)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        # Euclid's algorithm for calculating the length of vectors
        if isinstance(euclid_alg, Euclid):
            self.__math = euclid_alg
        else:
            raise Raise.error(
                f"Euclid type expected, '{type(euclid_alg)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if isinstance(jump_range, int):
            self.__max_distance = jump_range
        else:
            raise Raise.error(
                f"Int type expected, '{type(jump_range)}' received",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(start, StarsSystem):
            raise Raise.error(
                f"StarsSystem type expected, '{type(start)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        if not isinstance(systems, list):
            raise Raise.error(
                f"list type expected, '{type(systems)}' received.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.debug(currentframe(), "Initialize dataset")

        self.__points = systems
        self.__start_point = start
        self.__population_size = 100
        self.__generations = 100
        self.__mutation_rate = 0.05
        self.__crossover_rate = 0.4

    def __generate_individual(self) -> List[StarsSystem]:
        individual: List[StarsSystem] = [self.__start_point]
        remaining_points: List[StarsSystem] = self.__points.copy()
        while remaining_points:
            closest_point: StarsSystem = min(
                remaining_points,
                key=lambda point: self.__math.distance(
                    individual[-1].star_pos, point.star_pos
                ),
            )
            if (
                self.__math.distance(individual[-1].star_pos, closest_point.star_pos)
                > self.__max_distance
            ):
                break
            individual.append(closest_point)
            remaining_points.remove(closest_point)
        return individual

    def __generate_population(self) -> List[List[StarsSystem]]:
        population: List[List[StarsSystem]] = []
        for _ in range(self.__population_size):
            population.append(self.__generate_individual())
        return population

    def __get_fitness(self, individual: List[StarsSystem]) -> float:
        distance: float = 0
        for i in range(len(individual) - 1):
            distance += self.__math.distance(
                individual[i].star_pos, individual[i + 1].star_pos
            )
        return 1 / distance if distance > 0 else float("inf")

    def __select_parents(
        self, population: List[List[StarsSystem]]
    ) -> Tuple[List[StarsSystem], List[StarsSystem]]:
        parent1: List[StarsSystem]
        parent2: List[StarsSystem]
        parent1, parent2 = random.choices(
            population,
            weights=[self.__get_fitness(individual) for individual in population],
            k=2,
        )
        return parent1, parent2

    def __crossover(
        self, parent1: List[StarsSystem], parent2: List[StarsSystem]
    ) -> List[StarsSystem]:
        if random.random() > self.__crossover_rate:
            return parent1
        crossover_point: int = random.randint(1, len(parent1) - 2)
        child: List[StarsSystem] = parent1[:crossover_point] + [
            point for point in parent2 if point not in parent1[:crossover_point]
        ]
        return child

    def __mutate(self, individual: List[StarsSystem]) -> List[StarsSystem]:
        mutation_point1: int
        mutation_point2: int
        if random.random() > self.__mutation_rate:
            return individual
        mutation_point1, mutation_point2 = random.sample(
            range(1, len(individual) - 1), 2
        )
        individual[mutation_point1], individual[mutation_point2] = (
            individual[mutation_point2],
            individual[mutation_point1],
        )
        return individual

    def __evolve(self) -> List[StarsSystem]:
        population: List[List[StarsSystem]] = self.__generate_population()
        best_individual: List[StarsSystem] = None  # type: ignore
        for i in range(self.__generations):
            fitnesses: List[float] = [
                self.__get_fitness(individual) for individual in population
            ]
            best_individual = population[fitnesses.index(max(fitnesses))]
            if len(best_individual) == len(self.__points) + 1:
                break
            new_population: List[List[StarsSystem]] = [best_individual]
            while len(new_population) < self.__population_size:
                parent1: List[StarsSystem]
                parent2: List[StarsSystem]
                child: List[StarsSystem]
                parent1, parent2 = self.__select_parents(population)
                child = self.__crossover(parent1, parent2)
                child = self.__mutate(child)
                new_population.append(child)
            population = new_population
        return best_individual

    def run(self) -> None:
        """Run algorithm."""
        self.__final = self.__evolve()
        self.__final.remove(self.__start_point)
        # update distance
        d_sum: float = 0.0
        start: StarsSystem = self.__start_point
        for item in self.__final:
            end: StarsSystem = item
            end.data[EdsmKeys.DISTANCE] = self.__math.distance(
                start.star_pos, end.star_pos
            )
            d_sum += end.data[EdsmKeys.DISTANCE]
            start = end
        if self.logger:
            self.logger.debug = f"FINAL Distance: {d_sum:.2f} ly"

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.__plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"

    @property
    def get_final(self) -> List[StarsSystem]:
        """Return final data."""
        return self.__final


# #[EOF]#######################################################################
