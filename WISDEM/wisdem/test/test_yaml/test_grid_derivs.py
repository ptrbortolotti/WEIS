import unittest

import numpy as np

import openmdao.api as om
from openmdao.utils.assert_utils import assert_check_partials

from wisdem.glue_code.gc_WT_DataStruc import ComputeGrid


class Test(unittest.TestCase):

    def test_derivatives(self):
        tower_init_options = {}
        tower_init_options['n_height'] = n_height = 6
        
        comp = ComputeGrid(init_options=tower_init_options)

        prob = om.Problem()
        prob.model.add_subsystem('comp', comp)
        prob.setup(force_alloc_complex=True)

        prob['comp.ref_axis'] = np.random.random((n_height, 3))
        prob.run_model()

        check = prob.check_partials(compact_print=True, method='cs', step=1e-40)

        # Can visually check partials information this way
        # om.partial_deriv_plot('s', 'ref_axis', check, tol=1e-8, binary=False)

        assert_check_partials(check)
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
