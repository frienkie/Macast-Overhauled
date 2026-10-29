import importlib.util
import json
import socket
import struct
import threading
import queue
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit

import pytest

spec = importlib.util.spec_from_file_location('nirvana', Path(__file__).resolve().parents[1] / 'nirvana/nirvana.py')
nva = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nva)


@pytest.fixture
def handler(monkeypatch):
    renderer, protocol = Mock(), Mock()
    renderer.set_media_url.__func__ = nva.MPVRenderer.set_media_url
    protocol.get_state_speed.return_value = '1'
    monkeypatch.setattr(nva.NVAConectionHandler, 'renderer', property(lambda self: renderer))
    monkeypatch.setattr(nva.NVAConectionHandler, 'protocol', property(lambda self: protocol))
    obj = nva.NVAConectionHandler(Mock(), SimpleNamespace(headers={'Session': 'test', 'UUID': 'phone'}))
    obj.send_res = Mock()
    return obj


def response(monkeypatch, data):
    monkeypatch.setattr(nva.NetworkManager, 'GET', lambda *a, **k: SimpleNamespace(text=json.dumps({'code': 0, 'data': data})))


@pytest.mark.parametrize('field,payload,url', [
    ('durl', [{'url': 'https://cdn.example/video.flv'}], 'https://cdn.example/video.flv'),
    ('live_mobile', {'stream': 'https://cdn.example/live.m3u8'}, 'https://cdn.example/live.m3u8'),
    ('live_stream', {'flv': ['https://cdn.example/live.flv']}, 'https://cdn.example/live.flv'),
])
def test_optional_fields_do_not_block_other_streams(monkeypatch, handler, field, payload, url):
    response(monkeypatch, {field: payload})
    assert handler.get_video_url()[0] == url


def test_dash_uses_selected_quality_and_audio(monkeypatch, handler):
    response(monkeypatch, {'quality': 80, 'dash': {
        'video': [{'id': 64, 'base_url': 'https://cdn.example/720'}, {'id': 80, 'baseUrl': 'https://cdn.example/1080'}],
        'audio': [{'bandwidth': 10, 'base_url': 'https://cdn.example/a'}, {'bandwidth': 20, 'baseUrl': 'https://cdn.example/b'}]}})
    assert handler.get_video_url()[0] == 'https://cdn.example/1080'
    assert handler.audio_url == 'https://cdn.example/b'
    # Keep this unit test independent of background metadata downloads.
    handler.playurl_type = 4
    handler.send_play_cmd('https://cdn.example/1080')
    args = handler.renderer.set_media_url_options.call_args.args
    assert args[2]['audio-files-append'] == 'https://cdn.example/b'
    assert args[2]['referrer'] == 'https://www.bilibili.com/'


def test_empty_result_does_not_load_none(handler):
    handler.send_play_cmd(None)
    handler.renderer.set_media_url.assert_not_called()
    handler.renderer.set_media_url_options.assert_not_called()
    handler.protocol.set_state_transport_error.assert_called_once()


def test_custom_player_keeps_its_startup_method(handler):
    handler.renderer.set_media_url.__func__ = lambda: None
    handler.playurl_type = 4
    handler.send_play_cmd('https://cdn.example/live.flv')
    handler.renderer.set_media_url.assert_called_once_with('https://cdn.example/live.flv', '0')
    handler.renderer.set_media_url_options.assert_not_called()


def test_custom_player_rejects_dash_without_silent_audio_loss(handler):
    handler.renderer.set_media_url.__func__ = lambda: None
    handler.audio_url = 'https://cdn.example/audio'
    handler.send_play_cmd('https://cdn.example/video')
    handler.renderer.set_media_url.assert_not_called()
    handler.protocol.set_state_transport_error.assert_called_once()


@pytest.mark.parametrize('value,expected', [(False, False), ('false', False), ('0', False), (True, True), ('true', True), (1, True)])
def test_danmaku_boolean(handler, value, expected):
    handler.cmd_from_client('SwitchDanmaku', 1, {'open': value})
    handler.renderer.set_media_danmaku_show.assert_called_once_with(expected)
    handler.protocol.set_state_display_subtitle.assert_called_once_with(expected)


def test_play_url_without_extension(handler):
    handler.send_play_cmd = Mock()
    handler.audio_url = 'old audio'
    handler.cmd_from_client('PlayUrl', 1, {'url': 'https://cdn.example/v.mp4', 'seekTs': 12},
                            _playback_worker=True)
    handler.send_play_cmd.assert_called_once_with('https://cdn.example/v.mp4', start=12)
    assert handler.audio_url is None


def test_signing_roundtrips_encoded_token(monkeypatch):
    get = Mock(return_value=Mock())
    monkeypatch.setattr(nva.requests, 'get', get)
    nva.NetworkManager.GET('https://api.bilibili.com/x/tv/playurl?access_key=a%2Bb%3Dc&cid=1', sign=True)
    query = parse_qs(urlsplit(get.call_args.args[0]).query)
    assert query['access_key'] == ['a+b=c']
    assert len(query['sign'][0]) == 32
    assert get.call_args.kwargs['timeout'] == (5, 15)


def test_fragmented_and_combined_commands():
    obj = nva.NVAConectionBaseHandler(Mock(), SimpleNamespace(headers={}))
    obj.cmd_from_client = Mock()
    method = b'Pause'
    frame = struct.pack('>cBI2B7sB5s', nva.SEND_CMD, 2, 7, 1, 7, nva.COMMAND, len(method), method)
    for byte in frame[:-1]:
        obj.parse_request(bytes([byte]))
    obj.cmd_from_client.assert_not_called()
    obj.parse_request(frame[-1:] + frame)
    assert obj.cmd_from_client.call_count == 2
    assert obj.cache == b''


def test_terminate_before_start_is_safe():
    obj = nva.NVAConectionBaseHandler(Mock(), SimpleNamespace(headers={}))
    obj.terminate()
    assert obj.terminated


def test_reconnect_when_os_reuses_descriptor():
    protocol = object.__new__(nva.NVAProtocol)
    protocol.lock = threading.Lock()
    protocol.poller = nva.SelectPoller()
    old = Mock(uuid='phone', session='session', cache=b'partial', counter=10)
    old.sock = None
    protocol.clients = {42: old}
    protocol.poller.register(42)
    new = SimpleNamespace(uuid='phone', session='session', sock=Mock())
    new.sock.fileno.return_value = 42
    protocol.add(new)
    assert protocol.clients == {42: old}
    assert protocol.poller._fds == [42]
    assert old.cache == b''
    old.start.assert_called_once()


def test_heartbeat_thread_exits_promptly():
    server, client = socket.socketpair()
    obj = nva.NVAConectionBaseHandler(server, SimpleNamespace(headers={}))
    try:
        obj.start()
        obj.terminate()
        assert not obj.ping_thread.is_alive()
    finally:
        client.close()


def test_real_nva_handshake_retains_socket(monkeypatch):
    cherrypy = nva.cherrypy
    monkeypatch.setattr(nva.Setting, 'get_usn', lambda: 'receiver-test')
    received = queue.Queue()

    @cherrypy.expose
    class Endpoint:
        @cherrypy.tools.nva()
        def SETUP(self, p):
            return b''

    def added(handler):
        received.put(handler)

    cherrypy.config.update({'environment': 'test_suite', 'server.socket_host': '127.0.0.1',
                            'server.socket_port': 0, 'engine.autoreload.on': False,
                            'log.screen': False})
    cherrypy.tree.mount(Endpoint(), '/', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
    cherrypy.server.httpserver = nva.NVAHTTPServer(cherrypy.server)
    cherrypy.engine.subscribe('nva-add', added)
    client = handler = None
    try:
        cherrypy.engine.start()
        client = socket.create_connection(cherrypy.server.bound_addr, timeout=5)
        client.sendall(b'SETUP /projection NVA/1.0\r\nSession: test\r\nUUID: phone\r\nContent-Length: 0\r\n\r\n')
        response = b''
        while b'\r\n\r\n' not in response:
            response += client.recv(4096)
        assert response.startswith(b'NVA/1.0 200'), response
        handler = received.get(timeout=5)
        client.sendall(b'next command')
        handler.sock.settimeout(5)
        assert handler.sock.recv(12) == b'next command'
    finally:
        if handler:
            handler.terminate()
        if client:
            client.close()
        cherrypy.engine.exit()
        cherrypy.engine.unsubscribe('nva-add', added)
