# Generated artifacts

Everything under `dist/` is generated release or target-build output and must not be edited manually.

The tracked public discovery indexes intentionally live outside this ignored build directory: `catalog/index.json` for machines and `CATALOGUE.md` for people. Both are regenerated with `pnpm run build:catalogue` and checked for freshness by `pnpm run check`.
