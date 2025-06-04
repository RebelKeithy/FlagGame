# Flag Game

An interactive flag colouring app built with [React](https://react.dev/) and [Vite](https://vitejs.dev/). It allows you to pick a country, choose a colour, and apply it to different parts of the flag SVG.

## Features

- Choose from a list of countries and display its flag
- Click individual shapes in the flag to change their colour
- Predefined colour picker for quick selection
- Flags stored as SVGs under `public/flags`
- Tools to generate new flag templates

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   Then open the printed local URL in your browser.

To build a production bundle run:
```bash
npm run build
```
You can preview the production build with:
```bash
npm run preview
```
Lint the project with:
```bash
npm run lint
```

## Generating Flags

Flags are standard SVGs placed in the `public/flags` directory. A flexible generator script is included:

```bash
python3 create_flag.py COUNTRY_NAME -x WIDTH -y HEIGHT [options]
```

The script accepts many options such as `--vertical`, `--horizontal`, `--circle`, `--cross`, `--star`, `--moon`, `--rect` and `--triangle`. Generated files are written to `public/flags` by default. See `create_flag.py --help` for the full list of arguments and examples.

The helper script `generate_flag_array.sh` prints a JSON array of the available country codes based on the files in `public/flags`.

## License

This project is provided as-is under the MIT license.
