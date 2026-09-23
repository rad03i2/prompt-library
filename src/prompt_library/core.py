from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

_SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_VAR = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


class PromptError(ValueError):
    pass


@dataclass(frozen=True)
class Prompt:
    name: str
    title: str
    description: str
    template: str
    tags: list[str]
    version: int = 1

    @property
    def variables(self) -> list[str]:
        return sorted(set(_VAR.findall(self.template)))

    def render(self, values: dict[str, str], strict: bool = True) -> str:
        missing = [v for v in self.variables if v not in values]
        if strict and missing:
            raise PromptError("Missing variables: " + ", ".join(missing))
        return _VAR.sub(lambda m: str(values.get(m.group(1), m.group(0))), self.template)

    @classmethod
    def from_dict(cls, data: dict) -> "Prompt":
        required = {"name", "title", "description", "template"}
        missing = required - data.keys()
        if missing:
            raise PromptError("Missing fields: " + ", ".join(sorted(missing)))
        name = str(data["name"])
        if not _SLUG.fullmatch(name):
            raise PromptError("name must be a lowercase slug of at most 64 characters")
        tags = data.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(x, str) for x in tags):
            raise PromptError("tags must be a list of strings")
        version = data.get("version", 1)
        if not isinstance(version, int) or version < 1:
            raise PromptError("version must be a positive integer")
        return cls(name, str(data["title"]), str(data["description"]), str(data["template"]), tags, version)


class PromptLibrary:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def load(self, name: str) -> Prompt:
        if not _SLUG.fullmatch(name):
            raise PromptError("Invalid prompt name")
        path = self.root / f"{name}.json"
        if not path.is_file():
            raise PromptError(f"Prompt not found: {name}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PromptError(f"Cannot read {path}: {exc}") from exc
        prompt = Prompt.from_dict(data)
        if prompt.name != name:
            raise PromptError(f"Prompt name does not match filename: {path}")
        return prompt

    def all(self) -> list[Prompt]:
        if not self.root.exists():
            return []
        prompts = []
        for path in sorted(self.root.glob("*.json")):
            prompts.append(self.load(path.stem))
        return prompts

    def search(self, query: str = "", tags: Iterable[str] = ()) -> list[Prompt]:
        words = [w.casefold() for w in query.split() if w]
        wanted = {t.casefold() for t in tags}
        scored = []
        for prompt in self.all():
            prompt_tags = {t.casefold() for t in prompt.tags}
            if wanted and not wanted.issubset(prompt_tags):
                continue
            haystack = " ".join((prompt.name, prompt.title, prompt.description, " ".join(prompt.tags))).casefold()
            if words and not all(w in haystack for w in words):
                continue
            score = sum(3 if w in prompt.title.casefold() else 1 for w in words)
            scored.append((score, prompt.name, prompt))
        return [p for _, _, p in sorted(scored, key=lambda x: (-x[0], x[1]))]

    def validate(self) -> list[str]:
        errors = []
        if not self.root.exists():
            return [f"Directory does not exist: {self.root}"]
        for path in sorted(self.root.glob("*.json")):
            try:
                self.load(path.stem)
            except PromptError as exc:
                errors.append(f"{path.name}: {exc}")
        return errors

    def save(self, prompt: Prompt, overwrite: bool = False) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f"{prompt.name}.json"
        if path.exists() and not overwrite:
            raise PromptError(f"Prompt already exists: {prompt.name}")
        path.write_text(json.dumps(asdict(prompt), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path
