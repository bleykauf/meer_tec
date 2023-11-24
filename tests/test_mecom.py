from meer_tec.mecom import construct_param_cmd, construct_reset_cmd


def test_vs_float() -> None:
    # created with https://www.meerstetter.ch/MeCom/
    CMD = "#7BEF32VS03E8E641C8CCCDE2C1\r"
    cmd = construct_param_cmd(
        device_addr=123,
        cmd="VS",
        param_id=1000,
        value_type=float,
        value=25.1,
        param_inst=230,
        seq_num=61234,
    )
    assert cmd == CMD


def test_vr_float() -> None:
    # created with https://www.meerstetter.ch/MeCom/
    CMD = "#7BEF32?VR03E8E69AAD\r"
    cmd = construct_param_cmd(
        device_addr=123,
        cmd="?VR",
        param_id=1000,
        value_type=float,
        param_inst=230,
        seq_num=61234,
    )
    assert cmd == CMD


def test_vs_int() -> None:
    CMD = "#E6EA5FVS07E57B0000001958B0\r"
    cmd = construct_param_cmd(
        device_addr=230,
        cmd="VS",
        param_id=2021,
        value_type=int,
        value=25,
        param_inst=123,
        seq_num=59999,
    )
    assert cmd == CMD


def test_vr_int() -> None:
    CMD = "#E6EA5F?VR07E57BB3B5\r"
    cmd = construct_param_cmd(
        device_addr=230,
        cmd="?VR",
        param_id=2021,
        value_type=int,
        param_inst=123,
        seq_num=59999,
    )
    assert cmd == CMD


def test_reset() -> None:
    CMD = "#7B3039RSB5BB\r"
    cmd = construct_reset_cmd(device_addr=123, seq_num=12345)
    assert cmd == CMD
