"""App-local MPV UI assets and conservative launch options."""

from macast.bundled_plugins import bundle_directory


def player_ui_options(scale=1.0):
    try:
        scale = min(2.0, max(0.75, float(scale)))
    except (TypeError, ValueError):
        scale = 1.0
    root = bundle_directory().parent / 'mpv_ui'
    script = root / 'scripts/modernz'
    if not (script / 'main.lua').is_file():
        return ['--script-opts=osc-timetotal=yes,osc-layout=bottombar,'
                'osc-title=${title},osc-visibility=auto,osc-scalewindowed=1.3,'
                'osc-scalefullscreen=1.5']
    options = ['--osc=no', '--script={}'.format(script),
               '--osd-fonts-dir={}'.format(root / 'fonts'),
               '--secondary-sub-ass-override=no']
    for line in (root / 'modernz.conf').read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=', 1)
        options.append('--script-opts-append=modernz-{}={}'.format(key, value))
    options.append('--script-opts-append=modernz-macast_ui_scale={}'.format(float(scale)))
    return options
