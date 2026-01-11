============
rst2revealjs
============

.. important:: This is experimental project!!

Simple convert from docutils AST to Reveal.js presentation.

Overview
========

This is docutils adapter to write Reveal.js presentation by reStructuredText and other formats.
You can write presentation by plain text using many expression of reStructuredText.

Usage
=====

.. warning:: This section is included plan and it is not availabled yet.

.. code:: console

   pip install rst2revealjs

.. code:: rst

   Title
   =====

   Section 1
   =========

   Section 1-1
   -----------

.. code:: console

   rst2revealjs presentation.rst

You can see `presentation.html` by your browser.

Features
========

This provides some features to realize overview.

* Custom directives for specify behaviors about Reveal.js.
* Writer to generate HTML file using Reveal.js presentation.

Motivation
==========

This is re-implement from core features of sphinx-revealjs.
Because I want to write Reveal.js presentation on Web front-end using Pyodide. [#]_

As first goal, I will provide playground website to convert from reStructuredText to presentation using this.

License
=======

Apache-2.0 license. Please see LICENSE on repository.

.. ruburic::

.. [#] docutils is registered on Pyodided built-in packages, but Sphinx is not registered.
