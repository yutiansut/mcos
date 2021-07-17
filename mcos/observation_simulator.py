import numpy as np
from abc import abstractmethod, ABC
from sklearn.covariance import LedoitWolf
from typing import Tuple

class AbstractObservationSimulator(ABC):

    @abstractmethod
    def simulate(self) -> Tuple[np.array, np.array]:
        """
        Draws empirical means and covariances. See section 4.1 of the "A Robust Estimator of the Efficient Frontier"
        paper.
        :param n_observations: number of observations
        @return: Tuple of expected return vector and covariance matrix
        """
        pass


class MuCovLedoitWolfObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> Tuple[np.array, np.array]:
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)
        return x.mean(axis=0).reshape(-1, 1), LedoitWolf().fit(x).covariance_


class MuCovObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> Tuple[np.array, np.array]:
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)
        return x.mean(axis=0).reshape(-1, 1), np.cov(x, rowvar=False)


class MuCovJackknifeObservationSimulator(AbstractObservationSimulator):

    def __init__(self, mu: np.array, cov: np.array, n_observations: int):
        self.mu = mu
        self.cov = cov
        self.n_observations = n_observations

    def simulate(self) -> Tuple[np.array, np.array]:
        x = np.random.multivariate_normal(self.mu.flatten(), self.cov, size=self.n_observations)

        idx = np.arange(len(x))
        cov_hat = np.sum(np.cov(x[idx!=i], rowvar=False) for i in range(len(x)))/float(len(x))
        x_prime = np.sum(x[idx!=i] for i in range(len(x)))/float(len(x))

        return x_prime.mean(axis=0).reshape(-1, 1), cov_hat
