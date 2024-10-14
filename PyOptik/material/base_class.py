#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyOptik.units import Quantity, meter
import numpy
import warnings

class BaseMaterial:
    def __str__(self) -> str:
        """
        Provides an informal string representation of the Material object.

        Returns
        -------
        str
            Informal representation of the Material object.
        """
        return f"Material: {self.filename}"

    def __repr__(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns
        -------
        str
            Formal representation of the Material object.
        """
        return self.__str__()

    def _check_wavelength(self, wavelength_range: Quantity) -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises a warning if it is not.

        Parameters
        ----------
        lambda_um : float
            The wavelength to check, in micrometers.

        Raises
        ------
        UserWarning
            If the wavelength is outside the allowable range.
        """
        if self.wavelength_bound is not None:
            min_value, max_value = self.wavelength_bound

            if numpy.any((wavelength_range < min_value) | (wavelength_range > max_value)):
                warnings.warn(
                    f"Wavelength range goes from {wavelength_range.min().to_compact()} to {wavelength_range.max().to_compact()} "
                    f"which is outside the allowable range of {min_value.to_compact()} to {max_value.to_compact()} µm. "
                    f"[Material: {self.filename}]"
                )

    def ensure_units(func):
        """
        Decorator to ensure that the wavelength parameter has the correct units.

        Parameters
        ----------
        func : callable
            The function to wrap.

        Returns
        -------
        callable
            The wrapped function that ensures wavelength is a Quantity in meters.
        """
        def wrapper(self, wavelength: Quantity = None, *args, **kwargs):
            if wavelength is None:
                wavelength = numpy.linspace(self.wavelength_bound[0].magnitude, self.wavelength_bound[1].magnitude, 100) * self.wavelength_bound.units

            if not isinstance(wavelength, Quantity):
                wavelength = wavelength * meter
            return func(self, wavelength, *args, **kwargs)
        return wrapper