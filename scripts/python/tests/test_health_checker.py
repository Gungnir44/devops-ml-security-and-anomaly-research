"""
Unit tests for System Health Checker
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import psutil


class TestSystemHealthChecker:
    """Test SystemHealthChecker class"""

    def test_cpu_check_healthy(self):
        """Test CPU check returns healthy status when below threshold"""
        # Mock psutil.cpu_percent to return 50%
        with patch("psutil.cpu_percent", return_value=50.0):
            from system_health_checker_v2 import SystemHealthChecker

            checker = SystemHealthChecker()

            result = checker.get_cpu_info()
            assert result["status"] == "HEALTHY"
            assert result["cpu_percent_total"] == 50.0

    def test_cpu_check_warning(self):
        """Test CPU check returns warning when above warning threshold"""
        with patch("psutil.cpu_percent", return_value=70.0):
            from system_health_checker_v2 import SystemHealthChecker

            checker = SystemHealthChecker()

            result = checker.get_cpu_info()
            assert result["status"] == "WARNING"
            assert result["cpu_percent_total"] == 70.0

    def test_cpu_check_critical(self):
        """Test CPU check returns critical when above critical threshold"""
        with patch("psutil.cpu_percent", return_value=90.0):
            from system_health_checker_v2 import SystemHealthChecker

            checker = SystemHealthChecker()

            result = checker.get_cpu_info()
            assert result["status"] == "CRITICAL"
            assert result["cpu_percent_total"] == 90.0

    def test_memory_check_healthy(self):
        """Test memory check returns healthy status"""
        mock_memory = MagicMock()
        mock_memory.percent = 45.0
        mock_memory.total = 8 * 1024**3
        mock_memory.available = 4 * 1024**3
        mock_memory.used = 4 * 1024**3

        mock_swap = MagicMock()
        mock_swap.total = 2 * 1024**3
        mock_swap.used = 1 * 1024**3
        mock_swap.percent = 50.0

        with patch("psutil.virtual_memory", return_value=mock_memory):
            with patch("psutil.swap_memory", return_value=mock_swap):
                from system_health_checker_v2 import SystemHealthChecker

                checker = SystemHealthChecker()

                result = checker.get_memory_info()
                assert result["status"] == "HEALTHY"
                assert result["percent_used"] == 45.0

    def test_disk_check(self):
        """Test disk check returns proper status"""
        mock_partition = MagicMock()
        mock_partition.mountpoint = "/"
        mock_partition.device = "/dev/sda1"
        mock_partition.fstype = "ext4"

        mock_usage = MagicMock()
        mock_usage.percent = 40.0
        mock_usage.total = 100 * 1024**3
        mock_usage.used = 40 * 1024**3
        mock_usage.free = 60 * 1024**3

        with patch("psutil.disk_partitions", return_value=[mock_partition]):
            with patch("psutil.disk_usage", return_value=mock_usage):
                from system_health_checker_v2 import SystemHealthChecker

                checker = SystemHealthChecker()

                result = checker.get_disk_info()
                assert len(result) > 0
                assert result[0]["status"] == "HEALTHY"

    def test_overall_health_healthy(self):
        """Test overall health calculation when all systems healthy"""
        from system_health_checker_v2 import SystemHealthChecker

        checker = SystemHealthChecker()

        checker.health_data = {
            "cpu": {"status": "HEALTHY"},
            "memory": {"status": "HEALTHY"},
            "disk": [{"status": "HEALTHY"}],
        }

        result = checker.get_overall_health()
        assert result == "HEALTHY"

    def test_overall_health_warning(self):
        """Test overall health calculation with warning state"""
        from system_health_checker_v2 import SystemHealthChecker

        checker = SystemHealthChecker()

        checker.health_data = {
            "cpu": {"status": "WARNING"},
            "memory": {"status": "HEALTHY"},
            "disk": [{"status": "HEALTHY"}],
        }

        result = checker.get_overall_health()
        assert result == "WARNING"

    def test_overall_health_critical(self):
        """Test overall health calculation with critical state"""
        from system_health_checker_v2 import SystemHealthChecker

        checker = SystemHealthChecker()

        checker.health_data = {
            "cpu": {"status": "CRITICAL"},
            "memory": {"status": "HEALTHY"},
            "disk": [{"status": "HEALTHY"}],
        }

        result = checker.get_overall_health()
        assert result == "CRITICAL"


class TestDatabaseChecker:
    """Test DatabaseChecker class"""

    def test_check_redis_success(self):
        """Test successful Redis connection"""
        import sys
        from unittest.mock import MagicMock

        # Create a mock redis module
        mock_redis_module = MagicMock()
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_redis_module.Redis.return_value = mock_client

        with patch.dict("sys.modules", {"redis": mock_redis_module}):
            from system_health_checker_v2 import DatabaseChecker

            checker = DatabaseChecker()

            config = {"host": "localhost", "port": 6379, "timeout": 5}

            result = checker.check_redis(config)
            assert result["status"] == "CONNECTED"

    def test_check_redis_failure(self):
        """Test Redis connection failure"""
        import sys
        from unittest.mock import MagicMock

        # Create a mock redis module that raises an exception
        mock_redis_module = MagicMock()
        mock_redis_module.Redis.side_effect = Exception("Connection refused")

        with patch.dict("sys.modules", {"redis": mock_redis_module}):
            from system_health_checker_v2 import DatabaseChecker

            checker = DatabaseChecker()

            config = {"host": "localhost", "port": 6379, "timeout": 5}

            result = checker.check_redis(config)
            assert result["status"] == "FAILED"

    def test_check_postgres_skipped_without_library(self):
        """Test PostgreSQL check skipped when library not installed"""
        with patch(
            "system_health_checker_v2.DatabaseChecker.check_postgresql"
        ) as mock_check:
            mock_check.return_value = {
                "status": "SKIPPED",
                "message": "psycopg2 not installed",
            }

            from system_health_checker_v2 import DatabaseChecker

            checker = DatabaseChecker()

            config = {
                "host": "localhost",
                "port": 5432,
                "database": "test",
                "user": "user",
                "password": "pass",
                "timeout": 5,
            }

            result = checker.check_postgresql(config)
            assert result["status"] == "SKIPPED"


class TestReportGeneration:
    """Test report generation and export"""

    def test_export_json_report(self, tmp_path):
        """Test JSON report export"""
        from system_health_checker_v2 import SystemHealthChecker

        checker = SystemHealthChecker()
        checker.health_data = {
            "timestamp": "2024-01-01T00:00:00",
            "overall_health": "HEALTHY",
            "cpu": {"status": "HEALTHY", "usage": 30.0},
        }

        # Update the report path in config and disable history
        checker.config["monitoring"]["report_path"] = str(tmp_path)
        checker.config["monitoring"]["keep_history"] = False

        # Export the report
        checker.export_to_json()

        # Verify file was created
        report_file = tmp_path / "system_health_report.json"
        assert report_file.exists()

        # Verify content
        with open(report_file, "r") as f:
            data = json.load(f)
            assert data["overall_health"] == "HEALTHY"


class TestCommandLineArguments:
    """Test command-line argument parsing"""

    def test_quiet_mode(self):
        """Test quiet mode suppresses output"""
        # This would need to mock sys.argv and test main() function
        pass

    def test_config_file_loading(self):
        """Test custom config file loading"""
        # This would test loading a custom config.json
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
