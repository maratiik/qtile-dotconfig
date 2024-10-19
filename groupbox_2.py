# vim: ai:ts=4:sw=4:fenc=utf-8
from libqtile.widget.groupbox import GroupBox
from libqtile.log_utils import logger
from copy import copy, deepcopy

class BoxStyle:
    """Represents a highlight style for the GroupBox2 widget's elements."""

    attrs = ["text_color", "background_color", "rounded", "border", "border_color", "line", "line_color", "line_size"]

    text_color = None
    background_color = None
    rounded = None
    border = None
    border_color = None
    line = None
    line_color = None
    line_size = None

    def __init__(self, **config):
        for name in BoxStyle.attrs:
            self.__setattr__(name, config[name] if name in config else None)

    def __repr__(self):
        b = f" Border({self.border_color}, {self.border_size})"
        l = f" Line({self.line_color}, {self.line_size}, {self.line_length})"
        return "BoxStyle({}, {}, {}){}{}".format(
            self.text_color, self.background_color, "rounded" if self.rounded else "sharp",
            b if self.border_active else "",
            l if self.line_active else ""
        )


    def combine(self, other):
        """Returns a copy of this instance updated with non-None values from the other instance."""
        if other is None:
            return copy(self)

        result = BoxStyle()

        for name in BoxStyle.attrs:
            o = getattr(other, name)
            result.__setattr__(name, getattr(self, name) if o is None else o)

        return result


    def get_default():
        """Returns a new instance with all attributes set."""
        return BoxStyle(
            text_color = "#ffffff",
            background_color = None,
            rounded = False,
            border = 0,
            border_color = None,
            line = 0,
            line_color = None,
            line_size = 1
        )


class GroupBox2(GroupBox):
    defaults = [
        (
            "transform_label",
            None,
            "If this function is set, its result is used in place of the group's label;"
            "if None (default), the group's label is used directly."
        ),
        (
            "normal_style",
            None,
            "The BoxStyle applied to all groups regardless of highlighting."
        ),
        (
            "has_windows_style",
            None,
            "The BoxStyle applied to groups that contain windows."
        ),
        (
            "active_any_screen_style",
            None,
            "The BoxStyle applied to groups that are active on any screens."
        ),
        (
            "active_own_screen_style",
            None,
            "The BoxStyle applied to groups that are active on the screens where the widgets are located."
        ),
        (
            "active_current_screen_style",
            None,
            "The BoxStyle applied to the single group that is active on the screen that has the focus."
        ),
        (
            "urgent_style",
            None,
            "The BoxStyle applied to groups that have urgent windows."
        )
    ]

    def __init__(self, **config):
        GroupBox.__init__(self, **config)
        self.add_defaults(GroupBox2.defaults)

        self.styles = dict()
        for name in config:
            if name.endswith("_style"):
                if config[name] is None:
                    self.styles[name] = BoxStyle()

                if not isinstance(config[name], dict):
                    raise TypeError

                self.styles[name] = BoxStyle(**config[name])

    def get_style(self, name):
        if name in self.styles:
            return deepcopy(self.styles[name])

    def combine_styles(self):
        text_color = None
        border_active = False
        border_color = None
        border_size = None

    def box_width(self, groups):
        if self.transform_label is None:
            return GroupBox.box_width(self, groups)

        width, _ = self.drawer.max_layout_size(
            [self.fmt.format(self._execute_transform_label(i)) for i in groups], self.font, self.fontsize
        )
        return width + self.padding_x * 2 + self.borderwidth * 2

    def _execute_transform_label(self, group):
        has_windows = bool(group.windows)
        active_any = bool(group.screen)
        active_own = self.bar.screen.group.name == group.name
        active_current = active_own and self.qtile.current_screen == self.bar.screen
        urgent = self.group_has_urgent(group)

        return group.label if self.transform_label is None else self.transform_label(
            group,
            has_windows,
            active_any,
            active_own,
            active_current,
            urgent
        )

    def drawbox_new(
            self,
            offset,
            text,
            style,
            box_width = None,
            ):

        x = offset
        layout = self.layout
        drawer = self.layout.drawer

        self.layout.text = self.fmt.format(text)
        self.layout.font_family = self.font
        self.layout.font_size = self.fontsize
        self.layout.colour = style.text_color

        if box_width is not None:
            self.layout.width = box_width

        if style.border > 0:
            border_width = style.border
            framecolor = style.border_color
        else:
            border_width = 0
            framecolor = self.background or self.bar.background

        y = self.margin_y

        # Draw block
        if style.background_color is not None:
            drawer.set_source_rgb(style.background_color)
            opts = [x, y, layout.width, layout.height + self.padding_y * 2, border_width]
            if style.rounded:
                drawer.rounded_fillrect(*opts)
            else:
                drawer.fillrect(*opts)

        # Draw border
        if style.border > 0:
            drawer.set_source_rgb(style.border_color or style.text_color)
            opts = [x, y, layout.width, layout.height + self.padding_y * 2, border_width]
            if style.rounded:
                drawer.rounded_rectangle(*opts)
            else:
                drawer.rectangle(*opts)

        # Draw line
        if style.line > 0:
            line_width = layout.width * style.line_size
            line_x = x + (layout.width - line_width) / 2
            drawer.set_source_rgb(style.line_color or style.text_color)
            opts = [line_x, layout.height + self.padding_y * 2 - style.line, line_width, style.line, border_width]
            drawer.fillrect(*opts)

        # Draw the text
        drawer.ctx.stroke()
        layout.draw(x, y + self.padding_y)

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = self.margin_x

        for i, g in enumerate(self.groups):
            active_style = BoxStyle.get_default().combine(self.get_style("normal_style"))
            active_name = "normal"

            has_windows = bool(g.windows)
            active_any = bool(g.screen)
            active_own = self.bar.screen.group.name == g.name
            active_current = active_own and self.qtile.current_screen == self.bar.screen
            urgent = self.group_has_urgent(g)

            bw = self.box_width([g])

            if has_windows: # The group has at least one windows, regardless of focus
                active_style = active_style.combine(self.get_style("has_windows_style"))

            if active_any:  # The group is active on any screen
                active_style = active_style.combine(self.get_style("active_any_screen_style"))

            if active_own:  # The group is active on the screen where the widget is located
                active_style = active_style.combine(self.get_style("active_own_screen_style"))

            if active_current:  # The group is active on the screen that has the focus
                active_style = active_style.combine(self.get_style("active_current_screen_style"))

            if urgent:  # The group has at least one window with the urgent hint
                active_style = active_style.combine(self.get_style("urgent_style"))

            self.drawbox_new(
                offset,
                g.label if self.transform_label is None else self._execute_transform_label(g),
                active_style,
                bw
            )

            offset += bw + self.spacing
        self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)
