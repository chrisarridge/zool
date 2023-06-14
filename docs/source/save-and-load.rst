Saving and Loading
==================
Zool layouts can be saved as ``JSON`` files that can be read in again and re-created.

**Load example:**
We define `example_layout`:

.. code-block:: python


    import zool
    
    example_layout: Layout = zool.Layout(figwidth=10.0, layout='vertical', padding=0.5,
                     margin_left=2, margin_right=0.5, margin_top=0.5, margin_bottom=2.0)


A file file can be loaded using the following code:

.. code-block:: python

    filename Layout_data = "layout.json"
    loaded_layout = Layout.load(example_layout, filename)

**Save example:**
We define a Layout object called `example_layout`. 
This can be saved using:
.. code-block:: python
    example_layout: Layout = = zool.Layout(figwidth=10.0, layout='vertical', padding=0.5,
                     margin_left=2, margin_right=0.5, margin_top=0.5, margin_bottom=2.0)
    example_layout.save('layoutFile.json')