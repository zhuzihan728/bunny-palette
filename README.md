# Bunny Palette

An eight-page Okabe-Ito color guide with palettes, gradients, charts, heatmaps, and 2D/3D examples.

## Usage

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python make_palette_guide.py
```

Output: `output/pdf/okabe-ito-visualization-guide.pdf`.

## Palette

| Color | Hex |
|---|---|
| Blue | `#0072B2` |
| Orange | `#E69F00` |
| Bluish green | `#009E73` |
| Vermilion | `#D55E00` |
| Reddish purple | `#CC79A7` |
| Sky blue | `#56B4E9` |
| Yellow | `#F0E442` |
| Black | `#000000` |

## Screenshots

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
