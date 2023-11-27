""" Implementation of various simplifying factories for generating layouts.
"""

# Zool modules.
import zool.core


def vertical_stack(heights, labels=None, **kwargs):
    """This function returns a standard vertical stack of panels.

    Additional keyword arguments are passed straight through to the Plot class
    constructor.

    Args:
    :param heights list: List of panel heights (in cm).
    :param labels list: Optional list of panel labels.
    :return Zool figure object: Plot layout.
    """
    fig = zool.Figure(
        figheight=zool.core.FromChildren(), layout="vertical", **kwargs
    )
    for i in range(len(heights)):
        if labels is None:
            fig.add(
                "base",
                width=zool.core.FromParent(),
                height=zool.core.Fixed(heights[i]),
                label=str(i),
            )
        else:
            fig.add(
                "base",
                width=zool.core.FromParent(),
                height=zool.core.Fixed(heights[i]),
                label=labels[i],
            )

    fig.layout()
    return fig


def triangle(vars, d2d=4.0, d1d=1.0, m_padding=0.2, t_padding=0.1, **kwargs):
    """This function returns a triangle plot of panels.

    Additional keyword arguments are passed straight through to the
    Figure class constructor.

    Args:
    :param n int: Number of variables to plot in the triangle (n x n).
    :param d2d float: Dimension of the (square) 2d histograms.
    :param d1d float: Dimension of the 1d marginals.
    :param m_padding float: Padding between vertical panels (cm).
    :param t_padding float: Padding between panels in each vertical set (cm).
    :return Zool figure object: Plot layout.
    """

    fig = zool.Figure(
        figwidth=zool.core.FromChildren(),
        figheight=zool.core.Named("tleft-frame"),
        layout="horizontal",
        padding=m_padding,
        **kwargs,
    )
    n = len(vars)

    # Setup the vertical frames that will hold all the histograms. The
    # arrangement is for a left-hand frame to hold the marginals for each
    # horizontal row plus (n+1) vertical frames to hold the n variables.
    fig.add(
        "base",
        width=zool.core.Fixed(d1d),
        height=zool.core.FromChildren(),
        layout="vertical",
        padding=t_padding,
        label="tleft-frame",
    )
    for i in range(n - 1):
        fig.add(
            "base",
            width=zool.Fixed(d2d),
            height=zool.core.FromChildren(),
            layout="vertical",
            padding=t_padding,
            label="t{:1d}-frame".format(i + 1),
        )

    # Add marginal histograms to the left-hand frame, including some padding at
    # the top for alignment.
    fig.add(
        "tleft-frame", width=zool.core.FromParent(), height=zool.Fixed(d1d)
    )
    # 				label='{:1d}-top-padding'.format(i+1))
    for i in range(n - 1, 0, -1):
        fig.add(
            "tleft-frame",
            width=zool.core.FromParent(),
            height=zool.Fixed(d2d),
            label="{}-1d-v".format(vars[i]),
        )

    # Add 1D marginal and 2D histograms in the other frames.
    varindex = [0] + list(range(n - 1, 1, -1))
    for i in range(n - 1):
        frame = "t{:1d}-frame".format(i + 1)
        k = varindex[i]

        # Add padding at the top for alignment.
        for j in range(i):
            fig.add(
                frame, width=zool.core.FromParent(), height=zool.Fixed(d2d)
            )
        # 				label='{:1d}-{:1d}-padding'.format(i+1,j+1))

        # Add 1d marginal at the top of the column.
        fig.add(
            frame,
            width=zool.core.FromParent(),
            height=zool.Fixed(d1d),
            label="{}-1d-h".format(vars[k]),
        )

        # Add 2d histograms.
        for j in range(n - 1 - i, 0, -1):
            fig.add(
                frame,
                width=zool.core.FromParent(),
                height=zool.Fixed(d2d),
                label="{}-{}-2d".format(vars[k], vars[j]),
            )

    # Finish the layout and make the figure.
    fig.layout()

    return fig


def triangle_equal(
    vars, figwidth, d1d=1.0, m_padding=0.2, t_padding=0.1, **kwargs
):
    """This function returns a triangle plot of panels.

    Additional keyword arguments are passed straight through to the
    Figure class constructor.

    Args:
    :param n int: Number of variables to plot in the triangle (n x n).
    :param d1d float: Dimension of the 1d marginals.
    :param m_padding float: Padding between vertical panels (cm).
    :param t_padding float: Padding between panels in each vertical set (cm).
    :return Zool figure object: Plot layout.
    """

    fig = zool.Figure(
        figwidth=figwidth,
        figheight=zool.core.Named("tleft-frame"),
        layout="horizontal",
        padding=m_padding,
        **kwargs,
    )
    n = len(vars)

    # Setup the vertical frames that will hold all the histograms. The
    # arrangement is for a left-hand frame to hold the marginals for each
    # horizontal row plus (n+1) vertical frames to hold the n variables.
    fig.add(
        "base",
        width=zool.core.Fixed(d1d),
        height=zool.core.FromChildren(),
        layout="vertical",
        padding=t_padding,
        label="tleft-frame",
    )
    for i in range(n - 1):
        fig.add(
            "base",
            width=zool.core.Fill(),
            height=zool.core.FromChildren(),
            layout="vertical",
            padding=t_padding,
            label="t{:1d}-frame".format(i + 1),
        )

    # Add marginal histograms to the left-hand frame, including some padding at
    # the top for alignment.
    fig.add(
        "tleft-frame", width=zool.core.FromParent(), height=zool.Fixed(d1d)
    )
    # 				label='{:1d}-top-padding'.format(i+1))
    for i in range(n - 1, 0, -1):
        fig.add(
            "tleft-frame",
            width=zool.core.FromParent(),
            height=zool.Named("{}-{}-2d".format(vars[0], vars[1])),
            label="{}-1d-v".format(vars[i]),
        )

    # Add 1D marginal and 2D histograms in the other frames.
    varindex = [0] + list(range(n - 1, 1, -1))
    for i in range(n - 1):
        frame = "t{:1d}-frame".format(i + 1)
        k = varindex[i]

        # Add padding at the top for alignment.
        for j in range(i):
            fig.add(
                frame,
                width=zool.core.FromParent(),
                height=zool.FixedAspect(1.0),
            )
        # 				label='{:1d}-{:1d}-padding'.format(i+1,j+1))

        # Add 1d marginal at the top of the column.
        fig.add(
            frame,
            width=zool.core.FromParent(),
            height=zool.Fixed(d1d),
            label="{}-1d-h".format(vars[k]),
        )

        # Add 2d histograms.
        for j in range(n - 1 - i, 0, -1):
            fig.add(
                frame,
                width=zool.core.FromParent(),
                height=zool.FixedAspect(1.0),
                label="{}-{}-2d".format(vars[k], vars[j]),
            )

    # Finish the layout and make the figure.
    fig.layout()

    return fig


def subplot(
    nrows,
    ncolumns,
    width,
    fixed_height=None,
    fixed_aspect=None,
    label_fmt="r{:02d}c{:02d}",
    padding=0.25,
    **kwargs,
):
    """This function returns a simple grid plot of panels.

    Additional keyword arguments are passed straight through to the
    Figure class constructor.  This function can only accept either
    fixed_height or a fixed_aspect specification, both or neither
    will generate an exception.

    Args:
    :param nrows int: Number of rows.
    :param ncolumns int: Number of columns.
    :param width: Width of the figure in cm.
    :param fixed_height: If specified this is the height of the figure in cm.
    :param fixed_aspect: If specified, this is the fixed aspect ratio of each panel.
    :param label_fmt str: Format string for how each panel is labelled.
    :param padding float: Padding between each panel.
    :return Zool figure object: Plot layout.
    """
    if (fixed_height is None) and (fixed_aspect is None):
        raise UserError(
            "Must either have a fixed height or a fixed aspect ratio"
        )
    if (fixed_height is not None) and (fixed_aspect is not None):
        raise UserError(
            "Cannot use both fixed height and fixed panel aspect ratio"
        )

    if fixed_height is not None:
        layout = zool.Figure(
            figwidth=zool.Fixed(width),
            figheight=zool.Fixed(fixed_height),
            layout="vertical",
            padding=padding,
            **kwargs,
        )
    if fixed_aspect is not None:
        layout = zool.Figure(
            figwidth=zool.Fixed(width),
            figheight=zool.FromChildren(),
            layout="vertical",
            padding=padding,
            **kwargs,
        )

    for j in range(nrows):
        rlabel = "r{:02d}".format(j + 1)
        if fixed_aspect is not None:
            layout.add(
                "base",
                width=zool.core.FromParent(),
                height=zool.Named(label_fmt.format(1, 1)),
                layout="horizontal",
                padding=padding,
                label=rlabel,
            )
        if fixed_height is not None:
            layout.add(
                "base",
                width=zool.core.FromParent(),
                height=zool.Fill(),
                layout="horizontal",
                padding=padding,
                label=rlabel,
            )
        for i in range(ncolumns):
            if fixed_aspect is not None:
                layout.add(
                    rlabel,
                    width=zool.Fill(),
                    height=zool.core.FixedAspect(fixed_aspect),
                    label=label_fmt.format(j + 1, i + 1),
                )
            if fixed_height is not None:
                layout.add(
                    rlabel,
                    width=zool.Fill(),
                    height=zool.core.FromParent(),
                    label=label_fmt.format(j + 1, i + 1),
                )
    layout.layout()
    return layout
