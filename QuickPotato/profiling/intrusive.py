from QuickPotato.configuration.management import options
from QuickPotato.utilities.exceptions import CouchPotatoCannotFindMethod
from QuickPotato.profiling.interpreters import StatisticsInterpreter
from QuickPotato.harness.testing import PerformanceTest
from QuickPotato.profiling.debugger import Profiler
from functools import wraps, partial
import uuid

performance_test = PerformanceTest()


def performance_critical(method=None, enabled=True):
    """
    This decorator can be used to gather performance statistical
    on a method.
    :param method: The method that is being profiled
    :param enabled: If True will profile the method under test
    :return: The method output
    """
    # ---------------------------------------------------------------------

    @wraps(method)
    def method_execution(*args, **kwargs):
        """
        An inner function that Will execute the method under test and enable the profiler.
        It will work together with the Results class to formulate a list containing dictionary
        that will store all metrics in a database or csv file.
        :param args: The Arguments of the method under test
        :param kwargs: The key word arguments of the method under test
        :return: the methods results
        """
        if enabled and options.enable_intrusive_profiling:

            method_id = str(uuid.uuid1())
            pf = Profiler()
            pf.profile_method_under_test(method, *args, **kwargs)

            StatisticsInterpreter(
                performance_statistics=pf.performance_statistics,
                total_response_time=pf.total_response_time,
                database_name=performance_test.test_case_name,
                test_id=performance_test.current_test_id,
                method_name=method.__name__,
                sample_id=method_id
            )

            return pf.functional_output

        else:
            return method(*args, **kwargs)

    # ---------------------------------------------------------------------

    if method is None:
        return partial(performance_critical, enabled=enabled)

    elif callable(method) is not True:
        CouchPotatoCannotFindMethod()

    else:
        # Execute the method under test
        output = method_execution

        return output
