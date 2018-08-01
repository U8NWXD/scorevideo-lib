# Plan for `scorevideo-lib`

## Structure of Library Utilities
* Log File Utilities
  * Break log file into its sections:
    * Header
    * Video ID
    * Commands
    * Raw Log
    * Full Log
    * Notes
    * Marks
  * From relevant sections, extract data:
    * Behaviors
    * Video Duration
    * Sequence Number
  * Insert mark into Marks section
  * Compute time differential between arbitrary log entries across files
  * Based on a "lights-on" log, insert marks into scoring logs

## Testing
Use [pytest](https://docs.python-guide.org/writing/tests/) to write unittests in parallel files alongside main code
(e.g. `test_example.py` in the same directory as `example.py`). Tests will then be run frequently using continuous 
integration.

Also consider trialing [hypothesis](https://hypothesis.readthedocs.io/en/latest/), which will identify from unit tests
edge cases to consider.

## Hosting
Open-source on GitHub.

## Continuous Integration
Use Travis-CI. For tutorial, see https://docs.python-guide.org/scenarios/ci/.