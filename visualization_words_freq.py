import pygal
import pygal.style
from pygal.style import Style

import json

# To be frank, this code is bad.
# /ufe0f is a variant selector (choose color for same kind of emoji). That's why there are so many of it
# Yeah, those things that only occur once or less, ah they don't matter in the grand scheme of the project
# I'm just gonna list the things I don't have time to do as flaws...

TITLE_LIST = ("words", "emotes", "emojis")


def prepare_values(freq: dict):
    x_labels = []
    y_values = []
    total_com = sum(list(freq.values()))
    print(total_com)
    number_o_bars = 20
    num_unique_ele = len(list(freq.keys())) - number_o_bars
    for key, value in freq.items():
        x_labels.append(key)
        y_values.append(value)
        number_o_bars -= 1
        if number_o_bars == 0:
            break
    return x_labels, y_values, total_com, num_unique_ele


def bar_chart_pygal(x_values: list, total, index: int, name: str, chart_colors: list, tooltips, words_only=""):
    config = pygal.Config(
        x_label_rotation=0,
        show_legend=False,
        show_y_guides=False,
        width=1000,
        height=600,
    )

    weird_style = Style(
        background='black',
        plot_background="#121212",
        foreground=f"{chart_colors[0]}",  # Main color of other ticks
        foreground_strong=f"{chart_colors[1]}",  # Gridline color (Major ticks)
        foreground_subtle="#ff69b4",
        colors=[f"{chart_colors[2]}"],  # Data series colors
    )

    title = TITLE_LIST[index]
    chart = pygal.Bar(config=config, style=weird_style, dynamic_print_values=True)
    chart.title = f"Top 20 most common {words_only}{title}\nout of {total} commented {title} " \
                  f"in 30 of {name.title()}'s streams"
    chart.x_labels = x_values
    chart.x_title = f"{title.title()}"
    chart.y_title = f"Frequency of {title.title()}"
    chart.add("", tooltips)
    chart.render_in_browser()
    chart.render_to_file(f"svg_graphs/{name}_{title}_bar_chart.svg")
    chart.render_to_png(f"png_graphs/{name}_{title}_bar_chart.png")


def bar_pygal_tooltips(x_values: list, y_values: list):
    custom_tooltip = []
    for index in range(len(x_values)):
        custom_tooltip_dict = {"value": y_values[index], "label": x_values[index]}
        custom_tooltip.append(custom_tooltip_dict)
    return custom_tooltip


def pie_chart_pygal(x_values: list, y_values: list, total, index: int,
                    name: str, chart_colors: list, num_unique_ele, words_only=""):
    pie_fig = pygal.Config(
        width=1000,
        height=600,
    )

    pie_style = Style(
        background='#121212',
        plot_background="#323232",
        foreground=f"{chart_colors[0]}",  # Main color of other ticks
        foreground_strong=f"{chart_colors[1]}",  # Gridline color (Major ticks)
        foreground_subtle="#ff69b4",
    )
    sum_rest = total - sum(y_values)
    title = TITLE_LIST[index]
    piegal = pygal.Pie(config=pie_fig, style=pie_style, inner_radius=.3)
    for i in range(len(x_values)):
        piegal.add(x_values[i], y_values[i])

    # Add the value of the rest of the elements
    piegal.add(f"The rest of {num_unique_ele} {title}", sum_rest)
    piegal.title = f"The number of comments of top 20 most commented {words_only}{title} in\n{total} " \
                   f"commented {title} in total in 30 of {name.title()}'s streams"
    piegal.render_in_browser()
    piegal.render_to_file(f"svg_graphs/{name}_{title}_pie_chart.svg")
    piegal.render_to_png(f"png_graphs/{name}_{title}_pie_chart.png")


def second_pie_pygal(y_values: list, total, index: int, name: str,
                     chart_colors: list, num_unique_ele, words_only=""):
    # The second pie graph...
    pie_fig = pygal.Config(
        width=1000,
        height=600,
    )

    second_pie_style = Style(
        background='#121212',
        plot_background="#323232",
        foreground=f"{chart_colors[0]}",  # Main color of other ticks
        foreground_strong=f"{chart_colors[1]}",  # Gridline color (Major ticks)
        foreground_subtle="#ff69b4",
        colors=("#ffffff", "#000000")
    )
    sum_rest = total - sum(y_values)
    title = TITLE_LIST[index]
    top_rest = pygal.Pie(config=pie_fig, style=second_pie_style, inner_radius=.3)
    top_rest.add("Top 20 comments", sum(y_values))
    top_rest.add(f"The rest of {num_unique_ele} {title}", sum_rest)
    top_rest.title = f"The number of comments of top 20 most commented {words_only}{title} vs the rest of the chart" \
                     f"\nin {total} commented {title} in 30 of {name.title()}'s streams"
    top_rest.render_in_browser()
    top_rest.render_to_file(f"svg_graphs/{name}_{title}_top_rest_pie_chart.svg")
    top_rest.render_to_png(f"png_graphs/{name}_{title}_top_rest_pie_chart.png")


def streamers_file_extraction(streamer):
    path = f"{streamer}_elements_freq.json"
    with open(file=path) as f:
        woawoawoawoa = json.load(f)
    words_freq = woawoawoawoa["words_freq"]
    emotes_freq = woawoawoawoa["emotes_freq"]
    emoji_freq = woawoawoawoa["emoji_freq"]
    freq_list = [words_freq, emotes_freq, emoji_freq]
    color_palettes_list = [
        ["#765898", "#ff8c28", "#39ff14"],
        ["#ec2323", "#fbe5e5", "#ea8532"],
        ["#1d446c", "#00FFFF", "#8f3232"]
    ]
    return freq_list, color_palettes_list


def generate_graphs(freq_list: list, palettes, name, i):
    x_y_total_unique_types = prepare_values(freq=freq_list[i])
    x_values_types = x_y_total_unique_types[0]
    y_values_types = x_y_total_unique_types[1]
    total_types = x_y_total_unique_types[2]
    num_unique_types_left = x_y_total_unique_types[3]
    tooltips_types = bar_pygal_tooltips(x_values=x_values_types, y_values=y_values_types)
    bar_chart_pygal(x_values_types, total=total_types, index=i, name=name,
                    chart_colors=palettes[i], tooltips=tooltips_types)
    pie_chart_pygal(x_values_types, y_values_types,
                    total=total_types, index=i, name=name, chart_colors=palettes[i],
                    num_unique_ele=num_unique_types_left)
    second_pie_pygal(y_values_types, total=total_types, index=i, name=name,
                     chart_colors=palettes[i], num_unique_ele=num_unique_types_left)


def main():
    streamers_list = ["amelia", "kiara"]

    for streamer_name in streamers_list:
        print(f"Drawing charts for {streamer_name.title()}...")
        freq_color = streamers_file_extraction(streamer_name)
        freq_list = freq_color[0]
        palettes = freq_color[1]

        # Generate graphs for words, emotes, and emojis frequency list.
        for i in range(0, len(freq_list)):
            generate_graphs(freq_list, palettes, streamer_name, i)
    return


if __name__ == '__main__':
    main()
