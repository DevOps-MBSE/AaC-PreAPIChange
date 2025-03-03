from unittest.async_case import IsolatedAsyncioTestCase
from pygls.lsp import methods
from pygls.lsp.types import RenameParams

from tests.helpers.lsp.responses.rename_response import RenameResponse
from tests.plugins.lsp_server.base_lsp_test_case import BaseLspTestCase
from tests.plugins.lsp_server.definition_constants import (
    TEST_DOCUMENT_CONTENT,
    TEST_DOCUMENT_NAME,
)


class TestRenameProvider(BaseLspTestCase, IsolatedAsyncioTestCase):
    async def rename(self, file_name: str, new_name: str, line: int = 0, character: int = 0) -> RenameResponse:
        """
        Send a rename request and return the response.

        Args:
            file_name (str): The name of the virtual document in which to perform the hover action.
            line (int): The line number (starting from 0) at which to perform the hover action.
            character (int): The character number (starting from 0) at which to perform the hover action.
            new_name (str): The new name to apply.

        Returns:
            A RenameResponse that is returned from the LSP server.
        """
        return await self.build_request(
            file_name,
            RenameResponse,
            methods.RENAME,
            RenameParams(**self.build_text_document_position_params(file_name, line, character), new_name=new_name),
        )

    async def test_rename_request(self):
        expected_new_name = "DataANew"
        res: RenameResponse = await self.rename(TEST_DOCUMENT_NAME, expected_new_name, 1, 8)
        actual_text_edits = res.get_all_text_edits()
        actual_document_edits = res.get_workspace_edit()
        self.assertIn(TEST_DOCUMENT_NAME, list(actual_document_edits.keys())[0])
        self.assertIn(expected_new_name, actual_text_edits[0].get("newText"))
        self.assertEqual(2, len(actual_text_edits))

    async def test_no_rename_when_nothing_under_cursor(self):
        expected_new_name = "DataANew"
        await self.write_document(TEST_DOCUMENT_NAME, f"\n{TEST_DOCUMENT_CONTENT}")
        res: RenameResponse = await self.rename(TEST_DOCUMENT_NAME, expected_new_name)
        self.assertIsNone(res.response)

    async def test_rename_request_doesnt_duplicate_colons(self):
        """Covers bugfix #597."""
        lsp_client_new_text = "DataANew:"
        expected_new_name = lsp_client_new_text.strip(":")

        res: RenameResponse = await self.rename(TEST_DOCUMENT_NAME, lsp_client_new_text, 1, 8)
        actual_text_edits = res.get_all_text_edits()
        actual_document_edits = res.get_workspace_edit()

        self.assertIn(TEST_DOCUMENT_NAME, list(actual_document_edits.keys())[0])
        self.assertEqual(expected_new_name, actual_text_edits[0].get("newText"))
        self.assertEqual(2, len(actual_text_edits))
