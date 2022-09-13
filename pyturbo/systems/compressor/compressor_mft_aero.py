# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.mft.compressor import SimplifiedMftCompressor
from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class CompressorMftAero(System):
    """The doc"""

    def setup(self):

        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        self.add_inward("pcnr", 90.0)
        self.add_inward("gh", 0.0)
        self.add_inward("cmp_model", SimplifiedMftCompressor())
        self.add_inward("gas", IdealGas(287.058, 1004.0))  # dry air

    def compute(self):
        self.fl_out.Tt = self.gas.t_from_h(self.gas.h(self.fl_in.Tt) + self.cmp_model.ghr(self.gh))
        self.fl_out.Pt = self.fl_in.Pt * self.cmp_model.pr(self.pcnr, self.gh)
        self.fl_out.W = (
            self.cmp_model.wr(self.pcnr, self.gh) * self.fl_out.Pt / np.sqrt(self.fl_out.Tt)
        )
