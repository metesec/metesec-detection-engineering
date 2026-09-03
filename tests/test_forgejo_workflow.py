from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".forgejo" / "workflows" / "validate.yml"

CHECKOUT_ACTION = (
    "https://data.forgejo.org/actions/checkout@"
    "34e114876b0b11c390a56381ad16ebd13914f8d5"
)
class ForgejoWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.safe_load(cls.source)
        cls.job = cls.workflow["jobs"]["validate"]
        cls.steps = {step["name"]: step for step in cls.job["steps"]}

    def test_triggers_and_runner_are_explicit(self):
        self.assertEqual(
            set(self.workflow["on"]),
            {"push", "workflow_dispatch"},
        )
        self.assertEqual(
            self.job["runs-on"],
            "metesec-detection-validate",
        )

    def test_pipeline_has_read_only_repository_access_and_no_secrets(self):
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        self.assertEqual(
            self.steps["Check out repository"]["with"]["persist-credentials"],
            False,
        )
        self.assertNotIn("secrets.", self.source)
        self.assertNotIn("pull_request_target", self.workflow["on"])

    def test_remote_actions_are_fully_qualified_and_commit_pinned(self):
        action_steps = [step["uses"] for step in self.job["steps"] if "uses" in step]
        self.assertEqual(action_steps, [CHECKOUT_ACTION])

    def test_toolchain_and_validation_commands_are_pinned(self):
        self.assertEqual(
            self.steps["Verify runner toolchain"]["run"],
            'test "$(node --version)" = "v24.19.0"\n'
            'test "$(python --version)" = "Python 3.12.13"\n',
        )
        self.assertEqual(
            self.steps["Install pnpm"]["run"],
            'npm install --global --prefix "$RUNNER_TEMP/pnpm" pnpm@11.19.0\n'
            'echo "$RUNNER_TEMP/pnpm/bin" >> "$GITHUB_PATH"\n',
        )
        self.assertEqual(
            self.steps["Create Python environment"]["run"],
            'python -m venv "$RUNNER_TEMP/venv"\n'
            'echo "$RUNNER_TEMP/venv/bin" >> "$GITHUB_PATH"\n',
        )
        self.assertEqual(
            self.steps["Install JavaScript dependencies"]["run"],
            "pnpm install --frozen-lockfile",
        )
        self.assertEqual(
            self.steps["Install pinned Sigma toolchain"]["run"],
            "python -m pip install --requirement requirements-sigma.lock",
        )
        self.assertEqual(
            self.steps["Run complete repository validation"]["run"],
            "pnpm run check",
        )


if __name__ == "__main__":
    unittest.main()
