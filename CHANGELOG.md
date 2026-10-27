# Changelog

## 1.0.0 - 2026-10-27

First public release.

- API keys and the music folder are read from environment variables or a `.env` file
- Weather now requests metric units, so temperatures are really in Celsius
- Wolfram Alpha lookups use the `query` call
- The speech voice is selected correctly, with a fallback when only one voice is installed
- Unrecognised speech no longer stops the loop or crashes it
- Wikipedia disambiguation and missing pages are handled
- The assistant no longer starts speaking when the file is imported
- Added a date command, a Google search command and a missing-folder check for music
