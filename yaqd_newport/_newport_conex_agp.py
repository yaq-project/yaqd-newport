from ._newport_motor import NewportMotor


class NewportConexAGP(NewportMotor):
    _kind = "newport-conex-agp"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._native_units = "deg"

    # def _save_state(self):
    #     try:
    #         self.logger.info(f"Will I write to disk? {self._state.updated}")
    #         super()._save_state()
    #     except Exception as e:
    #         self.logger.error(str(e))
    #         raise e

    # async def update_state(self):
    #     try:
    #         self.logger.info(f"updating state...")
    #         await super().update_state()
    #     except Exception as e:
    #         self.logger.error(str(e))
    #         raise e

