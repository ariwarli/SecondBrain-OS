import tempfile
import unittest
from pathlib import Path
from unittest import mock

import model_router as mr


class ModelRouterTest(unittest.TestCase):
    def test_get_model_for_use_case_returns_tuple(self):
        with mock.patch.object(mr, "load_openclaw_config") as mock_load, mock.patch.object(
            mr, "load_model_aliases"
        ) as mock_aliases, mock.patch.object(
            mr, "_load_resolution_cache", return_value={}
        ), mock.patch.object(mr, "_save_resolution_cache"), mock.patch.object(
            mr, "_probe_model", return_value=False
        ):
            mock_load.return_value = {
                "models": {
                    "providers": {"ollama-cloud": {"baseUrl": "https://ollama.com/v1", "apiKey": "x"}}
                }
            }
            mock_aliases.return_value = {
                "classifier": {
                    "primary": "ollama-cloud/qwen3.5:4b",
                    "fallback": "ollama-cloud/nemotron-3-nano:4b",
                    "requestedPrimary": "ollama-cloud/qwen3.5:4b",
                    "requestedFallback": "ollama-cloud/nemotron-3-nano:4b",
                    "maxTokens": 180,
                    "temperature": 0,
                }
            }
            primary, fallback = mr.get_model_for_use_case("classifier")
            self.assertEqual(primary.provider, "ollama-cloud")
            self.assertEqual(primary.model_id, "qwen3.5:4b")
            self.assertEqual(primary.max_tokens, 180)
            self.assertEqual(primary.temperature, 0)
            self.assertIsNotNone(fallback)
            self.assertEqual(fallback.model_id, "nemotron-3-nano:4b")

    def test_load_model_aliases_prefers_state_file(self):
        with mock.patch.object(mr, "load_openclaw_config") as mock_load:
            with tempfile.TemporaryDirectory() as tmpdir:
                aliases_path = Path(tmpdir) / "model-router-aliases.json"
                aliases_path.write_text(
                    '{"modelAliases":{"classifier":{"primary":"ollama-cloud/qwen3.5","fallback":"ollama-cloud/minimax-m2.7"}}}',
                    encoding="utf-8",
                )
                mock_load.return_value = {"models": {"modelAliases": {"classifier": {"primary": "broken"}}}}
                aliases = mr.load_model_aliases(path=aliases_path)
        self.assertEqual(aliases["classifier"]["primary"], "ollama-cloud/qwen3.5")

    def test_get_model_for_use_case_prefers_requested_when_probe_succeeds(self):
        with mock.patch.object(mr, "load_openclaw_config") as mock_load, mock.patch.object(
            mr, "load_model_aliases"
        ) as mock_aliases, mock.patch.object(
            mr, "_load_resolution_cache", return_value={}
        ), mock.patch.object(mr, "_save_resolution_cache"), mock.patch.object(
            mr, "_probe_model", side_effect=lambda provider, model, cfg: model == "qwen3.5:4b"
        ):
            mock_load.return_value = {
                "models": {
                    "providers": {"ollama-cloud": {"baseUrl": "https://ollama.com/v1", "apiKey": "x"}}
                }
            }
            mock_aliases.return_value = {
                "classifier": {
                    "primary": "ollama-cloud/qwen3.5",
                    "fallback": "ollama-cloud/minimax-m2.1",
                    "requestedPrimary": "ollama-cloud/qwen3.5:4b",
                    "requestedFallback": "ollama-cloud/nemotron-3-nano:4b",
                    "maxTokens": 180,
                    "temperature": 0,
                }
            }
            primary, fallback = mr.get_model_for_use_case("classifier")
            self.assertEqual(primary.model_id, "qwen3.5:4b")
            self.assertEqual(fallback.model_id, "minimax-m2.1")

    def test_get_model_for_use_case_falls_back_when_requested_fails(self):
        with mock.patch.object(mr, "load_openclaw_config") as mock_load, mock.patch.object(
            mr, "load_model_aliases"
        ) as mock_aliases, mock.patch.object(
            mr, "_load_resolution_cache", return_value={}
        ), mock.patch.object(mr, "_save_resolution_cache"), mock.patch.object(
            mr, "_probe_model", side_effect=lambda provider, model, cfg: model == "qwen3.5"
        ):
            mock_load.return_value = {
                "models": {
                    "providers": {"ollama-cloud": {"baseUrl": "https://ollama.com/v1", "apiKey": "x"}}
                }
            }
            mock_aliases.return_value = {
                "classifier": {
                    "primary": "ollama-cloud/qwen3.5",
                    "fallback": "ollama-cloud/minimax-m2.1",
                    "requestedPrimary": "ollama-cloud/qwen3.5:4b",
                    "requestedFallback": "ollama-cloud/nemotron-3-nano:4b",
                    "maxTokens": 180,
                    "temperature": 0,
                }
            }
            primary, fallback = mr.get_model_for_use_case("classifier")
            self.assertEqual(primary.model_id, "qwen3.5")
            self.assertEqual(fallback.model_id, "minimax-m2.1")

    def test_unknown_use_case_raises_error(self):
        with mock.patch.object(mr, "load_openclaw_config") as mock_load, mock.patch.object(
            mr, "load_model_aliases"
        ) as mock_aliases:
            mock_load.return_value = {"models": {}}
            mock_aliases.return_value = {}
            with self.assertRaises(ValueError) as ctx:
                mr.get_model_for_use_case("unknown")
            self.assertIn("Unknown use_case", str(ctx.exception))

    def test_helper_functions_call_get_model(self):
        with mock.patch.object(mr, "get_model_for_use_case") as mock_get:
            mock_get.return_value = (mock.Mock(), None)
            mr.get_classifier_model()
            mock_get.assert_called_with("classifier")
            mr.get_wiki_model()
            mock_get.assert_called_with("wiki_ingest")
            mr.get_dm_model()
            mock_get.assert_called_with("reed_dm")
            mr.get_wellbeing_model()
            mock_get.assert_called_with("wellbeing")


if __name__ == "__main__":
    unittest.main()
