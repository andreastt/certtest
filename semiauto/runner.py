import unittest


# TODO(ato): Come up with a better name for this
class PreInstantiatedTestRunner(unittest.runner.TextTestRunner):
    """Allows the `resultclass` argument to be an already instantiated
    ``unittest.results.TestResult`` implementation.

    """

    def __init__(self, *args, **kwargs):
        super(PreInstantiatedTestRunner, self).__init__(*args, **kwargs)

    def _makeResult(self):
        return self.resultclass


class TestEventDelegator(unittest.runner.TextTestResult):
    """Allows attaching callback classes for state changes to tests.

    This class injects a callback delegator preserving the behaviour
    of ``unittest.results.TestResult``.  Using ``add_callback(cb)`` on
    this class one can add additional hooks to test runner events by
    implementing the ``TestEvents`` callback interface.

    """

    def __init__(self, stream, descriptions, verbosity):
        super(TestEventDelegator, self).__init__(
            stream, descriptions, verbosity)
        self.cbs = []

    def add_callback(self, cb):
        if not isinstance(cb, TestEvents):
            cb = cb()

        self.cbs.append(cb)

    def startTestRun(self):
        super(TestEventDelegator, self).startTestRun()
        for cb in self.cbs:
            cb.on_test_run_start()

    def startTest(self, test):
        super(TestEventDelegator, self).startTest(test)
        for cb in self.cbs:
            cb.on_test_start(test)

    def addSuccess(self, test):
        super(TestEventDelegator, self).addSuccess(test)
        for cb in self.cbs:
            cb.on_success(test)

    def addError(self, test, err):
        super(TestEventDelegator, self).addError(test, err)
        for cb in self.cbs:
            cb.on_error(test, err)

    def addFailure(self, test, err):
        super(TestEventDelegator, self).addFailure(test, err)
        for cb in self.cbs:
            cb.on_failure(test, err)

    def addSkip(self, test, reason):
        super(TestEventDelegator, self).addSkip(test, reason)
        for cb in self.cbs:
            cb.on_skip(test, reason)

    def addExpectedFailure(self, test, err):
        super(TestEventDelegator, self).addExpectedFailure(test, err)
        for cb in self.cbs:
            cb.on_expected_failure(test, err)

    def addUnexpectedSuccess(self, test):
        super(TestEventDelegator, self).addUnexpectedSuccess(test)
        for cb in self.cbs:
            cb.on_unexpected_success(test)

    def stopTest(self, test):
        super(TestEventDelegator, self).stopTest(test)
        for cb in self.cbs:
            cb.on_test_stop(test)

    def stopTestRun(self):
        super(TestEventDelegator, self).stopTestRun()
        for cb in self.cbs:
            cb.on_test_run_stop()


class TestEvents(object):
    """A set of hooks triggered as a test state gets updated.

    The hooks are called immediately after the relevant
    ``unittest.runner.TextTestResult`` actions have been performed.

    """

    def on_test_run_start(self):
        pass

    def on_test_start(self, test):
        pass

    def on_success(self, test):
        pass

    def on_error(self, test):
        pass

    def on_failure(self, test, err):
        pass

    def on_skip(self, test, reason):
        pass

    def on_expected_failure(self, test, err):
        pass

    def on_unexpected_success(self, test):
        pass

    def on_test_stop(self, test):
        pass

    def on_test_run_stop(self):
        pass


class TestStateUpdater(TestEvents):
    """A test result event class that can update the host browser on the
    progress of running tests.

    Meant to be used as a callback for ``TestEventDelegator``.

    """

    def __init__(self, handler):
        """Construct a new test state updater.

        :param handler: Handler for current host browser connection,
            which should be an instance of ``server.TestHandler``.

        """

        self.client = handler

    # TODO(ato): This can be improved:
    def send_event(self, event, test=None, **kwargs):
        """Send event to the currently connected client.

        If a test specified a weak reference to it will be used
        (`test.__hash__()`).  Additional key-values can be given
        as keyword arguments.

        Because a canonical list of tests is already in the browser's
        cache it will use the test reference as a key to look up the
        test's which state to change.

        Some sample JSON objects emitted from this could be::

            {"testRunStart"}
            {"testStart": {"id": 12345678}}
            {"skip"}

        :param event: The event command to send to the client.

        :param test: Optional test to include as context.

        :param kwargs: Optional additional arguments to be included.
            These must be serializable by `json`.

        """

        payload = kwargs

        # TODO(ato): Serialization of socket.error, etc.
        if "error" in payload:
            payload["error"] = str(payload["error"])

        if test:
            payload["id"] = test.__hash__()
        self.client.emit(event, payload if payload else None)

    def on_test_run_start(self):
        self.send_event("testRunStart")

    def on_test_start(self, test):
        self.send_event("testStart", test)

    def on_success(self, test):
        self.send_event("success", test)

    def on_error(self, test, err):
        self.send_event("error", test, error=err)

    def on_failure(self, test, err):
        self.send_event("failure", test, error=err)

    def on_skip(self, test, reason):
        self.send_event("skip", test, reason=reason)

    def on_expected_failure(self, test, err):
        self.send_event("expectedFailure", test, error=err)

    def on_unexpected_success(self, test):
        self.send_event("unexpectedSuccess", test)

    def on_test_stop(self, test):
        self.send_event("testStop", test)

    def on_test_run_stop(self):
        self.send_event("testRunStop")
