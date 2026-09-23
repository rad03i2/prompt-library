import json
import pytest
from prompt_library import Prompt, PromptError, PromptLibrary


def test_variables_and_render():
    p = Prompt("hello", "Hello", "Greeting", "Hi {{ name }} from {{city}}!", ["demo"])
    assert p.variables == ["city", "name"]
    assert p.render({"name": "رضوان", "city": "Mosul"}) == "Hi رضوان from Mosul!"


def test_missing_variable_is_error():
    p = Prompt("hello", "Hello", "Greeting", "Hi {{name}}", [])
    with pytest.raises(PromptError):
        p.render({})
    assert p.render({}, strict=False) == "Hi {{name}}"


def test_library_load_search_and_validate(tmp_path):
    data = {"name": "code-review", "title": "Code Review", "description": "Review Python", "template": "Review {{code}}", "tags": ["python", "review"], "version": 2}
    (tmp_path / "code-review.json").write_text(json.dumps(data), encoding="utf-8")
    lib = PromptLibrary(tmp_path)
    assert lib.load("code-review").version == 2
    assert [p.name for p in lib.search("code", ["python"])] == ["code-review"]
    assert lib.validate() == []


def test_rejects_path_traversal(tmp_path):
    with pytest.raises(PromptError):
        PromptLibrary(tmp_path).load("../secret")


def test_save_refuses_overwrite(tmp_path):
    lib = PromptLibrary(tmp_path)
    prompt = Prompt("hello", "Hello", "Greeting", "Hi", [])
    lib.save(prompt)
    with pytest.raises(PromptError):
        lib.save(prompt)
