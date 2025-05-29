.. Swanki documentation master file

Welcome to Swanki's Documentation!
==================================

**Swanki** is an automated flashcard generation tool that transforms academic PDFs into Anki flashcards with AI-generated content. It processes PDFs by extracting text and images, generating summaries, creating question-answer pairs, and optionally adding audio narration.

.. image:: https://img.shields.io/pypi/v/swanki.svg
   :target: https://pypi.org/project/swanki/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/swanki.svg
   :target: https://pypi.org/project/swanki/
   :alt: Python versions

Features
--------

- 📄 **PDF Processing**: Split and convert PDFs to markdown using Mathpix
- 🧹 **Content Cleaning**: Clean and standardize markdown formatting
- 🖼️ **Image Analysis**: Extract and summarize images with GPT-4 Vision
- 🎴 **Smart Card Generation**: Create contextual flashcards with AI
- 🔊 **Audio Support**: Generate TTS audio for cards using ElevenLabs
- 📤 **Anki Integration**: Direct upload to Anki via AnkiConnect
- ⚙️ **Configurable Pipeline**: Hydra-based configuration system

Quick Start
-----------

.. code-block:: bash

   # Install Swanki
   pip install swanki

   # Process a PDF
   swanki pdf_path=paper.pdf citation_key=smith2023

   # With audio generation
   swanki pdf_path=paper.pdf citation_key=smith2023 audio=cards

   # Auto-send to Anki
   swanki pdf_path=paper.pdf citation_key=smith2023 anki=auto_send

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   introduction
   installation
   quickstart
   configuration
   cli-usage
   pipeline

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/swanki
   api/models
   api/pipeline
   api/processing
   api/utils

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`