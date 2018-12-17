---
layout: post
date: 2018-12-17 20:24:00 +0800
title: "Marks during developing oscilliscope GUI"
comments: true
---
### 1.Qt5-serial package
On linux user should install the qt5-serial package for the implementation of QtSerialPort.so file.(In my case --- Arch Linux.)

### 2.Lamba
I have used ***lamba*** for pass arguments to the functions that connnected with UI elements' change.

### 3.Can't read vaild data for serial port?
While using `QtSerialPort.QSerialPort`, without implement `QSerialPort.waitReadyRead(int milliseconds)` will cause always read empty data from serial port, and the `QSerialPort.readyRead` signal cannot be emitted.(*Only tested in python interactive terminal,and so there is no event loop because of I didn't create a QApplication*)

And after test in a real QApplication with GUI, I found that doesn't like in the interactive terminal model, the `QSerialPort.readyRead` can be emitted.

Sum them up, the difference between QtSerial communication in python interactive terminal and in a real QApplication is whether you need to mannully call the `QSerialPort.waitReadyRead()` function.In python interactive terminal you need I thought that's probably because there is no event loop without a QApplication.

### 4.Big Bang!!!

What I found is that unlike C or C++ programming language,arguments pass to a python function are the uniqued ones.

What I mean is when you pass a variable or something which does have a pointer in C/C++ to function in C/C++ code, then the function will allocates new space to store the argument variable, and it only passes in the original variable's value, so if you do some change to this variable inside function,the original one won't be changed,because they have different pointer.

~~But in python codes, it's completely different.When you pass a variable or instance to a function, if the code in function changes the passed in variable,then the original one(in fact the same one, I tested and found their "id" is the same) will also changed.~~[Reference source](https://stackoverflow.com/questions/22558739/without-pointers-can-i-pass-references-as-arguments-in-python)

And I copied a paragraph from [here](https://stackoverflow.com/questions/986006/how-do-i-pass-a-variable-by-reference):
> Arguments are **passed by assignment**. The rationale behind this is twofold:
 
> 1.the parameter passed in is actually a reference to an object (but the reference is passed by value)
> 2.some data types are mutable, but others aren't.

> So: If you pass a mutable object into a method, the method gets a reference to that same object and you can mutate it to your heart's delight, but if you rebind the reference in the method, the outer scope will know nothing about it, and after you're done, the outer reference will still point at the original object.If you pass an immutable object to a method, you still can't rebind the outer reference, and you can't even mutate the object.To make it even more clear, let's have some examples.

I found the different between C language's "=" and python's "=".There are some codes in python:
{% highlight python %}
class TestIdClass():
	def __init__(self, item):
		print('This is one passed in.\n' + str(id(item)))
		self.item = item
		print("This is this instance's attribute\n" + str(id(self.item)))

x = 13

print('This is the original one\n' + str(id(x)))
test_id_class = TestIdClass(x)
{% endhighlight %}
And it output is this:
```
This is the original one
139678317521440
This is one passed in.
139678317521440
This is this instance's attribute
139678317521440
```
Their ids are the same, it means they are actually the same one.

So, the "=" operator in python lets the variable or instance in left side references to the right one(In my opinion), so they are actually the same,and have same ids.

But in C/C++, operator "=" does transfer the value from right side to left side, and so they are no the same(In my opinion).

### 5.QTimer
I discovered that the QTimer can't be used or declared inside a function as a local variable, if I do so, timer will not be validated. It probably needs to be a global variable.

### 6.Encountering intractable problems
 - 2018-01-06 

### 7.We've backed for development!
 - 2018-12-17