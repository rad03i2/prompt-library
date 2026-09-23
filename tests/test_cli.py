import json
from prompt_library.cli import main


def seed(path):
    path.mkdir()
    (path / "hello.json").write_text(json.dumps({"name":"hello","title":"Hello","description":"Greeting","template":"Hello {{name}}","tags":["demo"],"version":1}), encoding="utf-8")


def test_cli_validate_and_render(tmp_path, capsys):
    prompts = tmp_path / "prompts"
    seed(prompts)
    assert main(["--dir", str(prompts), "validate"]) == 0
    assert "OK: 1" in capsys.readouterr().out
    assert main(["--dir", str(prompts), "render", "hello", "--var", "name=Radwan"]) == 0
    assert capsys.readouterr().out.strip() == "Hello Radwan"


def test_cli_missing_variable(tmp_path, capsys):
    prompts = tmp_path / "prompts"
    seed(prompts)
    assert main(["--dir", str(prompts), "render", "hello"]) == 2
    assert "Missing variables" in capsys.readouterr().err
