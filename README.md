# service-dependency-order

Produce a dependency-first order or identify unresolved cycles.

A small Python command-line tool for reviewing supplied fixtures. The core report is calculated locally and does not require an account, an API key or network access.

## Quick start

Requires Python 3.10 or newer; no third-party dependencies.

```sh
git clone https://github.com/webhookcove-tools/service-dependency-order.git
cd service-dependency-order
python3 main.py examples/input.json
python3 -m unittest discover -s tests -v
```

The sample input is synthetic. Its top-level fields are `dependencies`. Compare the command output with `examples/expected.json` to see the exact report shape.

## Example result

```json
{
  "order": [
    "db",
    "api"
  ],
  "unresolved": []
}
```

## Use your own fixture

```sh
python3 main.py ./fixture.json > report.json
```

The input must be valid UTF-8 JSON using the example's structure. This is a focused utility rather than a general schema validator; missing required fields or malformed dates produce an error. No files are modified by the analysis command.

## Optional model explanation

```sh
python3 main.py examples/input.json --explain
```

This sends the computed report to the OpenAI-compatible chat endpoint configured in `config/development.env`. Environment variables take precedence:

```sh
OPENAI_BASE_URL=https://your-gateway.example/v1 \
OPENAI_API_KEY=your-credential \
OPENAI_MODEL=your-model-route \
python3 main.py ./fixture.json --explain
```

The bundled settings are development configuration. Use your own gateway settings for deployments and keep deployment credentials out of Git. `OPENAI_MODEL` identifies a gateway route; it does not establish the backing provider or model. The optional explanation prints text from the gateway; it is not schema-validated and may be inaccurate. The local report remains the reference for counts and facts.

## Boundaries

A structural dependency order does not prove deployment readiness or service health.

All input is processed locally by default. With `--explain`, the computed report leaves your machine and the gateway operator receives it. Use synthetic or approved input and check what the report contains before sending it. The client has a 30-second request timeout and no automatic retries. Errors from the gateway are surfaced rather than replaced with invented results.

## Development

`main.py` contains the local analysis and CLI. `gateway_client.py` implements the optional explanation request. The documented fixture is pinned by a standard-library unittest. Add a fixture and expected report when changing behavior.

Maintenance commits use labeled automation roles. These labels do not represent multiple human contributors.
