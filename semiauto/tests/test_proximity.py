from tornado.testing import gen_test
from tornado import gen

from tests import TestCase
from functools import partial


class TestProximity(TestCase):
    @gen_test
    def test_proximity_change(self):
        ok = yield self.instruct("Ensure the phone is unlocked and held in your hand, perpendicular to the floor")
        self.assertTrue(ok)
        # set up listener to store changes in an object
        # NOTE: use wrappedJSObject to access non-standard properties of window
        script = """
        window.wrappedJSObject.proximityStates = [];
        window.addEventListener('userproximity',
                                function(event){
                                    console.log("proximity event" + event);
                                  window.wrappedJSObject.proximityStates.push(event);
                                });
        window.addEventListener('deviceproximity',
                                function(event){
                                    console.log("proximity event" + event);
                                  window.wrappedJSObject.proximityStates.push(event);
                                });
        """
        self.marionette.execute_script(script)
        ok = yield self.instruct("Move your hand in front of the phone and hit OK when the screen darkens")
        self.assertTrue(ok)
        proximity_values = self.marionette.execute_script("return window.wrappedJSObject.proximityStates")
        # TODO: for some reason, we don't pick up on userproximity and deviceproximity events
        # in either System or CertTest apps...
        print proximity_values
