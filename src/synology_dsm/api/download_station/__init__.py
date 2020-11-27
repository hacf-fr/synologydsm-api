"""Synology DownloadStation API wrapper."""
from .task import SynoDownloadTask


class SynoDownloadStation:
    """An implementation of a Synology DownloadStation."""

    API_KEY = "SYNO.DownloadStation.*"
    INFO_API_KEY = "SYNO.DownloadStation.Info"
    SCHEDULE_API_KEY = "SYNO.DownloadStation.Schedule"
    STAT_API_KEY = "SYNO.DownloadStation.Statistic"
    TASK_API_KEY = "SYNO.DownloadStation.Task"

    def __init__(self, dsm):
        """Initialize a Download Station."""
        self._dsm = dsm
        self._tasks_by_id = {}
        self._schedule_config = {}
        self._stat = {}
        self._info = {}
        self._config = {}
        self.additionals = [
            "detail",
            "file",
        ]  # Can contain: detail, transfer, file, tracker, peer

    def update(self):
        """Update tasks from API."""
        self._tasks_by_id = {}
        list_data = self._dsm.get(
            self.TASK_API_KEY, "List", {"additional": ",".join(self.additionals)}
        )["data"]
        for task_data in list_data["tasks"]:
            if task_data["id"] in self._tasks_by_id:
                self._tasks_by_id[task_data["id"]].update(task_data)
            else:
                self._tasks_by_id[task_data["id"]] = SynoDownloadTask(task_data)

    # Global
    def update_info(self):
        """Update info about the Download Station instance."""
        self._info = self._dsm.get(self.INFO_API_KEY, "GetInfo")["data"]

    def get_info(self):
        """Return general informations about the Download Station instance."""
        return self._info

    def update_config(self):
        """Update configuration about the Download Station instance."""
        self._config = self._dsm.get(self.INFO_API_KEY, "GetConfig")["data"]

    def get_config(self):
        """Return configuration about the Download Station instance."""
        return self._config

    def update_schedule_config(self):
        """Update schedule configuration about the Download Station instance."""
        self._schedule_config = self._dsm.get(self.SCHEDULE_API_KEY, "GetConfig")[
            "data"
        ]

    def get_schedule_config(self):
        """Return schedule configuration about the Download Station instance."""
        return self._schedule_config

    def set_schedule_config(self, enabled: bool = None, emule_enabled: bool = None):
        """Set schedule configuration about the Download Station instance."""
        config = {}
        if enabled is not None:
            config["enabled"] = enabled
        if emule_enabled is not None:
            config["emule_enabled"] = emule_enabled
        res = self._dsm.get(self.SCHEDULE_API_KEY, "SetConfig", config)
        self.update_schedule_config()
        return res

    def update_stat(self):
        """Update statistic about the Download Station instance."""
        self._stat = self._dsm.get(self.STAT_API_KEY, "GetInfo")["data"]

    def get_stat(self):
        """Return statistic about the Download Station instance."""
        return self._stat

    # Downloads
    def get_all_tasks(self):
        """Return a list of tasks."""
        return self._tasks_by_id.values()

    def get_task(self, task_id):
        """Return task matching task_id."""
        return self._tasks_by_id[task_id]

    def create(self, uri, unzip_password=None, destination=None):
        """Create a new task (uri accepts HTTP/FTP/magnet/ED2K links)."""
        res = self._dsm.post(
            self.TASK_API_KEY,
            "Create",
            {
                "uri": ",".join(uri) if isinstance(uri, list) else uri,
                "unzip_password": unzip_password,
                "destination": destination,
            },
        )
        self.update()
        return res

    def pause(self, task_id):
        """Pause a download task."""
        res = self._dsm.get(
            self.TASK_API_KEY,
            "Pause",
            {"id": ",".join(task_id) if isinstance(task_id, list) else task_id},
        )
        self.update()
        return res

    def resume(self, task_id):
        """Resume a paused download task."""
        res = self._dsm.get(
            self.TASK_API_KEY,
            "Resume",
            {"id": ",".join(task_id) if isinstance(task_id, list) else task_id},
        )
        self.update()
        return res

    def delete(self, task_id, force_complete=False):
        """Delete a download task."""
        res = self._dsm.get(
            self.TASK_API_KEY,
            "Delete",
            {
                "id": ",".join(task_id) if isinstance(task_id, list) else task_id,
                "force_complete": force_complete,
            },
        )
        self.update()
        return res
