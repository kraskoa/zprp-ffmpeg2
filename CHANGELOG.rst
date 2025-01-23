Changelog
~~~~~~~~~

All notable changes to this project will be documented in this file.
Dates are displayed in UTC.

`v3.2.0 <https://github.com/kraskoa/zprp-ffmpeg2/compare/v3.1.1...v3.2.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   23 January 2025

-  Improved splitting in the new view()
   ```f67ad12`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/f67ad128d28e8e757e11f6f609773c92f0477303>`__
-  Finished fixing inconsistencies uncovered by `mypy`
   ```3d4405f`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/3d4405f2cad64899b97e94c718c723051ab87ced>`__


`v3.1.1 <https://github.com/kraskoa/zprp-ffmpeg2/compare/v3.1.0...v3.1.1>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   20 January 2025

-  Fixed incorrect implementation of merge_outputs() function
   ```f991c3d`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/f991c3d594d593b8c11fed2054a21a44df9d7b3a>`__
-  Cosmetic and slight logical changes to view.py
   ```d7cf00a`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/d7cf00afe8c2d708af85b3b97791232803c77c18>`__
-  Some tests for changed functionalities
   ```7dc11d6`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/7dc11d68266d5aba8f62915d5a5407bfb809a5e9>`__

`v3.1.0 <https://github.com/kraskoa/zprp-ffmpeg2/compare/v3.0.1...v3.1.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   16 January 2025

-  Expanded input() function to accept kwargs
   ```f8385ee`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/f8385eea55c635971b3e7b9fb376e9dcc91161ce>`__
-  Refactored and added tests for new functions
   ```fad8b24`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/fad8b24f2e55c6d40683a3e3c3428c3115b70cad>`__
-  Final implementation of Node.get_command(), using dataclasses this time
   ```3670704`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/3670704a5871445500d8166f7910865b5982cc3b>`__
-  Final implementation of merge_outputs() function from ffmpeg-python
   ```4ae6419`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/4ae6419ad0cc68cee1afcf0760cec80d181bec32>`__
-  Modified the view() function to work with new functions as well
   ```9d6f097`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/9d6f097920f48ff91851bacbc4251d28ecd2d8db>`__

`v3.0.1 <https://github.com/kraskoa/zprp-ffmpeg2/compare/v2.2.0...v3.0.1>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   22 December 2024

-  Refactored Node.get_command() to not operate on strings, using dictionaries instead
   ```dcf0c87`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/dcf0c87bbe1e07ea5844fcdc3e832f2214f40f5a>`__
-  Added concat() tests from the original ffmpeg-python library
   ```8226e09`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/8226e0969ecae35d42a2c784cc021c4412399868>`__
-  Initial implementation of the merge_outputs() function from ffmpeg-python
   ```ddf68a4`` <https://github.com/kraskoa/zprp-ffmpeg2/commit/ddf68a4b5e683e06f44050957064a2a718b66515>`__

`v2.2.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v2.1.2...v2.2.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   11 June 2024

-  Use oslex library for command splitting
   ```#11`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/11>`__
-  fix: add tox to poetry dependencies, change pytest version
   ```6b22bc1`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/6b22bc1167c71991e5105b5254d3cd76aeb49276>`__
-  fix: pipe stderr and stdout out of ffmpeg
   ```ce84a5e`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/ce84a5e76062dc70575ca43073f702c138c01996>`__
-  style: make filenames consistent
   ```7e38977`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/7e389776bca5886fa8fa5456b3ae29d1540e5b36>`__

`v2.1.2 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v2.1.1...v2.1.2>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   2 June 2024

-  Bump version: 2.1.1 → 2.1.2
   ```94ce1c6`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/94ce1c6af7285a4ff9e8fd357979b4eb16ac7ea0>`__
-  Apply automatic changes
   ```ee0f3c1`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/ee0f3c1e1eeca54f46846fe44fa19ec97289fddc>`__
-  fix: overlay filter had invalid arguments to ffmpeg
   ```8291888`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/8291888fc247e4c3862ad70c454684b02c6cb4c5>`__

`v2.1.1 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v2.1.0...v2.1.1>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   2 June 2024

-  fix: linting and mypy issues
   ```9589ec9`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/9589ec97c1f7e519bbcd956d9119910d54fb2a49>`__
-  Update interactive.
   ```e4912b8`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/e4912b8c621488eee02037f1afb2a445100f583a>`__
-  Bump version: 2.1.0 → 2.1.1
   ```4c40e82`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/4c40e82324a97a4115d6c31e04203834e38fc5a0>`__

`v2.1.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v2.0.0...v2.1.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   1 June 2024

-  Improving compatibility
   ```#7`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/7>`__
-  update lock.
   ```d4dce79`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/d4dce798ad3a18255c6f1f9dafd82a49f7d8f094>`__
-  Update lock.
   ```7178391`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/71783915fdb6287efeff03a9b790df7df7ae51b2>`__
-  Added more old api tests
   ```be2f8f1`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/be2f8f13d56a2fed25aeb6d681a2cffbf34e92c4>`__

`v2.0.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v1.2.0...v2.0.0>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   1 June 2024

-  Complex filter
   ```#6`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/6>`__
-  Fix: incorrect showing of params.
   ```f0e28e5`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/f0e28e570a344a8162939b7ca2e7f269b2099ef4>`__
-  Interactive example.
   ```57fed5c`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/57fed5ccb9fe9cc11f1752088277d301f5062610>`__
-  feat: Add overlay filter
   ```94aa24c`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/94aa24c2599006bcc16afd9671923bf7cb15c9bd>`__

`v1.2.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v1.1.0...v1.2.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   25 May 2024

-  feat: Add graph for basic filters
   ```#5`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/5>`__
-  Fix: update lock file
   ```aec6f02`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/aec6f02946c46581b61a56670b90e0ca0b0eea1e>`__
-  Apply automatic changes
   ```6da9cc6`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/6da9cc698d5bbcbac78b812b49412aa411d2c43d>`__
-  Next time commit tags after new version
   ```2f8fe73`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/2f8fe7333820b165efe5095a0389eb11f8ec5120>`__

`v1.1.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v1.0.0...v1.1.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   25 May 2024

-  feat: Add ffprobe function
   ```#4`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/4>`__
-  add ffmpeg headers for tests
   ```881d6ea`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/881d6ea0bdcfccdaed53ef87b019ce1982911cf6>`__
-  fix: properly parse flag-type options
   ```c9384d0`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/c9384d061f5c2f60c89798fb0700c81f61f38185>`__
-  fix: move ``generate_filters.py`` out of package, so that it works
   both with mypy and normal run
   ```74cb5f6`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/74cb5f6590214bfe7d13447ea9c489e16cfd8c55>`__

`v1.0.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v0.1.0...v1.0.0>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   10 May 2024

-  feature: extract filter type (video, audio) from source code. Make
   all filter options optional
   ```c77af88`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/c77af8807ed7dc650d80781682ad98249bab3faa>`__
-  refactor: code is more readable, split into files, changed prints to
   logger with debug level
   ```2e42ae8`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/2e42ae8a3a6d5785adfe3aef596ada3d5e584074>`__
-  fix: take care of typing in autogen code
   ```fef9dab`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/fef9dabb56efacf058fbd08744bc412f765a95d9>`__

`v0.1.0 <https://github.com/ffmpeg-zprp/zprp-ffmpeg/compare/v0.0.0...v0.1.0>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   29 April 2024

-  Mypy ```#2`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/2>`__
-  Ffmpeg connector and initial stream class logic
   ```#1`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/pull/1>`__
-  feature: add very basic graph structure and crucial api parts
   ```cb6c4fd`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/cb6c4fd2473b66f968131dfd806e82902395f78b>`__
-  feature: crucial base classes for the package
   ```e133438`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/e133438f08fbf248f28e7d67b4c40640ed9f3717>`__
-  fix: remove not needed class, fix mypy type errors
   ```91aa8cf`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/91aa8cf23ad051d4126083c57f6749bd49d4d517>`__

v0.0.0
^^^^^^

   26 March 2024

-  Change authors
   ```2892f0f`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/2892f0fac9b13743e06969e8e8a46ee8792541dd>`__
-  Restore design proposal
   ```09e47f5`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/09e47f5279fc933980b10e220292e400f2635b4e>`__
-  Try to revert merge.
   ```6c4fda6`` <https://github.com/ffmpeg-zprp/zprp-ffmpeg/commit/6c4fda6d834687cc2a3e4e9cca4df722df1356aa>`__
