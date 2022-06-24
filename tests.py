import unittest
from aiounittest import AsyncTestCase
from botbuilder.testing import DialogTestClient, DialogTestLogger
from app import DIALOG
from config import DefaultConfig

class TestDialogs(AsyncTestCase, unittest.TestCase):
    client = DialogTestClient("test", DIALOG)
    async def test_dialogs(self):
        reply = await self.client.send_activity("hello")
        self.assertEqual(reply.text, 'What can I help you with today?')
        reply = await self.client.send_activity("i want to travel")
        self.assertEqual(reply.text, 'To what city would you like to travel?')
        reply = await self.client.send_activity("Paris")
        self.assertEqual(reply.text, 'From what city will you be travelling?')
        reply = await self.client.send_activity("Lyon")
        self.assertEqual(reply.text, 'On what date would you like to go?')
        reply = await self.client.send_activity("2022-08-15")
        self.assertEqual(reply.text, 'On what date would you like to come back?')
        reply = await self.client.send_activity("2022-08-23")
        self.assertEqual(reply.text, 'What is your maximum budget per person?')
        reply = await self.client.send_activity("230")
        self.assertEqual(reply.text, 'I understood you want to go to Paris from Lyon, going on 2022-08-15, and returning on 2022-08-23, for a maximum budget of 230 per person.')

class TestDialogs(unittest.TestCase):
    def test_env_vars(self):
        config = DefaultConfig()
        self.assertIn(config.PORT, globals())
        