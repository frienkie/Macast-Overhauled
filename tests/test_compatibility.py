import errno
import json
from unittest.mock import Mock

import pytest
import macast
from macast_renderer.mpv import MPVRenderer, ObserveProperty
from macast.utils import Setting
from macast.ssdp import SSDPServer


@pytest.mark.parametrize('version,index', [((0, 34), False), ((0, 38), True), ((0, 40), True), ((1, 0), True)])
def test_loadfile_with_start_and_signed_audio(monkeypatch, version, index):
    monkeypatch.setattr(Setting, 'get', lambda key, default=None: default)
    renderer = object.__new__(MPVRenderer)
    renderer.mpv_version = version
    renderer.separate_danmaku = False  # Exercise legacy loadfile options without __init__.
    renderer.send_command = Mock()
    audio = 'https://cdn.example/audio.m4s?token=a,b&expires=123'
    renderer.set_media_url_options('https://cdn.example/video.m4s', 42,
                                   {'audio-files': audio, 'referrer': 'https://www.bilibili.com/'})
    command = renderer.send_command.call_args.args[0]
    assert command[:3] == ['loadfile', 'https://cdn.example/video.m4s', 'replace']
    if index:
        assert command[3] == -1
    assert len(command) == (5 if index else 4)
    assert command[-1]['start'] == '42'
    assert command[-1]['audio-files'] == audio
    assert 'start' not in renderer.media_options


def test_version_notification():
    renderer = object.__new__(MPVRenderer)
    renderer.update_state(json.dumps({'id': ObserveProperty.mpv_version.value, 'data': 'mpv 0.40.0'}))
    assert renderer.mpv_version == (0, 40)


def test_permission_retry_recovers_without_restart(monkeypatch):
    server = SSDPServer()
    server.sock = Mock()
    server.pending_memberships = ['192.168.1.2']
    server.sock.setsockopt.side_effect = [PermissionError(errno.EACCES, 'denied'), None]
    make_socket = Mock()
    monkeypatch.setattr('macast.ssdp.Sock', make_socket)
    server.retry_memberships()
    assert server.pending_memberships == ['192.168.1.2']
    assert server.sock_list == []
    server.retry_memberships()
    assert server.pending_memberships == []
    assert server.sock_list == [make_socket.return_value]
