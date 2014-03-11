from tests import TestCase
from tests import test


class TestSms(TestCase):
    @test
    def test_life(self):
        answer = yield self.prompt("What's the meaning of life?")
        self.assertEqual(answer, "42")

    # @test
    # def test_swipe(self):
    #     def swipe_detected(marionette):
    #         # TODO(ato): Implement
    #         import time
    #         time.sleep(2)
    #         return True

    #     yield self.instruct("Swipe on the screen")
    #     detected_swipe = Wait(self.marionette).until(swipe_detected)
    #     self.assertTrue(detected_swipe)
