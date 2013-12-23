light-layers
============

Layer abstraction for the Holiday by MooresCloud. Provides a number of functions for
doing colour washes and fades over time. 

Simple use case:
1. Create a layer with new LightLayer()
2. Create a ramp-up with ramp(). 
3. Create a wash() for some colour.
4. Move the 'current time' forward with wait()
6. Send them to a Holiday with render(). It will wait until it's finished before returning to you.

And because it was easy, support is provided for specifying colours by X11 name. See
https://en.wikipedia.org/wiki/Web\_colours for the list supported. It is case-insensitive
and allows spaces but does not require them. Otherwise, colours are in lists or tuples as a red/green/blue triple.

Currently expects to talk REST across the network. Will add SecretAPI support soon.

