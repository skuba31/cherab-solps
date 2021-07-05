# cython: language_level=3

# Copyright 2016-2021 Euratom
# Copyright 2016-2021 United Kingdom Atomic Energy Authority
# Copyright 2016-2021 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

from raysect.optical cimport Spectrum, Point3D, Vector3D
from cherab.core cimport Plasma, AtomicData
from cherab.core.model.lineshape cimport GaussianLine, LineShapeModel
from cherab.core.utility.constants cimport RECIP_4_PI
from cherab.core.math.mappers import AxisymmetricMapper

from cherab.solps cimport SOLPSFunction2D


cdef class SOLPSLineEmitter(PlasmaModel):

    def __init__(self, SOLPSFunction2D radiation_function, Line line, Plasma plasma=None, AtomicData atomic_data=None,
                 object lineshape=None, object lineshape_args=None, object lineshape_kwargs=None):

        super().__init__(plasma, atomic_data)

        self._line = line

        self._power_density = AxisymmetricMapper(radiation_function)

        self._lineshape_class = lineshape or GaussianLine
        if not issubclass(self._lineshape_class, LineShapeModel):
            raise TypeError("The attribute lineshape must be a subclass of LineShapeModel.")

        if lineshape_args:
            self._lineshape_args = lineshape_args
        else:
            self._lineshape_args = []
        if lineshape_kwargs:
            self._lineshape_kwargs = lineshape_kwargs
        else:
            self._lineshape_kwargs = {}

        # ensure that cache is initialised
        self._change()

    def __repr__(self):
        return '<SOLPSLineEmitter: element={}, charge={}, transition={}>'.format(self._line.element.name, self._line.charge, self._line.transition)

    cpdef Spectrum emission(self, Point3D point, Vector3D direction, Spectrum spectrum):

        cdef double ne, ni, te, radiance

        # cache data on first run
        if self._lineshape is None:
            self._populate_cache()

        # add emission line to spectrum
        radiance = RECIP_4_PI * self._power_density(point.x, point.y, point.z)
        return self._lineshape.add_line(radiance, point, direction, spectrum)

    cdef int _populate_cache(self) except -1:

        # sanity checks
        if self._plasma is None or self._atomic_data is None:
            raise RuntimeError("The emission model is not connected to a plasma object.")

        if self._line is None:
            raise RuntimeError("The emission line has not been set.")

        # locate target species
        try:
            self._target_species = self._plasma.composition.get(self._line.element, self._line.charge)
        except ValueError:
            raise RuntimeError("The plasma object does not contain the ion species for the specified line "
                               "(element={}, ionisation={}).".format(self._line.element.symbol, self._line.charge))

        # identify wavelength
        self._wavelength = self._plasma.atomic_data.wavelength(self._line.element, self._line.charge, self._line.transition)

        # instance line shape renderer
        self._lineshape = self._lineshape_class(self._line, self._wavelength, self._target_species, self._plasma,
                                                *self._lineshape_args, **self._lineshape_kwargs)

    def _change(self):

        # clear cache to force regeneration on first use
        self._target_species = None
        self._wavelength = 0.0
        self._lineshape = None
