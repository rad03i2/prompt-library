# Prompt Library

A local-first, searchable and versionable prompt collection with deterministic `{{variable}}` rendering, validation, a Python API, and a practical CLI. It keeps reusable prompts in reviewable JSON files instead of hiding them in application code or vendor dashboards.

## English

### Why it exists
Teams often copy prompts between scripts and chats, making changes difficult to review and reproduce. Prompt Library provides a small, provider-neutral format that works with Git, offline, and without API keys.

### Features
- Search prompt metadata by words and tags.
- Strict `{{variable}}` rendering with missing-variable detection.
- Safe prompt names that prevent path traversal.
- Validate an entire prompt directory before release.
- Human-readable UTF-8 JSON; Arabic and other Unicode text are preserved.
- Python API plus `prompt-library` and `python -m prompt_library` entry points.
- No runtime dependencies, network requests, telemetry, or secret storage.
- Included grounded summarization and code-review examples.

### Preview
```console
$ prompt-library search code
code-review    v1    Focused Code Review    [development, review, security]

$ prompt-library render summarize --var audience=developers --var "text=The release passed validation."
Summarize the text below for developers. ...
```
For screenshots, capture the CLI output above; the project is intentionally terminal/API based and has no graphical UI.

### Requirements & installation
Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

For development:
```bash
python -m pip install -e . pytest
pytest -q
```

### Usage
```bash
prompt-library list
prompt-library search review --tag security
prompt-library show code-review
prompt-library render code-review --var language=Python --var "code=print('hello')"
prompt-library validate
```
Use another collection with `--dir path/to/prompts`. Rendering is strict by default. `--allow-missing` intentionally leaves unresolved placeholders unchanged.

Prompt files follow this shape:
```json
{
  "name": "example",
  "title": "Example",
  "description": "What this prompt is for.",
  "template": "Explain {{topic}} to {{audience}}.",
  "tags": ["education"],
  "version": 1
}
```

Python API:
```python
from prompt_library import PromptLibrary

library = PromptLibrary("prompts")
prompt = library.load("summarize")
text = prompt.render({"audience": "developers", "text": "Release notes..."})
print(text)
```

### Configuration
There are no environment variables or credentials. The only runtime configuration is the prompt directory (`--dir`, default `prompts`) and render values supplied with repeated `--var KEY=VALUE` options.

### Project structure
```text
prompts/                    reusable prompt JSON files
src/prompt_library/core.py  model, rendering, search, validation
src/prompt_library/cli.py   command-line interface
tests/                      core and CLI tests
.github/workflows/ci.yml    cross-platform CI
```

### Testing
CI installs the package on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13, compiles sources, runs pytest, then validates the bundled prompts. Locally run `pytest -q` and `prompt-library validate`.

### Security & privacy
Everything runs locally. Templates are text substitution only: values are never evaluated as Python or shell code. Prompt filenames are restricted to safe slugs. Do not put credentials, private customer data, or secrets into a public prompt repository. Rendered prompts remain untrusted input to any downstream model or agent; see [SECURITY.md](SECURITY.md).

### Limitations
This is a prompt storage/search/rendering tool, not an LLM client, prompt-injection defense, evaluator, or orchestration framework. Search is deterministic substring metadata search rather than semantic/vector search. JSON files are loaded from disk on demand; very large catalogs may need an indexed backend. Templates intentionally support only simple variables—no executable expressions or control flow.

### Optional roadmap
Potential additions include schema export, import/export bundles, and optional semantic search adapters. These are not required for the current core workflow.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Prompt Library** مكتبة محلية لحفظ قوالب الأوامر النصية والبحث فيها وإدارتها بإصدارات واضحة داخل Git. تحفظ القوالب بصيغة JSON قابلة للمراجعة، وتدعم متغيرات `{{variable}}` مع تحقق صارم، وواجهة أوامر وواجهة Python، من دون الاعتماد على مزود ذكاء اصطناعي أو مفتاح API.

### لماذا المشروع؟
نسخ البرومبتات بين المحادثات والسكربتات يجعل معرفة النسخة المستخدمة ومراجعة التغييرات صعبًا. يوفر المشروع تنسيقًا بسيطًا ومحايدًا يمكن مراجعته واختباره والعمل به دون إنترنت.

### المزايا
- البحث بالكلمات والوسوم ضمن بيانات القالب.
- استبدال المتغيرات مع اكتشاف القيم الناقصة قبل الاستخدام.
- أسماء آمنة تمنع اجتياز المسارات.
- التحقق من جميع ملفات المكتبة بأمر واحد.
- دعم UTF-8 والعربية دون تحويلها إلى رموز escape عند الحفظ.
- CLI وPython API وتشغيل عبر `python -m prompt_library`.
- لا توجد اتصالات شبكة أو telemetry أو اعتماديات تشغيل خارجية.
- أمثلة فعلية لمراجعة الكود والتلخيص الملتزم بالمصدر.

### التثبيت والمتطلبات
يتطلب Python 3.10 أو أحدث:
```bash
python -m venv .venv
python -m pip install -e .
```
وللتطوير والاختبار:
```bash
python -m pip install -e . pytest
pytest -q
```

### الاستخدام
```bash
prompt-library list
prompt-library search review --tag security
prompt-library show summarize
prompt-library render summarize --var audience=developers --var "text=Release notes..."
prompt-library validate
```
يمكن تحديد مجلد مختلف عبر `--dir`. الوضع الافتراضي يرفض التصيير إذا كان متغير مطلوب ناقصًا، بينما `--allow-missing` يترك المتغير الناقص كما هو عمدًا.

### الإعداد وبنية المشروع
لا توجد متغيرات بيئة أو أسرار مطلوبة. الإعدادات هي مسار مكتبة القوالب والقيم الممررة عند التصيير. توجد القوالب في `prompts/`، والمنطق في `src/prompt_library/`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

### الاختبارات
إعداد CI مخصص لاختبار Linux وWindows وmacOS مع Python 3.10 و3.12 و3.13، ويشمل compileall وpytest والتحقق من القوالب. محليًا استخدم `pytest -q` ثم `prompt-library validate`.

### الأمان والخصوصية
العمل محلي بالكامل. استبدال المتغيرات نصي فقط ولا ينفذ Python أو أوامر shell. لا تضع أسرارًا أو بيانات عملاء في مستودع عام. القالب الناتج يظل مدخلًا غير موثوق لأي نموذج أو Agent، وهذه المكتبة لا تمنح صلاحية لتنفيذ الأدوات. راجع [SECURITY.md](SECURITY.md).

### القيود
المشروع ليس عميل LLM ولا نظام RAG ولا دفاعًا ضد Prompt Injection ولا منصة تقييم. البحث نصي في البيانات الوصفية وليس بحثًا دلاليًا، والقوالب تدعم المتغيرات البسيطة فقط دون تعبيرات قابلة للتنفيذ أو شروط برمجية. الكتالوجات الضخمة جدًا قد تحتاج قاعدة بيانات مفهرسة.

### التطوير الاختياري
يمكن مستقبلًا إضافة تصدير schema وحزم استيراد/تصدير ومحولات اختيارية للبحث الدلالي، بينما الوظائف الأساسية الحالية لا تعتمد عليها.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
