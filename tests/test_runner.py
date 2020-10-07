import unittest
import tests.converter_package_unit_tests
import tests.model_package_unit_tests
import tests.controller_package_tests

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(tests.converter_package_unit_tests))
suite.addTests(loader.loadTestsFromModule(tests.model_package_unit_tests))
suite.addTests(loader.loadTestsFromModule(tests.controller_package_tests))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
