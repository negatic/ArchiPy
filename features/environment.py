from pydantic_settings import SettingsConfigDict

from archipy.configs.base_config import BaseConfig


class TestConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_file=".env.test",
    )


config = TestConfig()
BaseConfig.set_global(config)


def before_scenario(context, scenario):
    # Assign global config to scenario context.
    try:
        context.test_config = BaseConfig.global_config()
    except Exception as e:
        print("Error in before_scenario:", e)
