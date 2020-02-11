"""Demonstration of Zool's plotting layout engine."""

# Modules to import
import zool
import matplotlib.pyplot as plt

# Here is a grid of panels with a fixed panel aspect ratio
fig = zool.subplot(2, 3, 20.0, fixed_aspect=16.0/9.0)
fig.new()
fig.axes('r01c01')
fig.axes('r01c02')
fig.axes('r01c03')
fig.axes('r02c01')
fig.axes('r02c02')
fig.axes('r02c03')
plt.savefig('example7.pdf')

# Save this figure to JSON.
fig.to_json('test_example7.json')
new_fig = zool.Figure.from_json('test_example7.json')
new_fig.new()
new_fig.axes('r01c01')
new_fig.axes('r01c02')
new_fig.axes('r01c03')
new_fig.axes('r02c01')
new_fig.axes('r02c02')
new_fig.axes('r02c03')
plt.savefig('example7_loaded.pdf')

# First example, a fairly straight-forward vertical stack of panels.
print('Example 1: fairly straight-forward vertical stack')
fig = zool.Figure(figwidth=zool.Fixed(10.0), figheight=zool.FromChildren(),
				layout='vertical', padding=0.5, margin_left=2,
				margin_right=2)
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0), label='a')
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0), label='b')
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0), label='c')
fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0), label='d')
fig.layout()
fig.show()
fig.preview()
fig.new()
fig.axes('a')
fig.axes('b')
fig.axes('c')
fig.axes('d')
plt.savefig('example1.pdf')
print('\n\n')

# Second example, the same thing, but each panel has a fixed aspect ratio.
print('Example 2: fairly straight-forward vertical stack but with fixed aspect ratio')
fig = zool.Figure(figwidth=zool.Fixed(10.0), figheight=zool.FromChildren(),
				layout='vertical', padding=0.5, margin_left=2,
				margin_right=2)
fig.add('base',width=zool.FromParent(), height=zool.FixedAspect(1.0), label='a')
fig.add('base',width=zool.FromParent(), height=zool.FixedAspect(1.0), label='b')
fig.add('base',width=zool.FromParent(), height=zool.FixedAspect(1.0), label='c')
fig.add('base',width=zool.Named('a'), height=zool.Named('a'), label='d')
fig.layout()
fig.show()
fig.preview()
fig.new()
fig.axes('a')
fig.axes('b')
fig.axes('c')
fig.axes('d')
plt.savefig('example2.pdf')
print('\n\n')


# Example with a more complicated layout.
print('Example 3: More complicated layout')
fig = zool.Figure(figwidth=zool.Fixed(20.0),figheight=zool.FromChildren(),
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


# Now demo the factory functions.  Here is a simple vertical stack of panels
# with a fixed width.
fig = zool.vertical_stack([1,2,3,4], figwidth=zool.core.Fixed(10.0))
fig.new()
fig.axes('0')
fig.axes('1')
fig.axes('2')
fig.axes('3')
plt.savefig('example4.pdf')

# Here is a triangle plot with fixed aspect ratio 2d histograms and a fixed
# figure width.
a = zool.triangle_equal(['a','b','c','d'], zool.Fixed(16.0), margin_left=2.0, margin_bottom=2.0, margin_top=0.25, margin_right=0.25)
a.new()
a.axes('b-1d-v')
a.axes('c-1d-v')
a.axes('d-1d-v')
a.axes('a-1d-h')
a.axes('d-1d-h')
a.axes('c-1d-h')
a.axes('a-b-2d')
a.axes('a-c-2d')
a.axes('a-d-2d')
a.axes('d-b-2d')
a.axes('d-c-2d')
a.axes('c-b-2d')
plt.savefig('example5.pdf')


# Here is a grid of panels with a fixed figure height
fig = zool.subplot(2, 3, 16.0, fixed_height=10.0)
fig.new()
fig.axes('r01c01')
fig.axes('r01c02')
fig.axes('r01c03')
fig.axes('r02c01')
fig.axes('r02c02')
fig.axes('r02c03')
plt.savefig('example6.pdf')

# Here is a grid of panels with a fixed panel aspect ratio
fig = zool.subplot(2, 3, 20.0, fixed_aspect=16.0/9.0)
fig.new()
fig.axes('r01c01')
fig.axes('r01c02')
fig.axes('r01c03')
fig.axes('r02c01')
fig.axes('r02c02')
fig.axes('r02c03')
plt.savefig('example7.pdf')

# Save this figure to JSON.
fig.to_json('test_example7.json')
new_fig = zool.Figure.from_json('test_example7.json')
new_fig.new()
new_fig.axes('r01c01')
new_fig.axes('r01c02')
new_fig.axes('r01c03')
new_fig.axes('r02c01')
new_fig.axes('r02c02')
new_fig.axes('r02c03')
plt.savefig('example7_loaded.pdf')
