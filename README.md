# Project-Lemma
## Before we get started
Sync venv using uv
```
uv sync
```

Prepare the images will be used to during the image gerneration, put it in the `images` folder, and you can customize the path in the yaml.
```
Project-Lemma
├── LICENSE
├── README.md
├── example.yaml
├── image
├── image_generator.py
├── output
│   ├── gundam_quote.png
│   ├── memento_mori.png
│   ├── motivation_custom_bg.png
│   ├── motivation_fixed-2.png
│   └── motivation_fixed.png
├── pyproject.toml
└── uv.lock
```

## Usage
use `-f` for to specift the input source yaml file.
```
uv run python image_generator.py -f example.yaml
```

example output
![Gundam Quote](https://github.com/vincent5753/Project-Lemma/blob/main/gundam_quote.png?raw=true)

## TDL
### Core & Data Structure
Separate quote text and source/attribution in YAML schemas

### Effects
Background pic zoom in/out effect
Source text style
More Phrase text style
