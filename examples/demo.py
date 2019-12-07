"""Demonstration of Zool's plotting layout engine."""

# Modules to import
import zool
import matplotlib.pyplot

fig = zool.Plot(width=zool.Fixed(10.0), height=zool.FromChildren(),
				layout='vertical', padding=0.5, margin_left=2,
				margin_right=2)
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
fig.show()
fig.layout()
fig.show()
fig.preview()



# Start the figure and make the top level frame.
fig = zool.Plot(width=zool.Fixed(20.0),height=zool.FromChildren(),
			layout='vertical',padding=0.5,
			margin_left=3.0,margin_right=3.0,margin_bottom=2.0,margin_top=1.0)
fig.add('base', width=zool.FromParent(), height=zool.Fixed(5.0), label='A1')
fig.add('base', width=zool.FromParent(), height=zool.Fixed(5.0), label='B1')
fig.add('base', width=zool.FromParent(), height=zool.Fixed(10.0), label='C1')
fig.add('base', width=zool.FromParent(), height=zool.Fixed(10.0), label='FR2',
		layout='horizontal', padding=1.0)

# Populate the second frame.
fig.add('FR2',width=zool.Fixed(5.0),height=zool.FromParent(),label='A2')
fig.add('FR2',width=zool.Fill(),height=zool.FromParent(),label='FR3',
		layout='horizontal',padding=0.5)
fig.add('FR2',width=zool.Fill(),height=zool.FromParent(),label='B2')
fig.add('FR2',width=zool.Fill(),height=zool.FromParent(),label='C2')

# Add items to the third frame.
fig.add('FR3',width=zool.Fill(),height=zool.FromParent(),label='A3')
fig.add('FR3',width=zool.Fill(),height=zool.FromParent(),label='B3')

# do the layout
fig.layout()
fig.show()
fig.preview()
