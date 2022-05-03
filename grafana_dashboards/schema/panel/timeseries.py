import voluptuous as v

from grafana_dashboards.schema.panel.base import Base


class Timeseries(Base):
    threshold = {
        # means required/not optional, but can be `null`
        # `null` translates to -Infinity
        v.Required("value"): v.Any(None, v.Number()),
        v.Required("color"): str,
    }

    thresholds_config = {
        v.Required("mode"): v.Any("absolute", "percentage"),
        v.Required("steps"): [threshold],
    }

    field_color = {
        v.Required("mode"): v.Any(
            "thresholds",
            "palette-classic",
            "palette-saturated",
            "continuous-GrYlRd",
            "fixed",
        ),
        v.Optional("fixedColor"): str,
        v.Optional("seriesBy"): v.Any("min", "max", "last"),
    }

    line_config = {
        v.Optional("lineColor"): str,
        v.Optional("lineWidth"): v.Clamp(min=0, max=10),
        v.Optional("lineInterpolation"): v.Any(
            "linear",
            "smooth",
            "stepBefore",
            "stepAfter",
        ),
        v.Optional("lineStyle"): {
            v.Optional("fill"): v.Any("solid", "dash", "dot", "square"),
            v.Optional("dash"): [v.Number()],
        },
        v.Optional("spanNulls"): v.Any(bool, v.Number()),
    }

    fill_config = {
        v.Optional("fillColor"): str,
        v.Optional("fillOpacity"): v.Clamp(min=0, max=100),
        v.Optional("fillBelowTo"): str,
    }

    points_config = {
        v.Optional("showPoints"): v.Any("auto", "never", "always"),
        v.Optional("pointSize"): v.Number(),
        v.Optional("pointColor"): str,
        v.Optional("pointSymbol"): str,
    }

    axis_config = {
        v.Optional("axisPlacement"): v.Any(
            "auto", "top", "right", "bottom", "left", "hidden"
        ),
        v.Optional("axisLabel"): str,
        v.Optional("axisWidth"): v.Number(),
        v.Optional("axisSoftMin"): v.Number(),
        v.Optional("axisSoftMax"): v.Number(),
        v.Optional("axisGridShow"): bool,
        v.Optional("scaleDistribution"): {
            v.Required("type"): v.Any("linear", "log", "ordinal"),
            v.Optional("log"): v.Number(),
        },
    }

    bar_config = {
        v.Optional("barAlignment"): v.Any(-1, 0, 1),
        v.Optional("barWidthFactor"): v.Number(),
        v.Optional("barMaxWidth"): v.Number(),
    }

    stackable_field_config = {
        v.Optional("stacking"): {
            v.Optional("mode"): v.Any("none", "normal", "percent"),
            v.Optional("group"): str,
        },
    }

    hideable_field_config = {
        v.Optional("hideFrom"): {
            v.Required("tooltip"): bool,
            v.Required("legend"): bool,
            v.Required("viz"): bool,
        },
    }

    # Following https://github.com/grafana/grafana/blob/v8.5.0/packages/grafana-schema/src/schema/graph.cue
    graph_field_config = {
        **line_config,
        **fill_config,
        **points_config,
        **axis_config,
        **bar_config,
        **stackable_field_config,
        **hideable_field_config,
        v.Optional("drawStyle"): v.Any("line", "bars", "points"),
        v.Optional("gradientMode"): v.Any("none", "opacity", "hue", "scheme"),
        v.Optional("thresholdsStyle"): {
            v.Required("mode"): v.Any("off", "line", "area", "line+area", "series"),
        },
        v.Optional("transform"): v.Any("constant", "negative-Y"),
    }

    def get_schema(self):
        timeseries = {
            **Base.datasource,
            **Base.grid_pos,
            v.Required("fieldConfig", default={"defaults": {}}): {
                v.Required("defaults", default={}): {
                    v.Optional("displayName"): str,
                    v.Optional("unit"): Base.formats,
                    v.Optional("decimals"): v.All(int, v.Clamp(min=0)),
                    v.Optional("min"): v.Number(),
                    v.Optional("max"): v.Number(),
                    # TODO: Grafana hasn't defined a proper schema yet
                    # See https://github.com/grafana/grafana/blob/v8.5.0/packages/grafana-schema/src/scuemata/dashboard/dashboard.cue#L265-L274
                    v.Optional("mappings"): list,
                    v.Optional("thresholds"): __class__.thresholds_config,
                    v.Optional("color"): __class__.field_color,
                    v.Optional("links"): list,
                    v.Optional("noValue"): str,
                    v.Optional("custom"): __class__.graph_field_config,
                },
                v.Required("overrides", default=[]): [
                    {
                        v.Required("matcher"): {
                            v.Required("id", default=""): str,
                            v.Optional("options"): v.All(),
                        },
                        v.Required("properties"): [
                            {
                                v.Required("id", default=""): str,
                                v.Optional("value"): v.All(),
                            }
                        ],
                    }
                ],
            },
            v.Optional("links"): list,
            v.Required("options", default={}): {
                **Base.options_with_legend,
                **Base.options_with_tooltip,
                **Base.options_with_text_formatting,
            },
            # TODO: Grafana hasn't defined a proper schema yet
            # See https://github.com/grafana/grafana/blob/v8.5.0/packages/grafana-schema/src/scuemata/dashboard/dashboard.cue#L164
            v.Optional("targets"): list,
        }
        timeseries.update(self.base)

        # FIXME: this is smelly
        del timeseries["span"]

        return v.Schema(timeseries, extra=v.PREVENT_EXTRA)
