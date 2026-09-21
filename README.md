# Bunny Palette

An eight-page Okabe-Ito visualization guide for papers, posters, and websites.

## Instructions for code agents

Use `make_palette_guide.py` as the canonical implementation. When reproducing or adapting it, preserve the rules below unless the task explicitly changes them. For exact reproduction, also preserve random seeds, sample counts, data generation, layout, typography, opacity, and the 3D view.

## Generate the guide

Requires Python 3.10+; NumPy and Matplotlib versions are listed in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python make_palette_guide.py
```

Output: `output/pdf/okabe-ito-visualization-guide.pdf`. Generated files under `output/` are ignored by Git.

## Palette

Preserve hex values and semantic mappings. Default categorical order follows this table; reinforce color with labels, shapes, or line styles.

| Color | Hex | Role |
|---|---|---|
| Blue | `#0072B2` | Primary accent, control model, negative diverging endpoint |
| Orange | `#E69F00` | Categorical series, regression alternative |
| Bluish green | `#009E73` | Categorical series, embedding group |
| Vermilion | `#D55E00` | Categorical series, positive diverging endpoint |
| Reddish purple | `#CC79A7` | Regression alternative, embedding group, diverging endpoint |
| Sky blue | `#56B4E9` | Secondary categorical color |
| Yellow | `#F0E442` | Fills or dark backgrounds; avoid thin marks on white |
| Black | `#000000` | Categorical fallback |

| Neutral | Hex |
|---|---|
| Ink | `#17202A` |
| Secondary text | `#5F6B76` |
| Border | `#CBD2D9` |
| Canvas | `#F3F5F7` |
| White | `#FFFFFF` |

## Rendering rules

### Color derivation

Use linear RGB mixing with white: `mixed = (1 - t) * base_rgb + t * white_rgb`.

- Tint levels (`t`): `0.90`, `0.75`, `0.55`, `0.32`, `0.00`.
- Random embedding tints: `0.02-0.46` in 2D; `0.02-0.44` in 3D.
- Sequential heatmaps: White -> Blue mixed with 62% white -> Blue.
- Diverging heatmaps: Blue -> White -> Vermilion or Reddish purple. Keep the original endpoints; do not darken them.

### Marker sizing

Reuse `adaptive_point_area`: normalize each selected dimension to its observed range, calculate nearest-neighbor distances, then return `clip(6 + 250 * median_distance, 6, 28)` in points squared. Marker sizes are areas, not radii or diameters.

- Preserve `MARK_DISPLAY_SCALE = 1.30`.
- Regression: multiply base area by the display scale. In smaller panels, additionally scale area by the panel-area ratio to the single-model panel, and line width by the square root of that ratio.
- Embeddings: use `1.25 * MARK_DISPLAY_SCALE * base_area`, with per-point area variation of `0.75-1.25`. Both 2D and 3D compute spacing from the x/y coordinates.
- 3D shadows use the unscaled base area; point enlargement must not enlarge shadows.

### Chart behavior

- Regression: match observation and fit hues; keep observations faint and uncertainty bands transparent behind points and lines. Two-model pairs are Blue + Orange and Blue + Reddish purple, with circle/square markers.
- 2D embedding: Blue, Orange, and Bluish green groups; hide axes, ticks, and coordinate labels.
- 3D embedding: Bluish green and Reddish purple groups; hide axes, ticks, and coordinate labels. Keep the floor below the cloud and projected shadows within its bounds. Lower points cast darker, tighter shadows; higher points cast lighter, broader shadows.

## Verify changes

After rendering changes, regenerate all eight pages and compare them with the previews below. Check colors, marker scaling, uncertainty bands, hidden embedding axes, and floor/shadow geometry. Update screenshots only when the visual change is intentional; keep them in `docs/screenshots/`.

## Screenshots

Pages 1-8, in order: palette, tints, categorical charts, regression, heatmaps, 2D embedding, 3D embedding, and recipes.

| Palette and neutrals | Tints and transitions |
|---|---|
| ![Palette and neutral colors](docs/screenshots/01-palette.png) | ![Tint levels and diverging ramps](docs/screenshots/02-tints.png) |

| Categorical charts | Regression and uncertainty |
|---|---|
| ![Categorical bar, line, and scatter charts](docs/screenshots/03-categorical.png) | ![Regression models with uncertainty bands](docs/screenshots/04-regression.png) |

| Heatmaps | 2D embedding |
|---|---|
| ![Sequential and diverging heatmaps](docs/screenshots/05-heatmaps.png) | ![Three-group 2D embedding](docs/screenshots/06-embedding-2d.png) |

| 3D embedding | Palette recipes |
|---|---|
| ![3D embedding with projected shadows](docs/screenshots/07-embedding-3d.png) | ![Ready-to-use palette recipes](docs/screenshots/08-recipes.png) |
