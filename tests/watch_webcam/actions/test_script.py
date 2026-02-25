from unittest.mock import patch, call

from watch_webcam.actions.script import Script


@patch("subprocess.run")
def test_switch_on_runs_on_scripts(mock_run):
    script = Script(on=["/on1.sh", "/on2.sh"], off=["/off.sh"])
    script.switch(True)
    mock_run.assert_has_calls([
        call("/on1.sh", check=True, shell=True),
        call("/on2.sh", check=True, shell=True),
    ])


@patch("subprocess.run")
def test_switch_off_runs_off_scripts(mock_run):
    script = Script(on=["/on.sh"], off=["/off1.sh", "/off2.sh"])
    script.switch(False)
    mock_run.assert_has_calls([
        call("/off1.sh", check=True, shell=True),
        call("/off2.sh", check=True, shell=True),
    ])


@patch("subprocess.run")
def test_switch_on_with_no_on_scripts(mock_run):
    script = Script(off=["/off.sh"])
    script.switch(True)
    mock_run.assert_not_called()


@patch("subprocess.run")
def test_switch_off_with_no_off_scripts(mock_run):
    script = Script(on=["/on.sh"])
    script.switch(False)
    mock_run.assert_not_called()


@patch("subprocess.run", side_effect=__import__("subprocess").CalledProcessError(1, "/fail.sh"))
def test_failed_script_logs_warning(mock_run, caplog):
    import logging
    script = Script(on=["/fail.sh"])
    with caplog.at_level(logging.WARNING, logger="logger"):
        script.switch(True)
    assert "/fail.sh" in caplog.text
