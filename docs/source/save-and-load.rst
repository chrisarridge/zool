Saving and Loading
==================
Zool layouts can be saved as ``JSON`` files that can be read in again and re-created.

Load example:
Let's say we have defined this class and our JSON file includes objects of this class.

.. code-block:: python
    import json

    class Layout_data:
        def __init__(self, data):
            self.data = data
    
        @classmethod
        def from_json(cls, json_data):
            # Assuming the JSON data has a key called 'data'
            return cls(json_data['data'])

Let's then assume the JSON file `layout.json` contains these objects.
The file can be loaded using the commands:

.. code-block:: python

    filename Layout_data = "layout.json"
    loaded_layout = Layout.load(Layout_data, filename)

Save example:
Let's say we have a Layout object called `example_layout`. 
This ca be saved using:
.. code-block:: python
    example_layout: Layout
    example_layout.save('layoutfile.json')