# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from groupbox_2 import GroupBox2

mod = "mod4"
terminal = "alacritty"
wallpaper = "/home/maratik/Images/Wallpapers/wallpaperflare.com_wallpaper.jpg"
colors = {
    "ON_1": "ffb23b",
    "ON_2": "cf7e00",
    "ON_3": "613b00",
    "ON_4": "291900",
    "OFF_1": 'ffffff',
    "OFF_2": "c3c3c3",
    "OFF_3": "757575",
    "OFF_4": "000000",
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    # Volume
    Key([], 'XF86AudioRaiseVolume', lazy.widget['volume'].increase_vol()),
    Key([], 'XF86AudioLowerVolume', lazy.widget['volume'].decrease_vol()),
    Key([], 'XF86AudioMute', lazy.widget['volume'].mute()),
    # Keyboard layout
    # Key([mod], 'Space', lazy.widget())
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus=colors['ON_2'],
        border_normal=colors['ON_3'],
        border_on_single=True,
        border_width=2,
        ),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper=wallpaper,
        wallpaper_mode='fill',
        bottom=bar.Bar(
            [
                GroupBox2(
                    highlight_method='line',
                    hide_unused=True,
                    margin_x=7,
                    padding_y=5,
                    active_current_screen_style={
                        "text_color": colors['ON_2'],
                        "line_color": colors['ON_2'],
                        'line': 1,
                    },
                    active_own_screen_style={
                        'text_color': colors['ON_3'],
                        'line_color': colors['ON_3'],
                        'line': 1
                    },
                    active_any_screen_style={
                        'text_color': colors['ON_3']
                    },
                    has_windows_style={
                        'text_color': colors['ON_3']
                    },
                    normal_style={
                        'text_color': colors['ON_3']
                    },
                    urgent_style={
                        'text_color': colors['ON_3'],

                    }
                ),
                widget.TaskList(
                    highlight_method='block',
                    border=colors['ON_2'],
                    rounded=False,
                    icon_size=15,
                    margin_y=-3,
                    padding_y=10,
                    urgent_border=colors['ON_1'],
                    max_title_width=150,
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Clock(format="%A %-d.%-m.%Y"),
                widget.Spacer(),
                widget.Systray(),
                widget.Volume(
                    fmt="🎵{}",
                    mute_format='x',
                ),
                widget.Battery(
                    format='⚡︎{char}{percent:1.0%}',
                    full_char='',
                    show_short_text=False
                ),
                widget.Clock(format="%H:%M"),
                widget.Spacer(
                    length=7
                )
            ],
            30,
            border_width=[2, 0, 0, 0],  # Draw top and bottom borders
            border_color=[colors['ON_2'], "000000", "000000", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        wallpaper=wallpaper,
        wallpaper_mode='fill',
        bottom=bar.Bar(
            [
                GroupBox2(
                    highlight_method='line',
                    hide_unused=True,
                    margin_x=7,
                    padding_y=5,
                    active_current_screen_style={
                        "text_color": colors['ON_2'],
                        "line_color": colors['ON_2'],
                        'line': 1,
                    },
                    active_own_screen_style={
                        'text_color': colors['ON_3'],
                        'line_color': colors['ON_3'],
                        'line': 1
                    },
                    active_any_screen_style={
                        'text_color': colors['ON_3']
                    },
                    has_windows_style={
                        'text_color': colors['ON_3']
                    },
                    normal_style={
                        'text_color': colors['ON_3']
                    }
                ),
                widget.TaskList(
                    highlight_method='block',
                    border=colors['ON_2'],
                    rounded=False,
                    icon_size=15,
                    margin_y=-3,
                    padding_y=10,
                    urgent_border=colors['ON_1'],
                    max_title_width=150,
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Clock(format="%A %-d.%-m.%Y"),
                widget.Spacer(),
                # widget.KeyboardLayout(
                #     configured_keyboards=['us', 'ru'],
                #     display_map={'us': 'US', 'ru': 'RU'}
                # ),
                widget.Volume(
                    fmt="🎵{}",
                    mute_format='x'
                ),
                widget.Battery(
                    format='⚡︎{char}{percent:1.0%}',
                    full_char='',
                    show_short_text=False
                ),
                widget.Clock(format="%H:%M"),
                widget.Spacer(
                    length=7
                )
            ],
            30,
            border_width=[2, 0, 0, 0],  # Draw top and bottom borders
            border_color=[colors['ON_2'], "000000", "000000", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Run some autostart scripts
import os
import subprocess

@hook.subscribe.startup
def run_every_startup():
    kb_layouts_script = os.path.expanduser('~/.config/qtile/kb_layouts.sh')
    subprocess.call([kb_layouts_script])