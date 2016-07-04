# MouseGestureRecognition

## Recognize different mouse gestures using simple logistic regression
To recognize and categorize different mouse gestures using simple logistic regression. The model is trained with very high accuracy (98%). I had some doubt about overfitting too but it works very well in practice.

## Symbols learnt
1. U (letter u): U
2. Alpha (greek alpha letter): α. Unfortunately, the way I write alpha makes it looks like the [Ichthys](https://en.wikipedia.org/wiki/Ichthys) symbol.
3. Hat: ^
4. Z (letter z): Z
5. The derivative symbol (looks like an intverted 6): ∂
6. Triangle (equilateral triangle pointing upward): △
7. Greater than: >

This list is definitely extendable simply by adding more training samples and let the model learn them.

## Demo
To start the demo, start the server first by running

```
$python server.py
```

Then you can run the demo jar

```
$java -jar Demo.jar
```

The demo will exit after 20s. To run it for a long while, use the following (Ctrl + C twice to exit)

```
while true ; do java -jar Demo.jar ; done
```

Register the drawing by holding down left ctrl, draw a pattern with the mouse, and release left ctrl. The server will try to recognize the pattern and a small popup will appear if a symbol is recognized.

## Libraries used
[JNativeHook](https://github.com/kwhat/jnativehook/) (for the demo only)
[scikitlearn](http://scikit-learn.org/)
[Argo JSON](http://argo.sourceforge.net/)
