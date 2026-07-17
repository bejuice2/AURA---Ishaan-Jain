from __future__ import annotations

from waitress import serve

import runtime_config


def main() -> None:
    errors = runtime_config.production_configuration_errors()
    if errors:
        for error in errors:
            print(f"Configuration error: {error}")
        raise SystemExit(2)

    runtime_config.ensure_data_directory()
    from production_app import app

    print(
        f"Starting AURA on {runtime_config.HOST}:{runtime_config.PORT} "
        f"in {runtime_config.ENVIRONMENT} mode"
    )
    serve(
        app,
        host=runtime_config.HOST,
        port=runtime_config.PORT,
        threads=8,
        clear_untrusted_proxy_headers=True,
    )


if __name__ == "__main__":
    main()
