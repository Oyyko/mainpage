---
title: Value categories in Cpp
date: 2022-08-23
tags: [Cpp]
---

## Intro

```cpp
#define IS_XVALUE(expr) \
(is_rvalue_reference<decltype((expr))>{})
#define IS_PRVALUE(expr) \
(!is_reference<decltype((expr))>{})
#define IS_LVALUE(expr) \
(is_lvalue_reference<decltype((expr))>{})
```

This is a method I recently discovered to determine which value category an **expression** is. I'll explain why it works later.

First, let's take a look at value categories in C++.

One of the most important things you should notice before you start is that value categories are not a property about **values**, but rather a property about **expressions**. Actually it depends on how you understand **value**, I looked through the C++ standard but **it seems they don't define what the term value means**. However, we all know what an expression is. (in case you don't know, you can refer to cppreference)

Anyway, there are 3 kinds of value categories. They are called LVALUE, PRVALUE, XVALUE.

We know you can write x=3 but not 3=x. Since 3 and x are both expressions, there must be some qualitative difference between them. Since x can be placed to the left of the equals sign(assignment sign), so we call it an lvalue. 3 is called an rvalue accordingly.

OK. Now I know the difference between LVALUE and RVALUE, but what is PRVALUE and XVALUE?

Well, there are two dimensions to the form of expressions. 1. Does the expression have an identity? 2. Can the expression be moved?

The one that has identity and can be moved is called XVALUE (eXpiring value).
The one that has identity but cannot be moved is called LVALUE.
The one that has no identity but can be moved is called PRVALUE.

For example, these are examples for XVALUE:
```cpp
std::move(x);
a.m, the member of object expression, where a is an rvalue and m is a non-static data member of non-reference type;
```

## Temporary materialization

The most useful example to help you understand XVALUE is: Temporary materialization.

```cpp
struct S { int m; }; 
int i = S().m; // member access expects glvalue as of C++17;
               // S() prvalue is converted to xvalue
```

As the cppreference goes: A prvalue of any complete type T can be converted to an xvalue of the same type T. This conversion initializes a temporary object of type T from the prvalue by evaluating the prvalue with the temporary object as its result object, and produces an xvalue denoting the temporary object. If T is a class or array of class type, it must have an accessible and non-deleted destructor.

So the key difference between XVALUE and PRVALUE is that can we **reuse** the resources of it. We cannot reuse the number 3 or 3.7 but **we can reuse the memory allocated for a temporary string object**.

## Decltype and value categories

Decltype is a good tool to help us determine the category of an expression. 

Because its behavior is to generate an rvalue reference for XVALUE, an unreferenced type for PRVALUE, and an lvalue reference for LVALUE.

Well, someone may argue that if `int x=3;` then `x is an LVALUE but decltype(x) is int itself rather than int&.` That's because the special case for id-expr in the behavior of decltype.

If the argument is an unparenthesized id-expression or an unparenthesized class member access expression, then decltype yields the type of the entity named by this expression. If there is no such entity, or if the argument names a set of overloaded functions, the program is ill-formed.

So the right way is `int x=3; decltype((x)) xref=x;`. Here the type of `xref` is `int&`.

## std::move

The famous function `move` actually does nothing to do with "move something". Actually, it just change the value category of the parameter from LVALUE to XVALUE. In the most cases, you should call move using an LVALUE.

std::move is used to **indicate** that an object t may be "moved from", i.e. allowing the efficient transfer of resources from t to another object.

In particular, std::move produces an xvalue expression that identifies its argument t. It is exactly equivalent to a static_cast to an rvalue reference type.







